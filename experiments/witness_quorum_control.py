#!/usr/bin/env python3
"""Review-only currentness witness quorum control; never authorizes an action."""
import json
import sys
from pathlib import Path


def classify(case):
    witnesses = case["witnesses"]
    if not witnesses or len(witnesses) < case["quorum"]:
        return "deny_unresolved_quorum"
    if any(w["status"] != "current" for w in witnesses):
        return "deny_non_current_witness"
    if any(w["epoch"] != case["issuer_epoch"] for w in witnesses):
        return "deny_epoch_disagreement"
    if len({w["authority"] for w in witnesses}) < case["quorum"]:
        return "deny_shared_authority"
    return "review_current_quorum"


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
        "finding": "Currentness is reviewable only when independent witnesses agree on the issuer epoch; missing quorum, stale witnesses, disagreement, and shared authority remain deny states.",
        "safety": "classification only; no authorization, write, retry, or validator action is performed",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
