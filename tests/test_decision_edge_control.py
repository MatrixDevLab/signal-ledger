import unittest
from pathlib import Path

from experiments.decision_edge_control import evaluate


FIXTURE = Path(__file__).parents[1] / "experiments" / "decision-edge-control.json"


class DecisionEdgeControlTests(unittest.TestCase):
    def test_reference_fixture_is_deterministic_and_scoped(self):
        result = evaluate(FIXTURE)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(
            [item["classification"] for item in result["results"]],
            ["settled", "review", "insufficient"],
        )
        self.assertFalse(result["semantics_changed"])

    def test_missing_delta_is_not_settled(self):
        fixture = FIXTURE.parent / "_missing-delta-fixture.json"
        fixture.write_text(
            '{"cases": [{"id": "missing", "decision_delta": null, '
            '"expected_state": "ok", "observed_state": "ok", '
            '"expected_classification": "insufficient"}]}',
            encoding="utf-8",
        )
        try:
            result = evaluate(fixture)
        finally:
            fixture.unlink()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["results"][0]["classification"], "insufficient")

    def test_malformed_delta_is_not_a_runtime_error(self):
        fixture = FIXTURE.parent / "_malformed-delta-fixture.json"
        fixture.write_text(
            '{"cases": [{"id": "malformed", "decision_delta": "chosen", '
            '"expected_state": "ok", "observed_state": "ok", '
            '"expected_classification": "insufficient"}]}',
            encoding="utf-8",
        )
        try:
            result = evaluate(fixture)
        finally:
            fixture.unlink()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["results"][0]["classification"], "insufficient")


if __name__ == "__main__":
    unittest.main()
