"""把 JSON 档案同步为便于阅读的 Markdown 知识库。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .database import JSONDatabase


ARCHIVE_ROOT_SECTIONS = (
    "00_总览",
    "01_季度政务",
    "02_国家档案",
    "03_国策与战略",
    "04_辅助资料",
    "99_原始资料",
)


def _display(value: Any) -> str:
    if value in (None, "", []):
        return "（未记录）"
    if isinstance(value, list):
        return "；".join(str(item) for item in value) or "（未记录）"
    return str(value)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(text.rstrip() + "\n")


def _record_blocks(records: Iterable[dict[str, Any]], title_field: str) -> str:
    blocks: list[str] = []
    for index, record in enumerate(records, start=1):
        title = _display(record.get(title_field))
        lines = [f"## {index}. {title}", ""]
        for key, value in record.items():
            lines.append(f"- {key}：{_display(value)}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) if blocks else "（暂无记录）"


def _history_matches(
    records: Iterable[dict[str, Any]], keywords: tuple[str, ...]
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for record in records:
        searchable = " ".join(str(value) for value in record.values())
        if any(keyword in searchable for keyword in keywords):
            matches.append(record)
    return matches


def _table_section(title: str, records: Iterable[dict[str, Any]]) -> str:
    if isinstance(records, dict):
        normalized = [
            {"名称": key, "数值": value} for key, value in records.items()
        ]
    else:
        normalized = [record for record in records if isinstance(record, dict)]
    return f"## {title}\n\n" + _record_blocks(normalized, "名称")


def _intelligence_section(source: Any, section: str) -> list[dict[str, Any]]:
    """兼容旧分类对象和后续追加的扁平情报数组。"""
    collected: list[dict[str, Any]] = []
    if isinstance(source, dict):
        nested = source.get(section, [])
        if isinstance(nested, list):
            collected.extend(item for item in nested if isinstance(item, dict))
        return collected

    if not isinstance(source, list):
        return collected

    for record in source:
        if not isinstance(record, dict):
            continue
        nested = record.get(section)
        if isinstance(nested, list):
            collected.extend(item for item in nested if isinstance(item, dict))
            continue
        labels = (record.get("分类"), record.get("地区"), record.get("区域"))
        if any(section == str(label) for label in labels if label):
            collected.append(record)
    return collected


class MarkdownKnowledgeBase:
    """按六个一级入口将 JSON 快照导出为 Markdown 阅读稿。"""

    def __init__(
        self,
        database: JSONDatabase,
        root_dir: str | Path | None = None,
    ) -> None:
        self.database = database
        project_root = Path(__file__).resolve().parent.parent
        self.root_dir = Path(root_dir) if root_dir else project_root / "大明档案"
        for section in ARCHIVE_ROOT_SECTIONS:
            (self.root_dir / section).mkdir(parents=True, exist_ok=True)

    def sync_all(self) -> Path:
        snapshot = self.database.snapshot()
        history = snapshot["history_records"]
        personnel = snapshot["personnel"]
        edicts = snapshot["edicts"]
        strategy = snapshot["strategy"]
        game_state = snapshot["game_state"]
        personal_notes = snapshot["personal_notes"]
        intelligence = snapshot["intelligence"]

        index_lines = [
            "# 大明档案",
            "",
            "本目录由本地 JSON 存档同步生成，便于玩家阅读与长期整理。",
            "JSON 文件仍是结构化数据源；请在程序中修改后重新同步。",
            "",
        ]
        for section in ARCHIVE_ROOT_SECTIONS:
            index_lines.append(f"- [{section}](./{section}/)")
        # 根目录 README 是人工维护的档案入口，已有时不得被同步器覆盖。
        readme_path = self.root_dir / "README.md"
        if not readme_path.exists():
            _write(readme_path, "\n".join(index_lines))

        _write(
            self.root_dir / "01_季度政务" / "季度记录汇总（系统生成）.md",
            "# 季度记录汇总（系统生成）\n\n" + _record_blocks(history, "时间"),
        )
        _write(
            self.root_dir / "02_国家档案" / "01_朝臣" / "朝臣总档.md",
            "# 朝臣档案\n\n" + _record_blocks(personnel, "姓名"),
        )

        war_records = _history_matches(
            history,
            ("战", "军", "兵", "辽东", "边防", "叛乱", "流寇", "建虏"),
        )
        war_text = "# 战争记录\n\n" + _record_blocks(war_records, "时间")
        liaodong_intelligence = _intelligence_section(intelligence, "辽东")
        if liaodong_intelligence:
            war_text += "\n\n## 辽东情报\n\n" + _record_blocks(
                liaodong_intelligence, "时间"
            )
        _write(
            self.root_dir / "02_国家档案" / "05_战争" / "战争记录.md",
            war_text,
        )

        fiscal_records = _history_matches(
            history,
            ("财", "税", "饷", "银", "粮", "仓", "赈", "户部"),
        )
        fiscal_text = "# 财政报告\n\n" + _record_blocks(fiscal_records, "时间")
        fiscal_intelligence = _intelligence_section(intelligence, "财政")
        if fiscal_intelligence:
            fiscal_text += "\n\n## 财政情报\n\n" + _record_blocks(
                fiscal_intelligence, "时间"
            )
        _write(
            self.root_dir / "02_国家档案" / "04_财政" / "财政报告.md",
            fiscal_text,
        )

        _write(
            self.root_dir / "01_季度政务" / "02_诏书" / "诏书全集.md",
            "# 诏书全集\n\n" + _record_blocks(edicts, "诏书标题"),
        )
        _write(
            self.root_dir
            / "03_国策与战略"
            / "90_历史策略镜像"
            / "国策路线.md",
            "# 国策路线（历史兼容镜像）\n\n> 本文件由旧 data/strategy.json 同步生成，混合保存历史计划、季度建议与执行记录，不是当前长期国策清单。当前长期制度请读取 `大明档案/03_国策与战略/01_制度规则/关键制度源头/01_长期国策有效清单.md`。\n\n"
            + _record_blocks(strategy, "目标"),
        )
        state_text = "# 国家态势\n\n"
        state_text += "\n\n".join(
            _table_section(section, game_state.get(section, []))
            for section in ("阶层", "田税", "海军", "船种", "党派", "势力", "地块")
        )
        _write(
            self.root_dir / "02_国家档案" / "03_国家态势" / "国家态势总览.md",
            state_text,
        )
        _write(
            self.root_dir / "03_国策与战略" / "05_玩家笔记" / "个人战略笔记.md",
            "# 参谋笔记\n\n" + _record_blocks(personal_notes, "标题"),
        )
        return self.root_dir

    def save_analysis_report(self, report: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = (
            self.root_dir
            / "04_辅助资料"
            / "AI分析报告"
            / f"局势分析_{timestamp}.md"
        )
        _write(path, "# AI辅助分析报告\n\n" + report)
        return path
