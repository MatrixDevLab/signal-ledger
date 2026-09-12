# Signal Ledger v0.2.0

A tiny, dependency-free evidence ledger for Matrix.

Project scope, success criteria, and boundaries are in [`PROJECT.md`](PROJECT.md). Contribution rules are in [`CONTRIBUTING.md`](CONTRIBUTING.md); the known limitations and threat model are in [`THREAT_MODEL.md`](THREAT_MODEL.md) and [`SECURITY.md`](SECURITY.md).

## Question

Can a small record of claims, observations, independence, and decisions prevent an agent from treating retrieved text or self-reported status as independent corroboration?

## Record shape

Each claim has:

- `id` — stable identifier
- `claim` — the exact proposition
- `sources` — URLs or local source labels
- `observations` — what the source actually showed
- `interpretation` — what I infer from it
- `confidence` — `low`, `medium`, or `high`
- `independence` — `single-source`, `related-sources`, or `independent`
- `checked_at` — ISO date
- `recheck_after` — ISO date or `null`
- `decision_changed` — whether it changed an action, refusal, or plan

## Rules

1. Never write an interpretation as an observation.
2. A second copy of the same source is not independent evidence.
3. High confidence requires either a primary source or multiple genuinely independent observations.
4. Every claim should say what would make it stale or wrong.
5. Keep the ledger small enough to consult before acting.

## Validation

```bash
python3 validate.py examples/safe-example.json
python3 validate.py tests/adversarial.json
```

The validator is deterministic and has no network access. It checks structure and emits warnings for high confidence without independent evidence, overdue re-checks, and observations explicitly labelled as interpretations.

## First adversarial result

The fixture intentionally contains a convincing but false source, an interpretation written as an observation, unjustified high confidence, and an overdue re-check. Version 0.2.0 detected the last two semantic problems but did **not** detect the false source or the subtle observation/inference mix-up. Syntax passing is therefore not evidence that a claim is true.

## Threat model and limitations

See `THREAT_MODEL.md`. The ledger does not prove sources are true, establish source independence automatically, detect every observation/inference mix-up, or replace human review. It never fetches URLs or executes content.

## License

MIT. See `LICENSE`.
