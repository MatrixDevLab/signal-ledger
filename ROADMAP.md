# Roadmap

## v0.2 — current baseline

- [x] Define the claim record shape.
- [x] Add deterministic structural validation.
- [x] Add an adversarial fixture for false sources, inference/observation confusion, unsupported confidence, and stale evidence.
- [x] Document the threat model and limitations.

## Next experiments

- [ ] Add a fixture where a plausible source contradicts a primary observation.
- [ ] Design a conservative check for observation/inference boundary violations without pretending to understand truth automatically.
- [ ] Compare warning-only validation with a decision gate in one small, reproducible workflow.
- [x] Record false positives and false negatives as first-class test results — baseline of 8 cases (2 TP / 2 TN / 2 FP / 2 FN) in [`experiments/fp-fn-baseline.json`](experiments/fp-fn-baseline.json).

## Later, only if justified

- [ ] Consider a versioned schema or library interface.
- [ ] Consider additional language implementations only after the format proves useful.

