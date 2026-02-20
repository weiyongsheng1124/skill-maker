#!/usr/bin/env python3
"""
Skill Maker CLI - 命令列工具

用法：
    python cli.py generate --name my_skill --description "我的技能"
    python cli.py list
    python cli.py validate --skill my_skill
"""

import argparse
import sys
from pathlib import Path

from skill_maker import SkillMaker, generate_skill


def main():
    parser = argparse.ArgumentParser(description="Skill Maker - 產生 Agent Skills")
    subparsers = parser.add_subparsers(dest="command", help="可用指令")
    
    # generate 指令
    gen_parser = subparsers.add_parser("generate", help="產生新 Skill")
    gen_parser.add_argument("--name", required=True, help="Skill 名稱")
    gen_parser.add_argument("--description", required=True, help="Skill 描述")
    gen_parser.add_argument("--inputs", nargs="+", default=["df"], help="輸入參數")
    gen_parser.add_argument("--outputs", nargs="+", default=["result"], help="輸出參數")
    gen_parser.add_argument("--template", choices=["simple", "scoring", "trading"], 
                           default="simple", help="使用的模板")
    
    # list 指令
    subparsers.add_parser("list", help="列出已產生的 Skills")
    
    # validate 指令
    val_parser = subparsers.add_parser("validate", help="驗證 Skill")
    val_parser.add_argument("--skill", required=True, help="Skill 名稱")
    
    # test 指令
    test_parser = subparsers.add_parser("test", help="執行測試")
    test_parser.add_argument("--skill", required=True, help="Skill 名稱")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        skill_path = generate_skill(
            name=args.name,
            description=args.description,
            inputs=args.inputs,
            outputs=args.outputs,
            template=args.template
        )
        print(f"✅ Skill 已產生: {skill_path}")
    
    elif args.command == "list":
        maker = SkillMaker()
        skills = list(maker.output_dir.iterdir())
        if skills:
            print("📦 已產生的 Skills:")
            for skill in skills:
                print(f"  - {skill.name}")
        else:
            print("尚無產生的 Skills")
    
    elif args.command == "validate":
        maker = SkillMaker()
        skill_path = maker.output_dir / args.skill
        
        if not skill_path.exists():
            print(f"❌ Skill 不存在: {skill_path}")
            sys.exit(1)
        
        # 驗證原則
        checks = []
        
        # 原則 1: 有 __init__.py
        checks.append(("__init__.py", (skill_path / "__init__.py").exists()))
        
        # 原則 2: 有 schema
        checks.append(("schema.py", (skill_path / "schema.py").exists()))
        
        # 原則 3: 有測試
        checks.append(("test_skill.py", (skill_path / "test_skill.py").exists()))
        
        # 原則 4: 有足夠邏輯
        init_content = (skill_path / "__init__.py").read_text()
        checks.append(("邏輯代碼", len(init_content) > 200))
        
        print(f"🔍 驗證 {args.skill}:")
        all_passed = True
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✅ 所有原則檢查通過!")
        else:
            print("\n❌ 部分檢查未通過")
            sys.exit(1)
    
    elif args.command == "test":
        maker = SkillMaker()
        skill_path = maker.output_dir / args.skill
        
        if not (skill_path / "test_skill.py").exists():
            print(f"❌ 測試檔案不存在: {skill_path / 'test_skill.py'}")
            sys.exit(1)
        
        print(f"🧪 執行測試: {args.skill}")
        # 執行測試
        import subprocess
        result = subprocess.run(
            ["python", "-m", "pytest", str(skill_path / "test_skill.py"), "-v"],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        sys.exit(result.returncode)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
