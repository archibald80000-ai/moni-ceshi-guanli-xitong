"""JSON 数据存取层。

本模块只负责本地档案读写，不连接网络，也不执行任何游戏操作。
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_DATA: dict[str, Any] = {
    "history_records.json": [],
    "personnel.json": [],
    "edicts.json": [],
    "strategy.json": [],
    "personal_notes.json": [],
    "quarterly_workflows.json": [],
    "game_state.json": {
        "阶层": [],
        "田税": [],
        "海军": [],
        "船种": [],
        "党派": [],
        "势力": [],
        "地块": [],
    },
    "intelligence.json": {
        "辽东": [],
        "陕西": [],
        "流民": [],
        "财政": [],
        "朝堂": [],
        "外交": [],
    },
}


class JSONDatabase:
    """使用多个 JSON 文件保存政务档案。"""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parent.parent
        self.data_dir = Path(data_dir) if data_dir else project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.ensure_files()

    def ensure_files(self) -> None:
        """补齐缺少的数据文件，但绝不覆盖已有存档。"""
        for filename, default_value in DEFAULT_DATA.items():
            path = self.data_dir / filename
            if not path.exists():
                self._write_json(path, deepcopy(default_value))

    def _path(self, filename: str) -> Path:
        if filename not in DEFAULT_DATA:
            raise ValueError(f"不支持的数据文件：{filename}")
        return self.data_dir / filename

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        """先写临时文件再替换，减少写入中断造成的存档损坏。"""
        temporary_path = path.with_suffix(path.suffix + ".tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temporary_path.replace(path)

    def load(self, filename: str) -> Any:
        path = self._path(filename)
        try:
            with path.open("r", encoding="utf-8-sig") as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path.name} 格式损坏：{error}") from error

    def save(self, filename: str, data: Any) -> None:
        self._write_json(self._path(filename), data)

    def append(self, filename: str, record: dict[str, Any]) -> None:
        records = self.load(filename)
        if not isinstance(records, list):
            raise ValueError(f"{filename} 不是列表型档案，不能直接追加。")
        records.append(record)
        self.save(filename, records)

    def add_person(self, person: dict[str, Any]) -> None:
        name = str(person.get("姓名", "")).strip()
        if not name:
            raise ValueError("姓名不能为空。")

        people = self.load("personnel.json")
        if any(item.get("姓名") == name for item in people):
            raise ValueError(f"人物“{name}”已存在，请使用修改功能。")

        normalized = {
            "姓名": name,
            "身份": str(person.get("身份", "")).strip(),
            "派系": str(person.get("派系", "")).strip(),
            "职位": str(person.get("职位", "")).strip(),
            "影响力": str(person.get("影响力", "")).strip(),
            "能力": str(person.get("能力", "")).strip(),
            "政治倾向": str(person.get("政治倾向", "")).strip(),
            "当前状态": str(person.get("当前状态", "")).strip(),
            "与皇帝关系": str(person.get("与皇帝关系", "")).strip(),
            "风险": str(person.get("风险", "")).strip(),
            "简介": str(person.get("简介", "")).strip(),
            "历史事件": person.get("历史事件", []),
        }
        people.append(normalized)
        self.save("personnel.json", people)

    def update_person(self, name: str, updates: dict[str, Any]) -> bool:
        people = self.load("personnel.json")
        for person in people:
            if person.get("姓名") == name:
                for key, value in updates.items():
                    if key in person and key != "姓名":
                        person[key] = value
                self.save("personnel.json", people)
                return True
        return False

    def query_people(self, keyword: str = "") -> list[dict[str, Any]]:
        people = self.load("personnel.json")
        keyword = keyword.strip().lower()
        if not keyword:
            return people

        matches: list[dict[str, Any]] = []
        for person in people:
            searchable = json.dumps(person, ensure_ascii=False).lower()
            if keyword in searchable:
                matches.append(person)
        return matches

    def add_intelligence(self, category: str, item: dict[str, Any]) -> None:
        intelligence = self.load("intelligence.json")
        # 兼容早期版本把分类对象包在单元素列表中的结构；首次写入时归一化。
        if isinstance(intelligence, list):
            normalized: dict[str, list[Any]] = {}
            for group in intelligence:
                if not isinstance(group, dict):
                    continue
                for group_category, values in group.items():
                    if isinstance(values, list):
                        normalized.setdefault(group_category, []).extend(values)
            intelligence = normalized
        if not isinstance(intelligence, dict):
            raise ValueError("intelligence.json 必须是分类对象或兼容列表。")
        if category not in intelligence:
            intelligence[category] = []
        intelligence[category].append(
            {
                "来源": str(item.get("来源", "")).strip(),
                "时间": str(item.get("时间", "")).strip(),
                "内容": str(item.get("内容", "")).strip(),
                "重要等级": str(item.get("重要等级", "")).strip(),
            }
        )
        self.save("intelligence.json", intelligence)

    def snapshot(self) -> dict[str, Any]:
        """返回全部档案快照，供分析和 Markdown 导出使用。"""
        return {
            filename.removesuffix(".json"): self.load(filename)
            for filename in DEFAULT_DATA
        }
