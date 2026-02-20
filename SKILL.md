# Skill Maker

*自動生成符合設計原則的 Agent Skills*

---

## 設計原則

✅ **原則 1：Skill 必須可獨立呼叫** - 每個 Skill 有獨立的 `execute()` 方法

✅ **原則 2：Skill 必須明確輸入輸出** - 使用 dataclass 定義 Schema

✅ **原則 3：Skill 必須可測試** - 內建測試案例

✅ **原則 4：避免過度細碎的 Skill** - 整合相關功能，減少 Skill 數量

---

## 快速開始

```python
from skill_maker import SkillMaker

maker = SkillMaker()

# 生成一個新 Skill
maker.generate_skill(
    name="my_custom_skill",
    description="自定義技能描述",
    inputs=["df", "params"],
    outputs=["result"],
    logic="""
    # 評分邏輯
    score = 0
    if df['Close'].iloc[-1] > df['Open'].iloc[-1]:
        score += 1
    return {"should_buy": score >= 1, "score": score}
    """
)
```

---

## 產生器命令列工具

```bash
# 產生新 Skill
python -m skill_maker generate --name my_skill --inputs df params --outputs result

# 產生測試檔案
python -m skill_maker test --skill my_skill

# 驗證 Skill 結構
python -m skill_maker validate --skill my_skill
```

---

## 產生器模板結構

```
skill-maker/
├── SKILL.md              # 本文件
├── skill_maker.py        # 核心產生器
├── cli.py               # 命令列工具
├── templates/
│   ├── skill.py.jinja2  # Skill 模板
│   ├── test.py.jinja2   # 測試模板
│   └── schema.py.jinja2 # Schema 模板
└── examples/
    ├── simple_skill.json
    └── trading_skill.json
```

---

## 內建模板

### 1. 基礎模板 (simple)
- 適合簡單的單一功能 Skill
- 輸入 → 處理 → 輸出

### 2. 評分模板 (scoring)
- 適合多指標加權評分
- 輸入 → 多指標計算 → 加權總分 → 決策

### 3. 狀態機模板 (state_machine)
- 適合有狀態轉換的 Skill
- 狀態檢查 → 狀態轉換 → 輸出新狀態

### 4. 交易模板 (trading)
- 適合量化交易相關 Skill
- 整合風控、部位、訊號

---

## 產生的 Skill 結構

每個產生的 Skill 包含：

```
my_skill/
├── __init__.py          # Skill 主類別
├── schema.py            # 輸入輸出 Schema
├── logic.py            # 核心邏輯
├── test_skill.py       # 測試案例
└── SKILL.md            # 說明文件
```

---

## 設計原則檢查

產生器會自動驗證：

1. ✅ `execute()` 方法存在
2. ✅ `Input` / `Output` Schema 定義
3. ✅ `test_skill.py` 存在
4. ✅ Skill 功能整合（不小於 50 行邏輯）

---

## 版本資訊

- **Version**: 1.0.0
- **Date**: 2026-02-20
