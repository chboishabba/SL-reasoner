# SL-reasoner Interface Contract (Intended)

## Status Note

This is still an intended boundary, not the main live execution path.

At the moment:

- `SensibLaw` still performs most substantive deterministic reasoning,
  review, and promotion work
- `SL-reasoner` remains a read-only interpretive scaffold
- the suite should not force work into this repo prematurely

Operational rule:

- keep this repo low priority until the core engine is sound
- use it later for optional interpretive overlays only if the split becomes
  materially useful

Current approved seam:

- producer-owned repos may export a `reasoner_input_artifact`
  payload for `SL-reasoner`
- current first adopter is `SensibLaw` AU fact-review via
  `semantic_context.reasoner_input_artifact`
- `SL-reasoner` may validate and consume that payload read-only
- `SL-reasoner` outputs remain derived-only and non-authoritative
- no promotion, reducer, or compiled-state ownership crosses this seam

## Intersections
- Consumes `SensibLaw/` core payloads in read-only mode.
- May consume `SensibLaw` Wikipedia revision pair reports as read-only
  hypothesis inputs.
- May consume `SensibLaw` contested-region graph summaries/cycle refs as
  read-only hypothesis inputs.
- Produces optional interpretive artifacts for ITIR analysis tools.
- Feeds hypothesis context to `StatiBaker/` and operator workflows.

## Interaction Model
1. Load deterministic core payloads from SensibLaw outputs.
2. Evaluate interpretive/hypothetical routines under explicit assumptions.
3. Emit non-authoritative results with provenance and disclaimers.
4. Keep removal-safe behavior: core system remains unchanged without this module.

## Exchange Channels
### Channel A: Core Payload Ingress
- Input: obligation/activation/topology-like core bundles.
- Input may also include bounded Wikipedia revision pair reports and issue
  packets from `SensibLaw`.
- Constraint: no writes back to core payload stores.

### Channel B: Assumption/Policy Ingress
- Input: evaluator settings and interpretation policy knobs.
- Constraint: every run must surface assumptions explicitly.

### Channel C: Interpretation Egress
- Output: hypothesis payloads and argument-graph structures.
- Required metadata: disclaimer, schema version, provenance refs.

### Channel D: Audit Egress
- Output: trace of inputs, assumptions, and evaluator decisions.
- Consumer: review tooling and reproducibility checks.

## Non-Goals For Now

- becoming a second canonical reducer
- absorbing active deterministic review/promotion code just for neatness
- leading suite priority ahead of producer/state/operator normalization
- turning the new adapter seam into an immediate extraction mandate
