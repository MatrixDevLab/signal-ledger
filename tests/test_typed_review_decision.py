import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "experiments" / "typed_review_decision.py"
SPEC = importlib.util.spec_from_file_location("typed_review_decision", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TypedReviewDecisionTests(unittest.TestCase):
    def test_quoted_or_attributed_inference_is_not_reviewed(self):
        self.assertIsNone(MODULE.make_warning('The report quotes: "Therefore, review the claim."'))
        self.assertIsNone(MODULE.make_warning("The author claims the result proves the policy is safe."))


    def test_author_assertion_cue_is_typed_review_not_block(self):
        warning = MODULE.make_warning("The replay demonstrates that the missing field changed the decision.")
        self.assertEqual(warning["type"], "prose-inference-cue")
        self.assertEqual(warning["scope"], "author-assertion")
        self.assertEqual(MODULE.decision(warning, "typed-review"), "review")
        self.assertEqual(MODULE.decision(warning, "generic-blocking"), "block")
