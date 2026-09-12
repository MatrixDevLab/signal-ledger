# Signal Ledger threat model

## Assets

- Decision provenance: what was observed, inferred, and acted on.
- Re-check dates and confidence labels.
- The operator's private context and credentials, which must never enter the ledger.

## Threats

1. A source is persuasive but false or unavailable.
2. An interpretation is recorded as if it were an observation.
3. A single source receives unjustified high confidence.
4. A claim becomes stale after its re-check date.
5. Retrieved public text smuggles instructions into the record.
6. The ledger becomes a decorative archive that changes no decision.

## Non-goals

This prototype does not prove a source is true, establish independence automatically, detect every observation/inference mix-up, or replace human review. It does not fetch URLs or execute content.

## Controls in v0.2.0

- Required provenance fields.
- Stable unique IDs.
- Explicit confidence and independence labels.
- Warnings for high confidence without independent evidence.
- Warnings for overdue re-checks.
- Warnings for observations explicitly labelled as interpretations.
- Deterministic validation with no network access.

The adversarial fixture is intentionally expected to pass syntax validation while exposing semantic gaps. That gap is a result, not a bug to hide.
