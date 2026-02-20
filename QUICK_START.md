# Skill Maker 快速開始

## 安裝

```bash
cd skill-maker
pip install -e .
```

## 使用方式

### 1. 命令列產生

```bash
# 產生簡單 Skill
python cli.py generate \
    --name price_ma \
    --description "均線交叉訊號" \
    --inputs df \
    --outputs signal

# 產生評分 Skill
python cli.py generate \
    --name multi_indicator_entry \
    --description "多指標進場評分" \
    --inputs df params \
    --outputs signal score \
    --template scoring

# 產生交易 Skill
python cli.py generate \
    --name trading_strategy \
    --description "完整交易策略" \
    --template trading
```

### 2. Python API 產生

```python
from skill_maker import generate_skill

# 簡單 Skill
skill_path = generate_skill(
    name="my_skill",
    description="我的自定義技能",
    inputs=["df", "params"],
    outputs=["result"],
    template="scoring",
    logic="""
    # 自訂評分邏輯
    score = 0
    if df['Close'].iloc[-1] > df['MA20'].iloc[-1]:
        score += 1
    if df['RSI'].iloc[-1] < 30:
        score += 1
    return score, ["價格高於MA20", "RSI超賣"]
    """
)

print(f"Skill 已產生: {skill_path}")
```

### 3. 驗證與測試

```bash
# 驗證 Skill
python cli.py validate --skill my_skill

# 執行測試
python cli.py test --skill my_skill

# 列出所有 Skills
python cli.py list
```

---

## 產生的 Skill 結構

```
generated_skills/
└── my_skill/
    ├── __init__.py       # Skill 主類別
    ├── schema.py         # 輸入輸出定義
    ├── logic.py          # 核心邏輯
    ├── test_skill.py     # 測試案例
    └── SKILL.md         # 說明文件
```

---

## 使用產生的 Skill

```python
from generated_skills.my_skill import MySkill

skill = MySkill()
result = skill.execute(df=df, params={})

if result.success:
    print(f"完成: {result.data}")
```

---

## 四個設計原則

| 原則 | 檢查項目 |
|------|----------|
| 1. 可獨立呼叫 | `execute()` 方法存在 |
| 2. 明確輸入輸出 | `Input` / `Output` Schema 定義 |
| 3. 可測試 | `test_skill.py` 存在 |
| 4. 不過度細碎 | 代碼量 > 200 字元 |
