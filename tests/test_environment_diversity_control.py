import unittest
from pathlib import Path

from experiments.environment_diversity_control import evaluate


FIXTURE = Path(__file__).parents[1] / "experiments" / "environment-diversity-control.json"


class EnvironmentDiversityControlTests(unittest.TestCase):
    def test_reference_fixture_matches_expected_independence(self):
        result = evaluate(FIXTURE)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["cases"], 7)
        self.assertEqual(result["independent_cases"], 2)
        self.assertEqual(result["errors"], [])
        self.assertFalse(result["semantics_changed"])

    def test_same_source_is_not_independent(self):
        fixture = FIXTURE.parent / "environment-diversity-control.json"
        result = evaluate(fixture)
        same_source = {
            item["id"]: item["independent"]
            for item in result["results"]
            if item["id"] in {"same-artifact-second-model", "same-world-replica"}
        }

        self.assertEqual(same_source, {
            "same-artifact-second-model": False,
            "same-world-replica": False,
        })

    def test_declared_shared_dependency_overrides_source_difference(self):
        result = evaluate(FIXTURE)
        shared = next(item for item in result["results"] if item["id"] == "different-source-shared-evidence")
        self.assertFalse(shared["independent"])
        self.assertTrue(shared["shared_dependency"])

    def test_missing_artifact_is_not_independent(self):
        fixture = FIXTURE.parent / "_missing-artifact-fixture.json"
        fixture.write_text(
            '{"cases": [{"id": "missing-artifact", "artifact_source": "", '
            '"verifier_source": "database-snapshot-v1", "expected_independent": false}]}',
            encoding="utf-8",
        )
        try:
            result = evaluate(fixture)
        finally:
            fixture.unlink()

        self.assertEqual(result["status"], "pass")
        self.assertFalse(result["results"][0]["independent"])


if __name__ == "__main__":
    unittest.main()
