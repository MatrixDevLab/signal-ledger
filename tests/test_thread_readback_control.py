"""Regression tests for the canonical-thread readback safety boundary."""
import unittest

from experiments.thread_readback_control import classify


class ThreadReadbackControlTests(unittest.TestCase):
    def test_absent_notification_is_no_action(self):
        self.assertEqual(
            classify({
                "notification_status": "absent",
                "thread_status": "complete",
                "comment_status": "present",
            }),
            "no_action",
        )

    def test_incomplete_readback_is_permanent_no_retry_boundary(self):
        self.assertEqual(
            classify({
                "notification_status": "present",
                "thread_status": "incomplete",
                "comment_status": "absent",
            }),
            "no_retry_incomplete_effect",
        )

    def test_complete_present_readback_is_actionable(self):
        self.assertEqual(
            classify({
                "notification_status": "present",
                "thread_status": "complete",
                "comment_status": "present",
            }),
            "actionable",
        )


if __name__ == "__main__":
    unittest.main()
