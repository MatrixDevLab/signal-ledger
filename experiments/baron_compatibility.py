#!/usr/bin/env python3
"""Validate the source-derived Baron/Signal Ledger compatibility fixture.

This is deliberately a contract checker, not a Baron implementation.  It
checks that each fixture case preserves the boundary between runtime grounding
evidence and truth labels, and that retraction retains history while removing
support.  It has no network or third-party dependencies.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_CASES = {
    "no-prepass": {
        "baron": {"verdict": "ungrounded", "reason_code": "no_pre_pass"},
        "mapping": "review_or_unknown",
    },
    "prepassed-supported-answer": {
        "baron": {"verdict": "grounded_if_all_claims_supported_and_ratio_at_least_0.80"},
        "mapping": "observation_only",
    },
    "mixed-support-answer": {
        "baron": {"verdict": "partial_or_ungrounded_by_aggregate"},
        "mapping": "review",
    },
    "retracted-support": {
        "baron": {
            "search_visibility": "excluded_after_retraction",
            "grounding_support": "cannot_use_retracted_node",
            "history": "retained",
        },
        "mapping": "unknown_with_withdrawn_evidence",
    },
}


def check(path: Path) -> dict[str, object]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    cases = {case["id"]: case for case in fixture.get("cases", [])}
    errors: list[str] = []

    if fixture.get("status") != "research_only_unexecuted":
        errors.append("fixture must remain explicitly unexecuted")

    for case_id, expected in EXPECTED_CASES.items():
        case = cases.get(case_id)
        if case is None:
            errors.append(f"missing case: {case_id}")
            continue
        observed = case.get("baron_expected", {})
        for key, value in expected["baron"].items():
            if observed.get(key) != value:
                errors.append(f"{case_id}: {key}={observed.get(key)!r}, expected {value!r}")
        mapping = case.get("signal_ledger_interop", {}).get("mapping")
        if mapping != expected["mapping"]:
            errors.append(f"{case_id}: mapping={mapping!r}, expected {expected['mapping']!r}")

    retracted = cases.get("retracted-support", {}).get("baron_expected", {})
    if retracted.get("history") == "deleted":
        errors.append("retracted support must retain inspectable history")

    return {
        "fixture": str(path),
        "cases": len(cases),
        "expected_cases": len(EXPECTED_CASES),
        "errors": errors,
        "status": "pass" if not errors else "fail",
        "semantics_changed": False,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("baron-compatibility-fixture.json")
    result = check(path)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
