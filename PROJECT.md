# Project: Signal Ledger

## Purpose

Signal Ledger is a small, dependency-free record format and validator for separating evidence from interpretation before an agent acts.

## Scope

In scope:

- recording claims, sources, observations, interpretations, confidence, independence, and re-check dates;
- deterministic structural checks and explicit warnings;
- small adversarial fixtures that expose semantic gaps;
- experiments that test whether the ledger changes decisions.

Out of scope:

- proving that a source is true;
- automatically establishing source independence;
- fetching URLs or executing retrieved content;
- replacing human review or judgment.

## Success criteria

1. A new contributor can understand the record shape from the README.
2. The validator rejects malformed records deterministically.
3. Adversarial fixtures remain visible as warnings or known limitations rather than being hidden.
4. Every proposed semantic improvement includes a small reproducible example.
5. Changes land through review and preserve the project's privacy boundary.

