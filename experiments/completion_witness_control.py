#!/usr/bin/env python3
"""Review-only control for independent completion evidence.

It prevents a self-reported completion check from being treated as a settled
postcondition when the checker and the work share the same evidence source.
This is an evidence-shape control, not a truth or intent detector.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def classify(case: dict[str, object]) -> str:
    if not case.get("postcondition_observed"):
        return "insufficient"
    action_source = case.get("action_source")
    verifier_source = case.get("verifier_source")
    if not action_source or not verifier_source:
        return "insufficient"
    if action_source == verifier_source:
        return "review"
    return "settled"


def evaluate(path: Path) -> dict[str, object]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    results = []
    errors = []
    for case in fixture.get("cases", []):
        result = {"id": case.get("id"), "classification": classify(case)}
        results.append(result)
        if result["classification"] != case.get("expected_classification"):
            errors.append(
                f"{case.get('id')}: {result['classification']} != "
                f"{case.get('expected_classification')}"
            )
    return {
        "fixture": str(path),
        "cases": len(results),
        "results": results,
        "errors": errors,
        "status": "pass" if not errors else "fail",
        "semantics_changed": False,
        "scope": "completion-evidence independence only; no truth or intent inference",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("completion-witness-control.json")
    first = evaluate(path)
    second = evaluate(path)
    first["repeat_identical"] = first == second
    print(json.dumps(first, sort_keys=True, indent=2))
    return 0 if first["status"] == "pass" and first["repeat_identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
