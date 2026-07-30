"""基于本地档案的规则型辅助分析。

这里的“AI分析”不调用外部服务，也不自动做决定；它只从已有记录中
提取证据、提示缺口，并给出供玩家审阅的优先事项。
"""

from __future__ import annotations

from typing import Any, Iterable

from .database import JSONDatabase


FIELDS_FOR_CONTEXT = (
    "时间",
    "天下局势",
    "事件",
    "背景",
    "朝廷事件",
    "执行结果",
    "后续结果",
    "影响评价",
)


def _shorten(text: str, limit: int = 90) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _relevant_history(
    records: Iterable[dict[str, Any]], keywords: tuple[str, ...]
) -> list[str]:
    results: list[str] = []
    for record in records:
        context = "；".join(
            str(record.get(field, "")).strip()
            for field in FIELDS_FOR_CONTEXT
            if record.get(field)
        )
        if any(keyword in context for keyword in keywords):
            results.append(_shorten(context))
    return results[-2:]


def _relevant_intelligence(
    intelligence: dict[str, list[dict[str, Any]]],
    categories: tuple[str, ...],
) -> list[str]:
    results: list[str] = []
    for category in categories:
        for item in intelligence.get(category, [])[-2:]:
            time = item.get("时间") or "时间未记"
            level = item.get("重要等级") or "等级未记"
            content = item.get("内容") or "内容未记"
            results.append(f"{category}｜{time}｜{level}：{_shorten(str(content))}")
    return results[-3:]


def _section_summary(history_notes: list[str], intelligence_notes: list[str]) -> str:
    evidence = history_notes + intelligence_notes
    if not evidence:
        return "现有档案不足，暂不能形成可靠判断。"
    return "\n".join(f"- {item}" for item in evidence)


def generate_analysis_report(
    database: JSONDatabase,
    recent_turns: int = 6,
) -> str:
    """生成当前局势、长期目标、风险和建议四部分报告。"""
    history = database.load("history_records.json")
    personnel = database.load("personnel.json")
    edicts = database.load("edicts.json")
    strategy = database.load("strategy.json")
    intelligence = database.load("intelligence.json")
    recent_history = history[-max(1, recent_turns) :]

    fiscal = _section_summary(
        _relevant_history(
            recent_history, ("财", "税", "银", "粮", "饷", "仓", "户部", "赈")
        ),
        _relevant_intelligence(intelligence, ("财政",)),
    )
    military = _section_summary(
        _relevant_history(
            recent_history, ("战", "军", "兵", "辽东", "陕西", "边防", "流寇", "建虏")
        ),
        _relevant_intelligence(intelligence, ("辽东", "陕西", "外交")),
    )
    livelihood = _section_summary(
        _relevant_history(
            recent_history, ("民", "灾", "荒", "疫", "赈", "流民", "粮价")
        ),
        _relevant_intelligence(intelligence, ("流民", "陕西")),
    )
    court = _section_summary(
        _relevant_history(
            recent_history, ("朝", "官", "党", "阁", "奏", "弹劾", "任免")
        ),
        _relevant_intelligence(intelligence, ("朝堂",)),
    )

    active_strategies = [
        item
        for item in strategy
        if item.get("状态", "未开始") in ("未开始", "执行中")
    ]
    if active_strategies:
        directions = "；".join(
            f"{item.get('目标', '未命名目标')}（{item.get('状态', '未开始')}）"
            for item in active_strategies
        )
        keep = "继续按档案中的阶段和措施核对进度，不因单回合波动自动改线。"
    else:
        directions = "尚未登记未完成的长期国策。"
        keep = "先明确一项可复核的长期目标、阶段和衡量标准。"

    completed = [
        item.get("目标", "未命名目标")
        for item in strategy
        if item.get("状态") == "完成"
    ]
    adjust = (
        "已完成目标可归档复盘：" + "、".join(completed[-3:])
        if completed
        else "对缺少进展记录的国策补充证据后，再由玩家决定是否调整。"
    )

    risks: list[str] = []
    for person in personnel:
        risk = str(person.get("风险", "")).strip()
        if risk:
            risks.append(f"人物：{person.get('姓名', '未记名')}—{risk}")
    for edict in edicts[-10:]:
        result = str(edict.get("结果", "")).strip()
        if any(word in result for word in ("失败", "受阻", "未执行", "无效", "延误")):
            risks.append(
                f"诏书：{edict.get('诏书标题', '未命名诏书')}—{_shorten(result)}"
            )
    high_intelligence: list[str] = []
    for category, items in intelligence.items():
        for item in items:
            level = str(item.get("重要等级", ""))
            if any(word in level for word in ("高", "紧急", "重大")):
                high_intelligence.append(
                    f"{category}：{_shorten(str(item.get('内容', '内容未记')))}"
                )
    risks.extend(high_intelligence[-5:])
    if not risks:
        risks.append("现有档案中未发现已明确标注的高风险项；这不代表风险不存在。")

    suggestions: list[str] = []
    if not history:
        suggestions.append("先补录最近一个季度，建立分析基线。")
    if not personnel:
        suggestions.append("补录当前关键官员的职位、能力、风险与状态。")
    empty_intelligence = [
        category for category, items in intelligence.items() if not items
    ]
    if empty_intelligence:
        suggestions.append(
            "优先补齐空白情报分类：" + "、".join(empty_intelligence) + "。"
        )
    if active_strategies:
        suggestions.append("为执行中的国策补记本回合进展与可观察结果。")
    if risks and "未发现" not in risks[0]:
        suggestions.append("先核实已标注风险的时效和来源，再由玩家决定处置顺序。")
    if not suggestions:
        suggestions.append("继续维护季度记录，并在执行结果出现后更新影响评价。")

    risk_text = "\n".join(f"- {item}" for item in risks[:8])
    suggestion_text = "\n".join(f"- {item}" for item in suggestions)
    return (
        "【当前局势】\n\n"
        f"财政：\n{fiscal}\n\n"
        f"军事：\n{military}\n\n"
        f"民生：\n{livelihood}\n\n"
        f"朝堂：\n{court}\n\n"
        "【长期目标】\n\n"
        f"当前战略方向：{directions}\n\n"
        f"需要坚持：{keep}\n\n"
        f"需要调整：{adjust}\n\n"
        "【风险提醒】\n\n"
        f"{risk_text}\n\n"
        "【建议】\n\n"
        f"{suggestion_text}\n\n"
        "说明：以上内容仅依据本地档案生成，供玩家参考；不会自动执行，"
        "最终决策由玩家作出。"
    )

