import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from experiments.dependency_frontier_control import admission, frontier


FIXTURE = Path(__file__).parents[1] / "experiments" / "dependency-frontier-control.json"


class DependencyFrontierControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(FIXTURE.read_text())["cases"]

    def test_atomic_chain_invalidates_bounded_dependants(self):
        result = frontier(self.cases[0])
        self.assertEqual(result["bounded_frontier"], ["action-1", "decision-1"])
        self.assertFalse(result["requires_bundle_invalidation"])

    def test_opaque_edge_marks_bundle_boundary(self):
        result = frontier(self.cases[3])
        self.assertEqual(result["opaque_frontier"], ["bundle-x"])
        self.assertTrue(result["requires_bundle_invalidation"])

    def test_mixed_graph_preserves_bounded_and_opaque_frontiers(self):
        result = frontier(self.cases[2])
        self.assertEqual(result["bounded_frontier"], ["action-2", "decision-2", "summary-ab"])
        self.assertEqual(result["opaque_frontier"], [])

    def test_repeated_evaluation_is_identical(self):
        first = [frontier(case) for case in self.cases]
        second = [frontier(case) for case in self.cases]
        self.assertEqual(first, second)

    def test_consumer_keeps_opaque_edges_at_bundle_boundary(self):
        result = admission(frontier(self.cases[3]))
        self.assertEqual(result, {
            "disposition": "review_bundle",
            "revalidation_scope": ["bundle-x"],
        })

    def test_consumer_exposes_only_bounded_revalidation_scope(self):
        result = admission(frontier(self.cases[0]))
        self.assertEqual(result, {
            "disposition": "revalidate_bounded",
            "revalidation_scope": ["action-1", "decision-1"],
        })

    def test_frontier_partitions_are_disjoint_and_exclude_tombstones(self):
        for case in self.cases:
            result = frontier(case)
            bounded = set(result["bounded_frontier"])
            opaque = set(result["opaque_frontier"])
            tombstones = set(result["tombstones"])
            self.assertTrue(bounded.isdisjoint(opaque))
            self.assertTrue(bounded.isdisjoint(tombstones))
            self.assertTrue(opaque.isdisjoint(tombstones))

    def test_bundle_review_scope_does_not_leak_bounded_nodes(self):
        result = frontier(self.cases[3])
        consumer = admission(result)
        self.assertEqual(consumer["disposition"], "review_bundle")
        self.assertEqual(set(consumer["revalidation_scope"]), set(result["opaque_frontier"]))
        self.assertNotIn("action-3", consumer["revalidation_scope"])


if __name__ == "__main__":
    unittest.main()
