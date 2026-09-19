import json
import unittest
from pathlib import Path

from experiments.effect_settlement_control import classify


FIXTURE = Path(__file__).parents[1] / "experiments" / "effect-settlement-control.json"


class EffectSettlementControlTests(unittest.TestCase):
    def test_labelled_fixture_matches_review_states(self):
        fixture = json.loads(FIXTURE.read_text())
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(classify(case), case["expected_state"])

    def test_missing_readback_is_not_confirmed(self):
        case = {
            "acceptance_status": "accepted",
            "readback_status": "missing",
            "deletion_status": "not_deleted",
        }
        self.assertEqual(classify(case), "accepted_readback_missing")

    def test_unknown_acceptance_wins_over_readback_shape(self):
        case = {
            "acceptance_status": "unknown",
            "readback_status": "present",
            "deletion_status": "not_deleted",
        }
        self.assertEqual(classify(case), "acceptance_unknown")
