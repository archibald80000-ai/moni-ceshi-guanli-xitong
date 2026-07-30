"""季度回合记录助手。"""

from __future__ import annotations

from typing import Any


def create_quarter_record(
    current_date: str,
    game_situation: str,
    major_event: str,
    turn: str = "",
) -> dict[str, Any]:
    """根据用户提供的信息建立季度档案。

    未提供的决策和结果保持为空，避免系统自行编造游戏事实。
    """
    if not current_date.strip():
        raise ValueError("当前日期不能为空。")

    return {
        "时间": current_date.strip(),
        "回合": turn.strip(),
        "皇帝状态": "",
        "天下局势": game_situation.strip(),
        "事件": major_event.strip(),
        "背景": game_situation.strip(),
        "朝廷事件": major_event.strip(),
        "皇帝决策": "",
        "玩家决策": "",
        "诏书内容": "",
        "执行结果": "",
        "后续结果": "",
        "影响评价": "",
    }


def enrich_record(record: dict[str, Any], **updates: str) -> dict[str, Any]:
    """补充当前季度档案；只接受档案中已有字段。"""
    updated = dict(record)
    for key, value in updates.items():
        if key in updated:
            updated[key] = value.strip() if isinstance(value, str) else value
    return updated

