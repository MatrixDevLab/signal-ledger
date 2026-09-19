#!/usr/bin/env python3
"""Review-only grant/currentness comparison; never authorizes an action."""
import json
import sys
from pathlib import Path


def classify(case):
    if case["grant_epoch"] != case["current_epoch"]:
        return "deny_epoch_mismatch"
    if case["revocation_witness"] != "current":
        return "deny_revoked_or_stale"
    if case["witness_independence"] != "independent":
        return "deny_unresolved_authority"
    return "review_current"


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
        "rows": rows,
        "summary": {"cases": len(rows), "mismatches": len(mismatches), "passed": not mismatches},
        "finding": "A matching grant epoch is insufficient when the currentness or independence witness is stale, revoked, or unresolved.",
        "safety": "classification only; no authorization, write, retry, or validator action is performed",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
