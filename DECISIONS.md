# Decisions

## 2026-09-12 — Keep the first version dependency-free

The initial validator uses only the Python standard library. This keeps the experiment easy to inspect, run offline, and reproduce.

## 2026-09-12 — Warnings are not proof

The validator warns about unsupported confidence, stale re-checks, and explicit observation/inference confusion. It does not claim to establish truth or source independence automatically.

## 2026-09-12 — Keep adversarial failures public

The false-source and subtle inference cases remain in the fixture even when v0.2 does not detect them. A visible limitation is more useful than a green-looking test that hides the gap.

## 2026-09-12 — Exclude workspace claims from the public repository

`claims.json` is useful for local continuity but contains workspace-specific metadata. It is ignored by Git so the public project contains only portable, privacy-safe material.

