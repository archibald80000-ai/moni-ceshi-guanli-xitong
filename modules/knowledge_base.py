"""把 JSON 档案同步为便于阅读的 Markdown 知识库。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .database import JSONDatabase


KNOWLEDGE_SECTIONS = (
    "皇帝日志",
    "朝臣档案",
    "战争记录",
    "财政报告",
    "诏书全集",
    "国策路线",
    "国家态势",
    "参谋笔记",
    "资料索引",
    "AI分析报告",
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
    records = list(records)
    return f"## {title}\n\n" + _record_blocks(records, "名称")


class MarkdownKnowledgeBase:
    """将当前 JSON 数据快照导出为七类 Markdown 档案。"""

    def __init__(
        self,
        database: JSONDatabase,
        root_dir: str | Path | None = None,
    ) -> None:
        self.database = database
        project_root = Path(__file__).resolve().parent.parent
        self.root_dir = Path(root_dir) if root_dir else project_root / "大明档案"
        for section in KNOWLEDGE_SECTIONS:
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
        for section in KNOWLEDGE_SECTIONS:
            index_lines.append(f"- [{section}](./{section}/)")
        _write(self.root_dir / "README.md", "\n".join(index_lines))

        _write(
            self.root_dir / "皇帝日志" / "季度记录.md",
            "# 皇帝日志\n\n" + _record_blocks(history, "时间"),
        )
        _write(
            self.root_dir / "朝臣档案" / "朝臣总档.md",
            "# 朝臣档案\n\n" + _record_blocks(personnel, "姓名"),
        )

        war_records = _history_matches(
            history,
            ("战", "军", "兵", "辽东", "边防", "叛乱", "流寇", "建虏"),
        )
        war_text = "# 战争记录\n\n" + _record_blocks(war_records, "时间")
        if intelligence.get("辽东"):
            war_text += "\n\n## 辽东情报\n\n" + _record_blocks(
                intelligence["辽东"], "时间"
            )
        _write(self.root_dir / "战争记录" / "战争记录.md", war_text)

        fiscal_records = _history_matches(
            history,
            ("财", "税", "饷", "银", "粮", "仓", "赈", "户部"),
        )
        fiscal_text = "# 财政报告\n\n" + _record_blocks(fiscal_records, "时间")
        if intelligence.get("财政"):
            fiscal_text += "\n\n## 财政情报\n\n" + _record_blocks(
                intelligence["财政"], "时间"
            )
        _write(self.root_dir / "财政报告" / "财政报告.md", fiscal_text)

        _write(
            self.root_dir / "诏书全集" / "诏书全集.md",
            "# 诏书全集\n\n" + _record_blocks(edicts, "诏书标题"),
        )
        _write(
            self.root_dir / "国策路线" / "国策路线.md",
            "# 国策路线\n\n" + _record_blocks(strategy, "目标"),
        )
        state_text = "# 国家态势\n\n"
        state_text += "\n\n".join(
            _table_section(section, game_state.get(section, []))
            for section in ("阶层", "田税", "海军", "船种", "党派", "势力", "地块")
        )
        _write(self.root_dir / "国家态势" / "国家态势总览.md", state_text)
        _write(
            self.root_dir / "参谋笔记" / "个人战略笔记.md",
            "# 参谋笔记\n\n" + _record_blocks(personal_notes, "标题"),
        )
        return self.root_dir

    def save_analysis_report(self, report: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.root_dir / "AI分析报告" / f"局势分析_{timestamp}.md"
        _write(path, "# AI辅助分析报告\n\n" + report)
        return path
