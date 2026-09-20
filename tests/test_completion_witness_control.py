import unittest
from pathlib import Path

from experiments.completion_witness_control import evaluate


FIXTURE = Path(__file__).parents[1] / "experiments" / "completion-witness-control.json"


class CompletionWitnessControlTests(unittest.TestCase):
    def test_reference_fixture_is_deterministic_and_scoped(self):
        result = evaluate(FIXTURE)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(
            [item["classification"] for item in result["results"]],
            ["settled", "review", "insufficient", "insufficient"],
        )
        self.assertFalse(result["semantics_changed"])

    def test_self_grade_is_not_settled(self):
        result = evaluate(FIXTURE)
        self.assertEqual(result["results"][1]["classification"], "review")


if __name__ == "__main__":
    unittest.main()
