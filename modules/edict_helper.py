"""明代风格诏书文字辅助模块。"""

from __future__ import annotations


def generate_edict(policy_goal: str, target: str, purpose: str) -> str:
    """生成简洁、可复制的诏书草稿。

    本函数只生成文字，不会保存、发布或执行任何政策。
    """
    policy_goal = policy_goal.strip()
    target = target.strip()
    purpose = purpose.strip()
    if not all((policy_goal, target, purpose)):
        raise ValueError("政策目标、对象和目的均不能为空。")

    return (
        "奉天承运皇帝，诏曰：\n\n"
        f"今为{purpose}，特命{target}负责{policy_goal}。"
        "所司当审慎办理，按期具奏，不得因循怠忽。\n\n"
        "钦此。"
    )

