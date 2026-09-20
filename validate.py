#!/usr/bin/env python3
"""Command-line entry point for the deterministic Signal Ledger validator."""
import sys

from signal_ledger import load_records, validate_file


def main(path: str) -> int:
    warnings = validate_file(path)

    print(f"validated {len(load_records(path))} claim records; warnings={len(warnings)}")
    for warning in warnings:
        print(f"warning {warning.record_id}: {warning.code}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
