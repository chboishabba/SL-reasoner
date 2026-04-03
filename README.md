# sensiblaw-interpretation (scaffold)

> Interpretive / hypothetical layer for SensibLaw. **Non-authoritative.** Core payloads remain unchanged.

## Current Status

This repo is intentionally parked at scaffold level for now.

The intended boundary is still correct, but the current suite implementation
does **not** route most substantive reasoning through this module yet.
Today, the real deterministic extraction, review, promotion, and most
reasoning-like behavior still lives in `SensibLaw`.

That is acceptable for now.

Current working rule:

- keep building the real engine in `SensibLaw` while the core contracts,
  reducers, and operator surfaces are still settling
- keep `SL-reasoner` cordoned as an optional interpretive/LLM-facing layer
- only pull code outward into `SL-reasoner` later if `SensibLaw` complexity
  becomes large enough that the separation is materially helpful

So the near-term posture is:

- low priority
- no pressure to “use the repo because it exists”
- no second authority path
- no refactor until there is a concrete complexity threshold or boundary win

Current landed seam:

- `SensibLaw` may export a producer-owned `reasoner_input_artifact`
  contract-shaped payload for future `SL-reasoner` consumption
- `SL-reasoner` now has explicit adapter/contract helpers for:
  - validating read-only input artifacts
  - emitting derived reasoning artifacts
- that seam does not move any substantive deterministic logic out of
  `SensibLaw`
- no LLM/model execution is activated by this seam

## Purpose
- Experiment with reasoning/interpretation **separate** from core extraction.
- Produce optional, discardable hypotheses (`interpretation.v0.*`).
- Keep SensibLaw core deterministic and non-reasoning.

## Hard boundaries
- Read core payloads (obligation/activation/topology) **read-only**.
- Never mutate or rewrite core bundles or identity hashes.
- Outputs must be explicitly labeled as interpretive/hypothetical.
- Removing this module must leave core system behavior unchanged.

## Suggested outputs
- `InterpretationHypothesis` with assumptions + provenance.
- `ArgumentGraph` capturing alternative readings.
- All outputs carry a disclaimer and are versioned separately (`interpretation.v0.experimental`).

## Non-goals (for this repo)
- Compliance or correctness judgments.
- Precedence/conflict resolution that feeds back into core.
- Ontology expansion or synonym normalization.
- Hidden defaults or auto-resolution of “winners.”

## Next steps (when you decide to reason)
1. Define schemas under `schemas/interpretation.v0.*`.
2. Implement adapters in `interpretation/inputs.py` to ingest core payloads read-only.
3. Add evaluators under `interpretation/evaluators/` that always emit explicit assumptions + disclaimer.
4. Keep tests that fail if any core import is write-capable or if outputs miss disclaimers.

Initial posture: start by trying **Lila** as the first interpretation engine, and keep outputs explicitly
labeled as interpretive/hypothetical (never fed back into core).

## Refactor Trigger

Do not expand this repo just because reasoning exists somewhere in the suite.

Bring work here later only if one or more of these become true:

- `SensibLaw` accumulates too much optional or hypothetical reasoning logic
- derived explanation/comparison/follow-planning code is obscuring the core
  deterministic review path
- a clean read-only interpretive interface over stable `SensibLaw` outputs is
  now cheaper than continuing to co-locate everything

Until then, the right move is to leave `SL-reasoner` small and explicit.
