"""季度闭环工作单。

本模块只保存玩家和协作 AI 已提供的材料，不分析游戏、不替玩家下诏，
也不把计划自动升级为游戏事实。正式事实仍须以玩家提交的诏书和下季
朝政纪要为准。
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any


WORKFLOW_STAGES = (
    "收集上季反馈",
    "密谈中",
    "可行性核验",
    "政令草稿",
    "待玩家确认",
    "已下诏",
    "执行中",
    "待下季反馈",
    "已结案",
)
EDICT_SECTIONS = ("军事", "内政", "外交", "其他")


def _text(value: Any) -> str:
    return str(value or "").strip()


def _items(value: Any) -> list[str]:
    if isinstance(value, str):
        values = value.splitlines()
    elif isinstance(value, list):
        values = value
    else:
        values = []
    return [_text(item) for item in values if _text(item)]


def make_workflow_id(game_time: str) -> str:
    compact = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", game_time)[:24]
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"QW-{compact or '未标注'}-{stamp}"


def normalize_workflow(raw: dict[str, Any], existing: dict[str, Any] | None = None) -> dict[str, Any]:
    """标准化工作单；不派生任何游戏结果。"""
    if not isinstance(raw, dict):
        raise ValueError("季度工作单必须是对象。")
    existing = existing or {}
    game_time = _text(raw.get("游戏时间", existing.get("游戏时间", "")))
    if not game_time:
        raise ValueError("当前游戏时间不能为空，例如“崇祯十二年春”。")
    stage = _text(raw.get("状态", existing.get("状态", "收集上季反馈")))
    if stage not in WORKFLOW_STAGES:
        raise ValueError("季度工作单状态无效。")
    drafts_raw = raw.get("政令草稿", existing.get("政令草稿", {}))
    if not isinstance(drafts_raw, dict):
        drafts_raw = {}
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    workflow_id = _text(raw.get("工作单编号", existing.get("工作单编号", ""))) or make_workflow_id(game_time)
    return {
        "工作单编号": workflow_id,
        "游戏时间": game_time,
        "状态": stage,
        "上季反馈来源": _text(raw.get("上季反馈来源", existing.get("上季反馈来源", ""))),
        "本季主轴": _text(raw.get("本季主轴", existing.get("本季主轴", ""))),
        "本季问题": _text(raw.get("本季问题", existing.get("本季问题", ""))),
        "密谈大臣与问题": _text(raw.get("密谈大臣与问题", existing.get("密谈大臣与问题", ""))),
        "可行性核验": _text(raw.get("可行性核验", existing.get("可行性核验", ""))),
        "政令草稿": {
            section: _items(drafts_raw.get(section, [])) for section in EDICT_SECTIONS
        },
        "正式诏书标题": _text(raw.get("正式诏书标题", existing.get("正式诏书标题", ""))),
        "正式诏书正文": _text(raw.get("正式诏书正文", existing.get("正式诏书正文", ""))),
        "执行任务与验收": _text(raw.get("执行任务与验收", existing.get("执行任务与验收", ""))),
        "下季朝政纪要标题": _text(raw.get("下季朝政纪要标题", existing.get("下季朝政纪要标题", ""))),
        "下季朝政纪要原文": _text(raw.get("下季朝政纪要原文", existing.get("下季朝政纪要原文", ""))),
        "数据回填清单": _text(raw.get("数据回填清单", existing.get("数据回填清单", ""))),
        "玩家确认已下诏": bool(raw.get("玩家确认已下诏", existing.get("玩家确认已下诏", False))),
        "玩家确认已收到反馈": bool(raw.get("玩家确认已收到反馈", existing.get("玩家确认已收到反馈", False))),
        "创建时间": _text(existing.get("创建时间", "")) or now,
        "最后更新": now,
    }


def readiness(workflow: dict[str, Any]) -> list[str]:
    """给出缺失材料提示；提示不是对游戏事实的判断。"""
    missing: list[str] = []
    if not _text(workflow.get("上季反馈来源")):
        missing.append("补入上季朝政纪要或截图的来源路径。")
    if not _text(workflow.get("密谈大臣与问题")):
        missing.append("先记录密谈对象、问题、分歧和取舍。")
    if not _text(workflow.get("可行性核验")):
        missing.append("补入钱粮、人事、时限和风险的可行性核验。")
    if not any(workflow.get("政令草稿", {}).get(section) for section in EDICT_SECTIONS):
        missing.append("四板块政令草稿尚未填写。")
    if workflow.get("状态") in {"待玩家确认", "已下诏", "执行中", "待下季反馈", "已结案"}:
        if not _text(workflow.get("正式诏书标题")) or not _text(workflow.get("正式诏书正文")):
            missing.append("该状态需要保存正式诏书标题和正文。")
    if workflow.get("状态") in {"已下诏", "执行中", "待下季反馈", "已结案"} and not workflow.get("玩家确认已下诏"):
        missing.append("只有玩家实际提交后，才能勾选“玩家确认已下诏”。")
    if workflow.get("状态") == "已结案":
        if not workflow.get("玩家确认已收到反馈"):
            missing.append("结案前必须确认已收到下季游戏反馈。")
        if not _text(workflow.get("下季朝政纪要原文")):
            missing.append("结案前必须粘贴下季朝政纪要原文或填写其来源。")
        if not _text(workflow.get("数据回填清单")):
            missing.append("结案前必须填写数据回填清单，列出从纪要回填到哪些数据库和档案。")
    return missing


def _period_parts(game_time: str) -> tuple[str, str]:
    year = re.search(r"(天启|崇祯)[一二三四五六七八九十百零〇0-9]+年", game_time)
    season = re.search(r"(春|夏|秋|冬)", game_time)
    return (year.group(0) if year else "未标注年份", (season.group(0) + "季") if season else "未标注季节")


def workflow_markdown_path(archive_root: Path, game_time: str) -> Path:
    year, season = _period_parts(game_time)
    return archive_root / "01_季度政务" / "05_当前工作台" / year / season / "季度闭环工作单.md"


def render_workflow_markdown(workflow: dict[str, Any]) -> str:
    lines = [
        f"# {workflow['游戏时间']}季度闭环工作单",
        "",
        "> 本文件是工作材料的镜像：L1计划、L2诏书和L3游戏结果必须分开。未获玩家确认或未收到游戏反馈的内容，不构成当前事实。",
        "",
        f"- 工作单编号：`{workflow['工作单编号']}`",
        f"- 状态：{workflow['状态']}",
        f"- 创建时间：{workflow['创建时间']}",
        f"- 最后更新：{workflow['最后更新']}",
        "",
        "## 一、上季反馈（L3来源）",
        "",
        workflow["上季反馈来源"] or "（待补）",
        "",
        "## 二、密谈与可行性（L1）",
        "",
        f"### 本季主轴\n\n{workflow['本季主轴'] or '（待补）'}",
        f"\n### 本季问题\n\n{workflow['本季问题'] or '（待补）'}",
        f"\n### 密谈大臣、问题、分歧与取舍\n\n{workflow['密谈大臣与问题'] or '（待补）'}",
        f"\n### 可行性核验（钱粮、人事、时限、风险）\n\n{workflow['可行性核验'] or '（待补）'}",
        "",
        "## 三、四板块政令草稿（L1）",
        "",
    ]
    for section in EDICT_SECTIONS:
        lines.extend([f"### {section}", ""])
        values = workflow["政令草稿"].get(section, [])
        lines.extend([f"- {value}" for value in values] or ["（待补）"])
        lines.append("")
    lines.extend([
        "## 四、正式诏书（L2，须玩家确认已提交）",
        "",
        f"- 标题：{workflow['正式诏书标题'] or '（待补）'}",
        f"- 玩家确认已下诏：{'是' if workflow['玩家确认已下诏'] else '否'}",
        "",
        workflow["正式诏书正文"] or "（尚未形成或未获玩家确认）",
        "",
        "## 五、执行任务与验收（待反馈）",
        "",
        workflow["执行任务与验收"] or "（待补）",
        "",
        "## 六、下季朝政纪要与回填（L3/L4）",
        "",
        f"- 纪要标题：{workflow['下季朝政纪要标题'] or '（待补）'}",
        f"- 玩家确认已收到反馈：{'是' if workflow['玩家确认已收到反馈'] else '否'}",
        "",
        workflow["下季朝政纪要原文"] or "（尚未收到游戏反馈）",
        "",
        "### 数据回填清单",
        "",
        workflow["数据回填清单"] or "（待收到纪要后逐项填写）",
        "",
        "## 待补材料",
        "",
    ])
    lines.extend([f"- {item}" for item in readiness(workflow)] or ["- 工作单材料已按当前状态齐备；仍须以证据层级复核。"])
    return "\n".join(lines).rstrip() + "\n"


def write_workflow_markdown(archive_root: Path, workflow: dict[str, Any]) -> Path:
    path = workflow_markdown_path(archive_root, workflow["游戏时间"])
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".md.tmp")
    temporary.write_text(render_workflow_markdown(workflow), encoding="utf-8", newline="\n")
    temporary.replace(path)
    return path
