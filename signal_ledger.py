"""Programmatic interface for validating Signal Ledger records.

The validator is deliberately structural and deterministic. It does not fetch
sources, execute content, or decide whether a claim is true.
"""

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence


REQUIRED = {
    "id",
    "claim",
    "sources",
    "observations",
    "interpretation",
    "confidence",
    "independence",
    "checked_at",
    "recheck_after",
    "decision_changed",
}
CONFIDENCE = {"low", "medium", "high"}
INDEPENDENCE = {"single-source", "related-sources", "independent"}


class ValidationError(ValueError):
    """Raised when a ledger is structurally invalid."""


@dataclass(frozen=True)
class LedgerWarning:
    """A deterministic warning attached to one claim record."""

    record_id: str
    code: str


def validate_records(
    records: Any, *, today: Optional[date] = None
) -> Sequence[LedgerWarning]:
    """Validate records and return warnings without performing I/O.

    ``today`` is injectable so callers and tests can make overdue checks
    reproducible. Warnings do not make a ledger invalid; malformed structure
    raises :class:`ValidationError`.
    """

    if not isinstance(records, list) or not records:
        raise ValidationError("ledger must be a non-empty list")

    warnings = []
    ids = set()
    current_date = today or date.today()

    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ValidationError(f"record {index} must be an object")

        missing = REQUIRED - record.keys()
        if missing:
            raise ValidationError(f"record {index} missing: {sorted(missing)}")

        record_id = record["id"]
        if record_id in ids:
            raise ValidationError(f"duplicate id: {record_id}")
        ids.add(record_id)

        if record["confidence"] not in CONFIDENCE:
            raise ValidationError(f"invalid confidence: {record_id}")
        if record["independence"] not in INDEPENDENCE:
            raise ValidationError(f"invalid independence: {record_id}")
        if not record["sources"] or not record["observations"]:
            raise ValidationError(f"empty evidence: {record_id}")

        if record["confidence"] == "high" and record["independence"] != "independent":
            warnings.append(LedgerWarning(record_id, "high-confidence-without-independent-evidence"))

        recheck = record.get("recheck_after")
        if recheck:
            try:
                if date.fromisoformat(recheck) < current_date:
                    warnings.append(LedgerWarning(record_id, "overdue-recheck"))
            except (TypeError, ValueError):
                raise ValidationError(f"invalid recheck_after date: {record_id}")

        if any("interpretation:" in str(item).lower() for item in record["observations"]):
            warnings.append(
                LedgerWarning(record_id, "observation-explicitly-labelled-interpretation")
            )

    return warnings


def load_records(path: str) -> Any:
    """Load JSON records from ``path``; validation remains a separate step."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_file(path: str, *, today: Optional[date] = None) -> Sequence[LedgerWarning]:
    """Load and validate a JSON ledger file."""

    return validate_records(load_records(path), today=today)
