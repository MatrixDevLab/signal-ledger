#!/usr/bin/env python3
"""Review-only handoff seam control; never authorizes or retries an action."""
import json
import sys
from pathlib import Path


def classify(case):
    trace, execution = case["trace_outcome"], case["execution_outcome"]
    if trace == "unknown" and execution == "unknown":
        return "deny_unresolved"
    if trace == "unknown":
        return "deny_missing_trace"
    if execution == "unknown":
        return "deny_missing_execution"
    if trace != execution:
        return "deny_divergence"
    if not case["seam_observed"]:
        return "deny_missing_seam"
    return "review_aligned"


def main(path):
    fixture = json.loads(Path(path).read_text())
    rows = [{"id": c["id"], "expected_state": c["expected_state"], "observed_state": classify(c)} for c in fixture["cases"]]
    mismatches = [r for r in rows if r["expected_state"] != r["observed_state"]]
    result = {
        "schema": 1,
        "title": fixture["title"],
        "input": path,
        "rows": rows,
        "summary": {"cases": len(rows), "mismatches": len(mismatches), "passed": not mismatches},
        "finding": "Aligned outcomes remain review-only when the handoff seam is observed; missing seam evidence is a deny boundary, while divergence or missing outcomes remain deny states.",
        "safety": "classification only; no authorization, write, retry, or validator action is performed",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
