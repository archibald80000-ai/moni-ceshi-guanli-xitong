"""崇祯皇帝私人政务档案管理系统（命令行版）。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from modules.ai_analysis import generate_analysis_report
from modules.database import JSONDatabase
from modules.edict_helper import generate_edict
from modules.knowledge_base import MarkdownKnowledgeBase
from modules.turn_manager import create_quarter_record, enrich_record


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = {
    "markdown_knowledge_base": True,
    "knowledge_base_directory": "大明档案",
    "analysis_recent_turns": 6,
}


def load_config() -> dict[str, Any]:
    """读取可选的 config.json；不存在时使用开箱即用的默认设置。"""
    config = dict(DEFAULT_CONFIG)
    config_path = PROJECT_ROOT / "config" / "config.json"
    if config_path.exists():
        try:
            user_config = json.loads(config_path.read_text(encoding="utf-8-sig"))
            if isinstance(user_config, dict):
                config.update(user_config)
        except (json.JSONDecodeError, OSError) as error:
            print(f"配置文件读取失败，已使用默认设置：{error}")
    return config


class ChongzhenArchiveApp:
    """负责命令行交互，不包含自动决策或游戏操作。"""

    def __init__(self) -> None:
        self.config = load_config()
        self.database = JSONDatabase(PROJECT_ROOT / "data")
        knowledge_dir = PROJECT_ROOT / str(
            self.config.get("knowledge_base_directory", "大明档案")
        )
        self.knowledge_base = MarkdownKnowledgeBase(self.database, knowledge_dir)
        if self.config.get("markdown_knowledge_base", True):
            self.knowledge_base.sync_all()

    @staticmethod
    def pause() -> None:
        input("\n按回车键返回……")

    @staticmethod
    def print_records(records: list[dict[str, Any]]) -> None:
        if not records:
            print("暂无记录。")
            return
        for index, record in enumerate(records, start=1):
            print(f"\n[{index}]")
            for key, value in record.items():
                shown = "、".join(map(str, value)) if isinstance(value, list) else value
                print(f"{key}：{shown or '（未记录）'}")

    def sync_markdown(self, announce: bool = False) -> None:
        if not self.config.get("markdown_knowledge_base", True):
            return
        root = self.knowledge_base.sync_all()
        if announce:
            print(f"Markdown 知识库已同步：{root}")

    def add_quarter_record(self) -> None:
        print("\n=== 添加季度记录 ===")
        current_date = input("当前日期（如 崇祯元年春）：")
        turn = input("回合编号（可留空）：")
        situation = input("游戏情况：")
        major_event = input("重大事件：")
        record = create_quarter_record(current_date, situation, major_event, turn)

        if input("现在补充决策与结果字段？(y/N)：").strip().lower() == "y":
            record = enrich_record(
                record,
                皇帝状态=input("当前皇帝状态："),
                皇帝决策=input("皇帝决策："),
                玩家决策=input("玩家决策（可与皇帝决策相同）："),
                诏书内容=input("相关诏书内容："),
                执行结果=input("当前执行结果："),
                后续结果=input("后续结果："),
                影响评价=input("影响评价："),
            )

        self.database.append("history_records.json", record)
        self.sync_markdown()
        print("季度档案已保存。")

    def update_quarter_record(self) -> None:
        records = self.database.load("history_records.json")
        self.print_records(records)
        if not records:
            return
        try:
            index = int(input("\n要更新的记录序号：")) - 1
            if index < 0:
                raise IndexError
            record = records[index]
        except (ValueError, IndexError):
            print("序号无效。")
            return

        editable = [
            "皇帝状态",
            "天下局势",
            "事件",
            "背景",
            "朝廷事件",
            "皇帝决策",
            "玩家决策",
            "诏书内容",
            "执行结果",
            "后续结果",
            "影响评价",
        ]
        print("可修改字段：" + "、".join(editable))
        field = input("字段名：").strip()
        if field not in editable:
            print("字段名无效。")
            return
        record[field] = input("新内容：").strip()
        self.database.save("history_records.json", records)
        self.sync_markdown()
        print("季度档案已更新。")

    def archive_menu(self) -> None:
        while True:
            print(
                "\n=== 国家档案 ===\n"
                "1. 查看季度记录\n"
                "2. 更新季度记录\n"
                "3. 查看诏书档案\n"
                "4. 查看关键情报\n"
                "5. 添加关键情报\n"
                "6. 同步 Markdown 知识库\n"
                "0. 返回"
            )
            choice = input("请选择：").strip()
            if choice == "1":
                self.print_records(self.database.load("history_records.json"))
                self.pause()
            elif choice == "2":
                self.update_quarter_record()
                self.pause()
            elif choice == "3":
                self.print_records(self.database.load("edicts.json"))
                self.pause()
            elif choice == "4":
                intelligence = self.database.load("intelligence.json")
                for category, items in intelligence.items():
                    print(f"\n【{category}】")
                    self.print_records(items)
                self.pause()
            elif choice == "5":
                self.add_intelligence()
                self.pause()
            elif choice == "6":
                self.sync_markdown(announce=True)
                self.pause()
            elif choice == "0":
                return
            else:
                print("无效选项。")

    def add_intelligence(self) -> None:
        intelligence = self.database.load("intelligence.json")
        print("现有分类：" + "、".join(intelligence))
        category = input("分类（可输入新分类）：").strip()
        content = input("情报内容：").strip()
        if not category or not content:
            print("分类和内容不能为空。")
            return
        item = {
            "来源": input("来源："),
            "时间": input("时间："),
            "内容": content,
            "重要等级": input("重要等级（低/中/高/紧急）："),
        }
        self.database.add_intelligence(category, item)
        self.sync_markdown()
        print("情报已保存。")

    def personnel_menu(self) -> None:
        while True:
            print(
                "\n=== 官员档案 ===\n"
                "1. 查看全部\n"
                "2. 查询人物\n"
                "3. 新增人物\n"
                "4. 修改人物\n"
                "0. 返回"
            )
            choice = input("请选择：").strip()
            if choice == "1":
                self.print_records(self.database.query_people())
                self.pause()
            elif choice == "2":
                keyword = input("输入姓名、职位、派系或其他关键词：")
                self.print_records(self.database.query_people(keyword))
                self.pause()
            elif choice == "3":
                self.add_person()
                self.pause()
            elif choice == "4":
                self.edit_person()
                self.pause()
            elif choice == "0":
                return
            else:
                print("无效选项。")

    def add_person(self) -> None:
        print("\n=== 新增人物 ===")
        fields = [
            "姓名",
            "身份",
            "派系",
            "职位",
            "影响力",
            "能力",
            "政治倾向",
            "当前状态",
            "与皇帝关系",
            "风险",
            "简介",
        ]
        person = {field: input(f"{field}：") for field in fields}
        history_event = input("历史事件（可留空）：").strip()
        person["历史事件"] = [history_event] if history_event else []
        try:
            self.database.add_person(person)
        except ValueError as error:
            print(error)
            return
        self.sync_markdown()
        print("人物档案已保存。")

    def edit_person(self) -> None:
        name = input("要修改的人物姓名：").strip()
        matches = self.database.query_people(name)
        exact = next((item for item in matches if item.get("姓名") == name), None)
        if exact is None:
            print("未找到该人物。")
            return
        self.print_records([exact])
        editable = [key for key in exact if key != "姓名"]
        print("可修改字段：" + "、".join(editable))
        field = input("字段名：").strip()
        if field not in editable:
            print("字段名无效。")
            return
        if field == "历史事件":
            events = list(exact.get("历史事件", []))
            new_event = input("追加历史事件：").strip()
            if not new_event:
                print("内容不能为空。")
                return
            events.append(new_event)
            value: Any = events
        else:
            value = input("新内容：").strip()
        self.database.update_person(name, {field: value})
        self.sync_markdown()
        print("人物档案已更新。")

    def add_edict(self, body: str = "", target: str = "") -> None:
        print("\n=== 添加诏书档案 ===")
        record = {
            "时间": input("时间：").strip(),
            "诏书标题": input("诏书标题：").strip(),
            "正文": body or input("正文：").strip(),
            "执行人": input("执行人：").strip(),
            "目标": target or input("目标：").strip(),
            "结果": input("结果（尚未执行可留空）：").strip(),
        }
        if not record["诏书标题"] or not record["正文"]:
            print("诏书标题和正文不能为空，未保存。")
            return
        self.database.append("edicts.json", record)
        self.sync_markdown()
        print("诏书档案已保存。此操作仅保存文字，不会执行游戏政策。")

    def strategy_menu(self) -> None:
        while True:
            print(
                "\n=== 长期计划 ===\n"
                "1. 查看计划\n"
                "2. 新增计划\n"
                "3. 更新状态\n"
                "0. 返回"
            )
            choice = input("请选择：").strip()
            if choice == "1":
                self.print_records(self.database.load("strategy.json"))
                self.pause()
            elif choice == "2":
                self.add_strategy()
                self.pause()
            elif choice == "3":
                self.update_strategy()
                self.pause()
            elif choice == "0":
                return
            else:
                print("无效选项。")

    def add_strategy(self) -> None:
        goal = input("长期目标：").strip()
        measures = [
            item.strip()
            for item in input("措施（多项用逗号分隔）：").replace("，", ",").split(",")
            if item.strip()
        ]
        record = {
            "目标": goal,
            "阶段": input("阶段（如 1-6 回合）：").strip(),
            "措施": measures,
            "状态": input("状态（未开始/执行中/完成）：").strip() or "未开始",
            "进展记录": [],
        }
        if not record["目标"]:
            print("长期目标不能为空。")
            return
        self.database.append("strategy.json", record)
        self.sync_markdown()
        print("长期计划已保存。")

    def update_strategy(self) -> None:
        records = self.database.load("strategy.json")
        self.print_records(records)
        if not records:
            return
        try:
            index = int(input("\n计划序号：")) - 1
            if index < 0:
                raise IndexError
            record = records[index]
        except (ValueError, IndexError):
            print("序号无效。")
            return
        status = input("新状态（未开始/执行中/完成）：").strip()
        if status not in ("未开始", "执行中", "完成"):
            print("状态无效。")
            return
        progress = input("本次进展记录（可留空）：").strip()
        record["状态"] = status
        if progress:
            record.setdefault("进展记录", []).append(progress)
        self.database.save("strategy.json", records)
        self.sync_markdown()
        print("长期计划已更新。")

    def analyze(self) -> None:
        recent_turns = int(self.config.get("analysis_recent_turns", 6))
        report = generate_analysis_report(self.database, recent_turns)
        print("\n" + report)
        if self.config.get("markdown_knowledge_base", True):
            path = self.knowledge_base.save_analysis_report(report)
            print(f"\n报告已保存：{path}")

    def create_edict_draft(self) -> None:
        print("\n=== 生成诏书草稿 ===")
        goal = input("政策目标：")
        target = input("对象：")
        purpose = input("目的：")
        try:
            draft = generate_edict(goal, target, purpose)
        except ValueError as error:
            print(error)
            return
        print("\n--- 诏书草稿 ---\n")
        print(draft)
        print("\n此内容仅为可编辑草稿，不会自动执行。")
        if input("是否将草稿收入诏书档案？(y/N)：").strip().lower() == "y":
            self.add_edict(body=draft, target=target)

    def run(self) -> None:
        while True:
            print(
                "\n====================================\n"
                " 崇祯皇帝私人政务档案管理系统\n"
                "====================================\n"
                "1. 添加季度记录\n"
                "2. 查看国家档案\n"
                "3. 查看官员\n"
                "4. 添加诏书\n"
                "5. 查看长期计划\n"
                "6. AI分析当前局势\n"
                "7. 生成诏书\n"
                "0. 退出"
            )
            choice = input("请选择：").strip()
            try:
                if choice == "1":
                    self.add_quarter_record()
                    self.pause()
                elif choice == "2":
                    self.archive_menu()
                elif choice == "3":
                    self.personnel_menu()
                elif choice == "4":
                    self.add_edict()
                    self.pause()
                elif choice == "5":
                    self.strategy_menu()
                elif choice == "6":
                    self.analyze()
                    self.pause()
                elif choice == "7":
                    self.create_edict_draft()
                    self.pause()
                elif choice == "0":
                    print("档案已妥善保存。")
                    return
                else:
                    print("无效选项，请重新选择。")
            except ValueError as error:
                print(f"操作未完成：{error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="崇祯模拟器辅助管理系统")
    parser.add_argument(
        "--check",
        action="store_true",
        help="检查数据文件和 Markdown 知识库后退出",
    )
    args = parser.parse_args()

    app = ChongzhenArchiveApp()
    if args.check:
        print("启动检查通过。")
        print(f"数据目录：{app.database.data_dir}")
        print(f"Markdown 知识库：{app.knowledge_base.root_dir}")
        return
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        print("\n程序已安全退出，现有档案未被删除。")


if __name__ == "__main__":
    main()
