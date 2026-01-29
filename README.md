# sensiblaw-interpretation (scaffold)

> Interpretive / hypothetical layer for SensibLaw. **Non-authoritative.** Core payloads remain unchanged.

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
