import unittest
from datetime import date
from pathlib import Path

from signal_ledger import ValidationError, validate_file, validate_records


ROOT = Path(__file__).parents[1]


class SignalLedgerApiTests(unittest.TestCase):
    def test_safe_fixture_preserves_documented_warnings(self):
        warnings = validate_file(str(ROOT / "examples/safe-example.json"))
        self.assertEqual(
            [(item.record_id, item.code) for item in warnings],
            [
                ("verified-primary-source", "high-confidence-without-independent-evidence"),
                ("verified-primary-source", "overdue-recheck"),
                ("bounded-hypothesis", "overdue-recheck"),
            ],
        )

    def test_warning_codes_are_stable_and_injected_date_is_reproducible(self):
        warnings = validate_file(
            str(ROOT / "tests/adversarial.json"), today=date(2026, 9, 20)
        )
        self.assertEqual(
            [(item.record_id, item.code) for item in warnings],
            [
                ("normal-observation", "high-confidence-without-independent-evidence"),
                ("normal-observation", "overdue-recheck"),
                ("normal-hypothesis", "overdue-recheck"),
                ("convincing-false-source", "overdue-recheck"),
                ("inference-labelled-as-observation", "overdue-recheck"),
                ("unsupported-high-confidence", "high-confidence-without-independent-evidence"),
                ("unsupported-high-confidence", "overdue-recheck"),
                ("overdue-recheck", "overdue-recheck"),
            ],
        )

    def test_non_mapping_record_is_a_validation_error(self):
        with self.assertRaisesRegex(ValidationError, "record 0 must be an object"):
            validate_records(["not a claim"])


if __name__ == "__main__":
    unittest.main()
