#!/usr/bin/env python3
"""Classify abstract effect settlement states without retry side effects."""
import json
import sys
from pathlib import Path


def classify(case):
    if case["acceptance_status"] != "accepted":
        return "acceptance_unknown"
    if case["deletion_status"] == "deleted":
        return "accepted_readback_deleted"
    if case["readback_status"] == "present" and case["deletion_status"] == "not_deleted":
        return "accepted_and_read_back"
    return "accepted_readback_missing"


def main(path):
    fixture = json.loads(Path(path).read_text())
    rows = []
    for case in fixture["cases"]:
        observed = classify(case)
        rows.append({"id": case["id"], "expected_state": case["expected_state"], "observed_state": observed})
    mismatches = [row for row in rows if row["expected_state"] != row["observed_state"]]
    result = {
        "schema": 1,
        "title": fixture["title"],
        "input": path,
        "runs": 1,
        "rows": rows,
        "summary": {"cases": len(rows), "mismatches": len(mismatches), "passed": not mismatches},
        "safety": "classification only; no retry, write, or validator action is performed",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
