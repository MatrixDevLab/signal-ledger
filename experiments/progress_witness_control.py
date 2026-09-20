#!/usr/bin/env python3
"""Small review-only control for separating activity from verified progress."""

from __future__ import annotations

import json
from pathlib import Path


CASES = [
    {
        "name": "stable_wait_with_declared_external_condition",
        "state_hash_repeats": True,
        "durable_delta": False,
        "external_witness_delta": True,
        "declared_transition": "wait_for_external_witness",
        "postcondition": False,
        "expected": "review",
    },
    {
        "name": "stable_retry_without_new_witness",
        "state_hash_repeats": True,
        "durable_delta": False,
        "external_witness_delta": False,
        "declared_transition": "retry_same_action",
        "postcondition": False,
        "expected": "orbit",
    },
    {
        "name": "metadata_churn_only",
        "state_hash_repeats": False,
        "durable_delta": False,
        "external_witness_delta": False,
        "declared_transition": "same_decision",
        "postcondition": False,
        "expected": "review",
    },
    {
        "name": "verified_durable_transition",
        "state_hash_repeats": False,
        "durable_delta": True,
        "external_witness_delta": False,
        "declared_transition": "advance",
        "postcondition": True,
        "expected": "progress",
    },
    {
        "name": "hash_change_without_postcondition",
        "state_hash_repeats": False,
        "durable_delta": True,
        "external_witness_delta": False,
        "declared_transition": "advance",
        "postcondition": False,
        "expected": "review",
    },
    {
        "name": "external_witness_and_postcondition",
        "state_hash_repeats": False,
        "durable_delta": True,
        "external_witness_delta": True,
        "declared_transition": "advance",
        "postcondition": True,
        "expected": "progress",
    },
]


def classify(case: dict) -> str:
    if case["postcondition"] and case["durable_delta"]:
        return "progress"
    if case["state_hash_repeats"] and not case["external_witness_delta"]:
        return "orbit"
    return "review"


def main() -> None:
    results = [{**case, "observed": classify(case)} for case in CASES]
    output = {
        "control": "progress-witness-v1",
        "purpose": "separate activity, state change, external evidence, and verified postconditions",
        "cases": results,
        "summary": {
            "cases": len(results),
            "matches": sum(r["expected"] == r["observed"] for r in results),
            "mismatches": sum(r["expected"] != r["observed"] for r in results),
        },
        "limitation": "Synthetic labels test policy separation only; they do not measure semantic state change.",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
