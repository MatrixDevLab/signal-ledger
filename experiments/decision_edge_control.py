#!/usr/bin/env python3
"""Review-only control for recording the state transition behind an action.

The control distinguishes a settled transition from a post-hoc action trace.
It does not infer intent, agency, or semantic correctness.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def classify(case: dict[str, object]) -> str:
    if not case.get("decision_delta"):
        return "insufficient"
    if case.get("expected_state") == case.get("observed_state"):
        return "settled"
    return "review"


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
        "scope": "decision-edge evidence shape only; no intent or truth inference",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("decision-edge-control.json")
    first = evaluate(path)
    second = evaluate(path)
    first["repeat_identical"] = first == second
    print(json.dumps(first, sort_keys=True, indent=2))
    return 0 if first["status"] == "pass" and first["repeat_identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
