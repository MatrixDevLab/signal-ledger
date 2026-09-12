# Contributing

Signal Ledger prefers small, testable contributions over broad rewrites.

## Before opening a change

1. Read `PROJECT.md`, `THREAT_MODEL.md`, and `DECISIONS.md`.
2. Open or reference an Issue describing the concrete case.
3. Keep examples synthetic and free of private context, credentials, infrastructure details, or personal data.
4. Use a branch and Pull Request. Do not push directly to `main`.

## Checks

Run both fixtures from the repository root:

```bash
python3 validate.py examples/safe-example.json
python3 validate.py tests/adversarial.json
```

Warnings in the adversarial fixture are expected. A non-zero exit code or malformed-record failure is not.

## Review standard

A useful change should add one of:

- a concrete adversarial example;
- a reproducible validator improvement;
- a clarified threat or limitation;
- evidence that a proposed rule changes a decision safely.

Do not claim that syntax validation proves a source or conclusion is true.

