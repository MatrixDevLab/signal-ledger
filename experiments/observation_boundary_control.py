#!/usr/bin/env python3
"""Run a deliberately narrow observation/inference boundary check.

This is a structural review aid: it only flags explicit markers in fixture
records and never claims to understand whether a sentence is true.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def check(path: Path) -> dict[str, object]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    cases = fixture.get("cases", [])
    results = []
    errors = []
    for case in cases:
        observations = [str(item).lower() for item in case.get("observations", [])]
        explicit = any("inference:" in item or "interpretation:" in item for item in observations)
        expected = case.get("expected_explicit_boundary_warning", False)
        results.append({"id": case.get("id"), "explicit_marker": explicit, "warning": explicit})
        if explicit != expected:
            errors.append(f"{case.get('id')}: explicit marker={explicit}, expected {expected}")

    return {
        "fixture": str(path),
        "cases": len(cases),
        "results": results,
        "warnings": sum(1 for result in results if result["warning"]),
        "errors": errors,
        "status": "pass" if not errors else "fail",
        "semantics_changed": False,
        "scope": "explicit markers only; no truth or semantic classification",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("observation-boundary-control.json")
    result = check(path)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
