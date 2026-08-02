from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from modules.quarterly_workflow import (
    EDICT_SECTIONS,
    normalize_workflow,
    readiness,
    render_workflow_markdown,
    workflow_markdown_path,
    write_workflow_markdown,
)


class QuarterlyWorkflowTests(unittest.TestCase):
    def test_normalizes_four_sections_and_keeps_plan_separate(self) -> None:
        workflow = normalize_workflow(
            {
                "游戏时间": "崇祯十二年春",
                "状态": "政令草稿",
                "政令草稿": {"军事": "核兵\n补给", "内政": ["赈济"]},
            }
        )
        self.assertTrue(workflow["工作单编号"].startswith("QW-崇祯十二年春-"))
        self.assertEqual(workflow["政令草稿"]["军事"], ["核兵", "补给"])
        self.assertEqual(workflow["政令草稿"]["内政"], ["赈济"])
        self.assertEqual(workflow["正式诏书正文"], "")
        self.assertFalse(workflow["玩家确认已下诏"])

    def test_requires_real_confirmation_for_post_order_states(self) -> None:
        workflow = normalize_workflow({"游戏时间": "崇祯十二年春", "状态": "已下诏"})
        messages = readiness(workflow)
        self.assertTrue(any("正式诏书" in message for message in messages))
        self.assertTrue(any("玩家实际提交" in message for message in messages))

    def test_closed_case_needs_feedback_and_backfill(self) -> None:
        workflow = normalize_workflow({"游戏时间": "崇祯十二年春", "状态": "已结案"})
        messages = readiness(workflow)
        self.assertTrue(any("收到下季游戏反馈" in message for message in messages))
        self.assertTrue(any("数据回填" in message for message in messages))

    def test_markdown_path_uses_quarter(self) -> None:
        path = workflow_markdown_path(Path("档案"), "崇祯12年春季执行中")
        self.assertEqual(path, Path("档案/01_季度政务/05_当前工作台/崇祯12年/春季/季度闭环工作单.md"))

    def test_markdown_marks_evidence_layers(self) -> None:
        workflow = normalize_workflow({"游戏时间": "崇祯十二年春"})
        text = render_workflow_markdown(workflow)
        self.assertIn("上季反馈（L3来源）", text)
        self.assertIn("四板块政令草稿（L1）", text)
        self.assertIn("正式诏书（L2", text)
        for section in EDICT_SECTIONS:
            self.assertIn(f"### {section}", text)

    def test_write_is_atomic_target_and_readable(self) -> None:
        workflow = normalize_workflow({"游戏时间": "崇祯十二年春"})
        with tempfile.TemporaryDirectory() as temporary:
            path = write_workflow_markdown(Path(temporary), workflow)
            self.assertTrue(path.exists())
            self.assertFalse(path.with_suffix(".md.tmp").exists())
            self.assertIn("季度闭环工作单", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
