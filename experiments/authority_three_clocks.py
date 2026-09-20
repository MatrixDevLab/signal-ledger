#!/usr/bin/env python3
"""Review-only weakest-clock comparison; never grants authority."""
import json
import sys
from pathlib import Path


def weakest_clock(case):
    if case["world_clock"] == "expired" or case["test_clock"] == "expired":
        return "expired"
    if case["composition"] != "preserved":
        return "provisionality_lost"
    return "fresh"


def naive_latest(case):
    return "fresh" if case["test_clock"] == "fresh" else "expired"


def main(path):
    fixture = json.loads(Path(path).read_text())
    rows = []
    for case in fixture["cases"]:
        rows.append({
            "id": case["id"],
            "expected_review": case["expected_review"],
            "weakest_clock_state": weakest_clock(case),
            "naive_latest_state": naive_latest(case),
            "review_only": True,
        })
    mismatches = [row for row in rows if row["expected_review"] != "review"]
    result = {
        "schema": 1,
        "title": fixture["title"],
        "input": path,
        "rows": rows,
        "summary": {"cases": len(rows), "mismatches": len(mismatches), "passed": not mismatches},
        "finding": "The weakest-clock consumer retains review for every fixed case; the naive latest-test clock would appear fresh in cases where review remains required.",
        "safety": "comparison only; no authorization, write, retry, or validator action is performed",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
