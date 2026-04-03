"""
Contract helpers for the deferred `SL-reasoner` boundary.

These helpers freeze two surfaces:
- read-only reasoner input artifacts exported by producer-owned repos
- explicitly derived/non-authoritative reasoner outputs
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


REASONER_INPUT_ARTIFACT_SCHEMA_VERSION = "sl.reasoner_input.v0_1"
REASONER_DERIVED_ARTIFACT_SCHEMA_VERSION = "sl.reasoner_derived.v0_1"
SUITE_NORMALIZED_ARTIFACT_SCHEMA_VERSION = "itir.normalized.artifact.v1"
ALLOWED_INPUT_ARTIFACT_ROLES = frozenset({"reviewable_claim", "promoted_record", "derived_product"})


def validate_reasoner_input_artifact(payload: Mapping[str, Any]) -> None:
    if str(payload.get("schema_version") or "") != REASONER_INPUT_ARTIFACT_SCHEMA_VERSION:
        raise ValueError("Unsupported reasoner input artifact schema_version")
    if str(payload.get("source_system") or "") != "SensibLaw":
        raise ValueError("Reasoner input artifacts must currently come from SensibLaw")

    normalized_artifact = payload.get("normalized_artifact")
    if not isinstance(normalized_artifact, Mapping):
        raise ValueError("Reasoner input artifact requires normalized_artifact")
    if str(normalized_artifact.get("schema_version") or "") != SUITE_NORMALIZED_ARTIFACT_SCHEMA_VERSION:
        raise ValueError("normalized_artifact must use the suite normalized artifact schema")
    artifact_role = str(normalized_artifact.get("artifact_role") or "")
    if artifact_role not in ALLOWED_INPUT_ARTIFACT_ROLES:
        raise ValueError("normalized_artifact role is not allowed for reasoner input")

    compiler_contract = payload.get("compiler_contract")
    promotion_gate = payload.get("promotion_gate")
    if not isinstance(compiler_contract, Mapping):
        raise ValueError("Reasoner input artifact requires compiler_contract")
    if not isinstance(promotion_gate, Mapping):
        raise ValueError("Reasoner input artifact requires promotion_gate")


def build_reasoner_derived_artifact(
    *,
    artifact_id: str,
    source_artifact_ref: str,
    source_lane: str,
    reasoning_kind: str,
    upstream_artifact_ids: Sequence[str],
    envelope_id: str,
    envelope_kind: str,
    unresolved_pressure_status: str = "none",
    follow_obligation: Mapping[str, Any] | None = None,
    assumptions: Sequence[str] = (),
) -> dict[str, Any]:
    if unresolved_pressure_status not in {"none", "follow_needed", "hold", "abstain"}:
        raise ValueError("Unsupported unresolved pressure status")
    if follow_obligation is None and unresolved_pressure_status != "none":
        raise ValueError("Non-none unresolved pressure requires follow_obligation")

    return {
        "schema_version": SUITE_NORMALIZED_ARTIFACT_SCHEMA_VERSION,
        "artifact_role": "derived_product",
        "artifact_id": artifact_id,
        "canonical_identity": {
            "identity_class": "sl_reasoner_artifact",
            "identity_key": artifact_id,
            "aliases": [f"sl_reasoner:{reasoning_kind}", f"lane:{source_lane}"],
        },
        "provenance_anchor": {
            "source_system": "SL-reasoner",
            "source_artifact_id": source_artifact_ref,
            "anchor_kind": "reasoner_input_artifact",
            "anchor_ref": source_artifact_ref,
        },
        "context_envelope_ref": {
            "envelope_id": envelope_id,
            "envelope_kind": envelope_kind,
        },
        "authority": {
            "authority_class": "derived_inspection",
            "derived": True,
            "promotion_receipt_ref": None,
        },
        "lineage": {
            "upstream_artifact_ids": list(upstream_artifact_ids),
            "profile_version": REASONER_DERIVED_ARTIFACT_SCHEMA_VERSION,
        },
        "follow_obligation": dict(follow_obligation) if follow_obligation is not None else None,
        "unresolved_pressure_status": unresolved_pressure_status,
        "summary": {
            "reasoning_kind": reasoning_kind,
            "source_lane": source_lane,
            "assumption_count": len([value for value in assumptions if str(value).strip()]),
            "assumptions": [str(value) for value in assumptions if str(value).strip()],
        },
    }
