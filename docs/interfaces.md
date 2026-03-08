# SL-reasoner Interface Contract (Intended)

## Intersections
- Consumes `SensibLaw/` core payloads in read-only mode.
- May consume `SensibLaw` Wikipedia revision pair reports as read-only
  hypothesis inputs.
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
