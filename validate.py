#!/usr/bin/env python3
"""Deterministic structural validator for Signal Ledger records."""
import json
import sys
from datetime import date
from pathlib import Path

REQUIRED = {
    "id", "claim", "sources", "observations", "interpretation",
    "confidence", "independence", "checked_at", "recheck_after",
    "decision_changed",
}
CONFIDENCE = {"low", "medium", "high"}
INDEPENDENCE = {"single-source", "related-sources", "independent"}


def main(path: str) -> int:
    records = json.loads(Path(path).read_text())
    if not isinstance(records, list) or not records:
        raise ValueError("ledger must be a non-empty list")
    ids = set()
    warnings = []
    today = date.today()
    for i, record in enumerate(records):
        missing = REQUIRED - record.keys()
        if missing:
            raise ValueError(f"record {i} missing: {sorted(missing)}")
        record_id = record["id"]
        if record_id in ids:
            raise ValueError(f"duplicate id: {record_id}")
        ids.add(record_id)
        if record["confidence"] not in CONFIDENCE:
            raise ValueError(f"invalid confidence: {record_id}")
        if record["independence"] not in INDEPENDENCE:
            raise ValueError(f"invalid independence: {record_id}")
        if not record["sources"] or not record["observations"]:
            raise ValueError(f"empty evidence: {record_id}")

        if record["confidence"] == "high" and record["independence"] != "independent":
            warnings.append((record_id, "high-confidence-without-independent-evidence"))
        recheck = record.get("recheck_after")
        if recheck:
            try:
                if date.fromisoformat(recheck) < today:
                    warnings.append((record_id, "overdue-recheck"))
            except ValueError:
                raise ValueError(f"invalid recheck_after date: {record_id}")
        if any("interpretation:" in str(item).lower() for item in record["observations"]):
            warnings.append((record_id, "observation-explicitly-labelled-interpretation"))

    print(f"validated {len(records)} claim records; warnings={len(warnings)}")
    for record_id, warning in warnings:
        print(f"warning {record_id}: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
