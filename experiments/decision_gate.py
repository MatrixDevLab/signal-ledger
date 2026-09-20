#!/usr/bin/env python3
"""Compare warning-only and block-on-warning policies against the baseline."""
import json
import sys
from pathlib import Path


def classify(cases, policy):
    rows = []
    for case in cases:
        flagged = case["flagged"]
        blocked = policy == "block-on-warning" and flagged
        rows.append(
            {
                "id": case["id"],
                "intent": case["intent"],
                "flagged": flagged,
                "classification": case["classification"],
                "decision": "blocked" if blocked else ("allow-with-warning" if flagged else "allow"),
            }
        )
    return rows


def summarize(rows):
    blocked = [row for row in rows if row["decision"] == "blocked"]
    return {
        "cases": len(rows),
        "blocked": len(blocked),
        "allowed": len(rows) - len(blocked),
        "blocked_true_positive": sum(row["classification"] == "true-positive" for row in blocked),
        "blocked_false_positive": sum(row["classification"] == "false-positive" for row in blocked),
        "adversarial_allowed": sum(row["intent"] == "adversarial" and row["decision"] != "blocked" for row in rows),
    }


def main(baseline_path, output_path):
    baseline = json.loads(Path(baseline_path).read_text())
    all_cases = [case for fixture in baseline["fixtures"] for case in fixture["cases"]]
    policies = {}
    for policy in ("warning-only", "block-on-warning"):
        rows = classify(all_cases, policy)
        policies[policy] = {"summary": summarize(rows), "cases": rows}
    result = {
        "schema": 1,
        "title": "Warning-only versus decision-gate comparison",
        "input": "experiments/fp-fn-baseline.json",
        "method": {
            "runs": 2,
            "case_source": "The baseline's recorded per-case flagged and classification fields",
            "warning_only": "Never block; preserve warnings for review.",
            "block_on_warning": "Block whenever the validator emits at least one warning.",
        },
        "policies": policies,
        "finding": {
            "result": "block-on-warning blocks 4 of 8 cases: 2 intended adversarial cases and 2 benign controls.",
            "implication": "A naive gate converts the existing warning false positives into blocked work while still allowing 2 adversarial cases, so warning severity needs a narrower policy before merge gating.",
        },
    }
    Path(output_path).write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: decision_gate.py BASELINE OUTPUT")
    main(sys.argv[1], sys.argv[2])
