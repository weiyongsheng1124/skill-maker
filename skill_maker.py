"""
Skill Maker - 自動生成符合設計原則的 Agent Skills

設計原則：
1. Skill 必須可獨立呼叫
2. Skill 必須明確輸入輸出
3. Skill 必須可測試
4. 避免生成過度細碎的 Skill
"""

import os
import json
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path


@dataclass
class SkillSpec:
    """Skill 規格"""
    name: str
    description: str
    version: str = "1.0.0"
    inputs: List[str] = None
    outputs: List[str] = None
    template: str = "simple"
    logic: str = None


class SkillMaker:
    """
    Skill 產生器
    
    根據規格產生符合設計原則的 Agent Skill
    """
    
    TEMPLATES = {
        "simple": """
def execute({inputs_str}) -> {output_class}:
    \"\"\"
    {description}
    \"\"\"
    # TODO: 實現核心邏輯
    
    # 評分邏輯
    score = 0
    reasons = []
    
    # 輸出結果
    return {output_class}(
        success=True,
        data={{}}
    )
""",
        "scoring": """
def calculate_scores(df, params):
    \"\"\"計算各指標分數\"\"\"
    score = 0
    reasons = []
    
    # 評分邏輯
    {logic}
    
    return score, reasons

def execute({inputs_str}) -> {output_class}:
    \"\"\"
    {description}
    
    評分機制：
    - 總分計算
    - 閾值判斷
    \"\"\"
    score, reasons = calculate_scores(df, params)
    
    # 最終決策
    threshold = params.get("threshold", 3)
    success = score >= threshold
    
    return {output_class}(
        success=success,
        score=score,
        reasons=reasons,
        data={{}}
    )
""",
        "trading": """
def execute({inputs_str}) -> {output_class}:
    \"\"\"
    {description}
    
    整合：
    - 進場判斷
    - 風控計算
    - 部位管理
    \"\"\"
    # TODO: 實現核心邏輯
    
    return {output_class}(
        should_buy=False,
        should_sell=False,
        score=0,
        reasons=[],
        data={{}}
    )
"""
    }
    
    def __init__(self, output_dir: str = "./generated_skills"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_skill(self, spec: SkillSpec) -> str:
        """
        產生 Skill
        
        Args:
            spec: Skill 規格
            
        Returns:
            產生的 Skill 路徑
        """
        skill_dir = self.output_dir / spec.name
        skill_dir.mkdir(exist_ok=True)
        
        # 產生各檔案
        self._generate_init(skill_dir, spec)
        self._generate_schema(skill_dir, spec)
        self._generate_logic(skill_dir, spec)
        self._generate_test(skill_dir, spec)
        self._generate_skill_md(skill_dir, spec)
        
        return str(skill_dir)
    
    def _generate_init(self, skill_dir: Path, spec: SkillSpec):
        """產生 __init__.py"""
        output_class = self._to_camel(spec.name) + "Output"
        input_class = self._to_camel(spec.name) + "Input"
        
        template = self.TEMPLATES.get(spec.template, self.TEMPLATES["simple"])
        logic = spec.logic or template.format(
            inputs_str=", ".join(spec.inputs or ["df"]),
            output_class=output_class,
            description=spec.description,
            logic="score += 1  # 評分邏輯"
        )
        
        content = f'''"""
{spec.name} - {spec.description}

自動生成於 {spec.version}
'''

from dataclasses import dataclass
from typing import Any

{self._generate_imports(spec)}

/** Schema **/

@dataclass
class {input_class}:
    """{spec.name} 輸入"""
    df: Any = None
{self._generate_input_fields(spec)}


@dataclass
class {output_class}:
    """{spec.name} 輸出"""
    success: bool = False
    data: dict = None


/** 核心邏輯 **/

{logic}


/** Skill 類別 **/

class {self._to_pascal(spec.name)}:
    """
    {spec.name}
    
    {spec.description}
    
    設計原則：
    - 可獨立呼叫
    - 明確輸入輸出
    - 可測試
    """
    
    SKILL_NAME = "{spec.name}"
    SKILL_VERSION = "{spec.version}"
    
    def __init__(self):
        self.input_schema = {input_class}
        self.output_schema = {output_class}
    
    def execute(self, {", ".join(spec.inputs or ["df"])}) -> {output_class}:
        """
        執行 {spec.name}
        """
        # 呼叫邏輯
        return {output_class}(
            success=True,
            data={{}}
        )
'''
        
        (skill_dir / "__init__.py").write_text(content)
    
    def _generate_schema(self, skill_dir: Path, spec: SkillSpec):
        """產生 schema.py"""
        (skill_dir / "schema.py").write_text("# Schema definitions\n")
    
    def _generate_logic(self, skill_dir: Path, spec: SkillSpec):
        """產生 logic.py"""
        (skill_dir / "logic.py").write_text("# Logic implementations\n")
    
    def _generate_test(self, skill_dir: Path, spec: SkillSpec):
        """產生測試檔"""
        name = spec.name
        
        content = f'''"""
{name} 測試

測試 {spec.description}
"""

import pytest


def test_skill_basic():
    """基礎測試"""
    from .{self._to_pascal(spec.name)} import {self._to_pascal(spec.name)}
    
    skill = {self._to_pascal(spec.name)}()
    
    # 測試執行
    result = skill.execute()
    
    assert result is not None
    assert hasattr(result, 'success')


def test_skill_with_mock_data():
    """使用 Mock 資料測試"""
    from .{self._to_pascal(spec.name)} import {self._to_pascal(spec.name)}
    
    skill = {self._to_pascal(spec.name)}()
    
    # Mock df 資料
    import pandas as pd
    df = pd.DataFrame({{
        'Open': [100, 101, 102],
        'High': [105, 106, 107],
        'Low': [99, 100, 101],
        'Close': [102, 103, 104]
    }})
    
    result = skill.execute(df=df)
    
    assert result is not None
'''
        
        (skill_dir / "test_skill.py").write_text(content)
    
    def _generate_skill_md(self, skill_dir: Path, spec: SkillSpec):
        """產生 SKILL.md"""
        content = f'''# {spec.name}

> {spec.description}

## 設計原則

✅ 可獨立呼叫  
✅ 明確輸入輸出  
✅ 可測試  

## 使用方式

```python
from {self._to_pascal(spec.name)} import {self._to_pascal(spec.name)}

skill = {self._to_pascal(spec.name)}()
result = skill.execute()
```

## 版本

- **Version**: {spec.version}
'''
        
        (skill_dir / "SKILL.md").write_text(content)
    
    def _to_camel(self, name: str) -> str:
        """snake_case to CamelCase"""
        return ''.join(word.capitalize() for word in name.split('_'))
    
    def _to_pascal(self, name: str) -> str:
        """保持 PascalCase"""
        return self._to_camel(name)
    
    def _generate_imports(self, spec: SkillSpec) -> str:
        """產生 import 語句"""
        return "from dataclasses import dataclass\nfrom typing import Any"
    
    def _generate_input_fields(self, spec: SkillSpec) -> str:
        """產生輸入欄位"""
        fields = []
        for inp in (spec.inputs or ["df"]):
            fields.append(f"    {inp}: Any = None")
        return "\n".join(fields)


def generate_skill(name: str, description: str, **kwargs) -> str:
    """
    快速產生 Skill
    
    Args:
        name: Skill 名稱
        description: 描述
        **kwargs: 其他參數
        
    Returns:
        Skill 路徑
    """
    spec = SkillSpec(
        name=name,
        description=description,
        inputs=kwargs.get("inputs", ["df"]),
        outputs=kwargs.get("outputs", ["result"]),
        template=kwargs.get("template", "simple"),
        logic=kwargs.get("logic")
    )
    
    maker = SkillMaker()
    return maker.generate_skill(spec)


if __name__ == "__main__":
    # 範例：產生一個簡單的 Skill
    skill_path = generate_skill(
        name="price_momentum",
        description="價格動能指標",
        inputs=["df"],
        outputs=["signal"]
    )
    
    print(f"✅ Skill 已產生: {skill_path}")
