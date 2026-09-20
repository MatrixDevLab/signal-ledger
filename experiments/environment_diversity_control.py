#!/usr/bin/env python3
"""Check whether verification cases name an evidence source distinct from the artifact.

This is a review-only structural control. It does not claim that a world check is
correct; it prevents a second model reading the same artifact—or sharing an
explicit evidence dependency—from being labelled independent evidence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def evaluate(path: Path) -> dict[str, object]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    results = []
    errors = []
    for case in fixture.get("cases", []):
        artifact = case.get("artifact_source")
        verifier = case.get("verifier_source")
        shared = bool(case.get("shared_dependency"))
        independent = artifact != verifier and bool(verifier) and not shared
        expected = bool(case.get("expected_independent"))
        result = {
            "id": case.get("id"),
            "independent": independent,
            "expected": expected,
            "shared_dependency": shared,
        }
        results.append(result)
        if independent != expected:
            errors.append(f"{case.get('id')}: independent={independent}, expected={expected}")
    return {
        "fixture": str(path),
        "cases": len(results),
        "independent_cases": sum(1 for item in results if item["independent"]),
        "results": results,
        "errors": errors,
        "status": "pass" if not errors else "fail",
        "semantics_changed": False,
        "scope": "source identity and declared dependency only; no claim or outcome validation",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("environment-diversity-control.json")
    result = evaluate(path)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
