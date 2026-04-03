import json

import pytest

from interpretation.contracts import (
    REASONER_DERIVED_ARTIFACT_SCHEMA_VERSION,
    REASONER_INPUT_ARTIFACT_SCHEMA_VERSION,
    build_reasoner_derived_artifact,
    validate_reasoner_input_artifact,
)
from interpretation.hypotheses import InterpretationHypothesis
from interpretation.inputs import as_reasoner_input
from interpretation.outputs import to_derived_artifact


def _reasoner_input_fixture() -> dict:
    return {
        "schema_version": REASONER_INPUT_ARTIFACT_SCHEMA_VERSION,
        "source_system": "SensibLaw",
        "source_lane": "au",
        "source_artifact_ref": "au.fact_review_bundle:run-1",
        "artifact_role": "derived_product",
        "reasoner_scope": {
            "allowed_outputs": ["derived_product", "bounded_union_surface"],
            "forbidden_outputs": ["promoted_record", "compiled_state"],
            "allowed_operations": ["explanation", "comparison", "hypothesis", "follow_planning"],
            "forbidden_operations": ["promotion", "canonical_write", "state_reduction"],
        },
        "normalized_artifact": {
            "schema_version": "itir.normalized.artifact.v1",
            "artifact_role": "derived_product",
            "artifact_id": "au.fact_review_bundle:run-1",
            "canonical_identity": {"identity_class": "fact_review_run", "identity_key": "run-1"},
            "provenance_anchor": {
                "source_system": "SensibLaw",
                "source_artifact_id": "run-1",
                "anchor_kind": "semantic_run_id",
            },
            "context_envelope_ref": {"envelope_id": "run-1", "envelope_kind": "au_semantic"},
            "authority": {
                "authority_class": "derived_inspection",
                "derived": True,
                "promotion_receipt_ref": None,
            },
            "lineage": {"upstream_artifact_ids": ["run-1"], "profile_version": "sl.compiler_contract.v0_1"},
            "follow_obligation": None,
            "unresolved_pressure_status": "hold",
        },
        "compiler_contract": {"lane": "au"},
        "promotion_gate": {"decision": "audit", "reason": "mixed_promote_review_or_abstain_pressure"},
        "summary": {"gate_decision": "audit"},
    }


def test_reasoner_input_artifact_is_validated_and_read_only() -> None:
    payload = _reasoner_input_fixture()
    validate_reasoner_input_artifact(payload)
    ro = as_reasoner_input(payload)

    assert ro["source_system"] == "SensibLaw"
    with pytest.raises(TypeError):
        ro["source_system"] = "other"  # type: ignore[misc]


def test_reasoner_input_artifact_rejects_non_reasoner_roles() -> None:
    payload = _reasoner_input_fixture()
    payload["normalized_artifact"]["artifact_role"] = "compiled_state"

    with pytest.raises(ValueError, match="not allowed"):
        validate_reasoner_input_artifact(payload)


def test_reasoner_derived_artifact_is_always_non_authoritative() -> None:
    artifact = build_reasoner_derived_artifact(
        artifact_id="sl.reasoner:test-1",
        source_artifact_ref="au.fact_review_bundle:run-1",
        source_lane="au",
        reasoning_kind="explanation",
        upstream_artifact_ids=["au.fact_review_bundle:run-1"],
        envelope_id="run-1",
        envelope_kind="au_semantic",
        assumptions=["A"],
    )

    assert artifact["schema_version"] == "itir.normalized.artifact.v1"
    assert artifact["artifact_role"] == "derived_product"
    assert artifact["authority"]["authority_class"] == "derived_inspection"
    assert artifact["authority"]["derived"] is True
    assert artifact["authority"]["promotion_receipt_ref"] is None
    assert artifact["lineage"]["profile_version"] == REASONER_DERIVED_ARTIFACT_SCHEMA_VERSION


def test_reasoner_derived_artifact_requires_follow_metadata_when_pressure_open() -> None:
    with pytest.raises(ValueError, match="requires follow_obligation"):
        build_reasoner_derived_artifact(
            artifact_id="sl.reasoner:test-2",
            source_artifact_ref="au.fact_review_bundle:run-1",
            source_lane="au",
            reasoning_kind="follow_planning",
            upstream_artifact_ids=["au.fact_review_bundle:run-1"],
            envelope_id="run-1",
            envelope_kind="au_semantic",
            unresolved_pressure_status="hold",
        )


def test_to_derived_artifact_uses_hypothesis_assumptions() -> None:
    payload = to_derived_artifact(
        artifact_id="sl.reasoner:test-3",
        source_artifact_ref="au.fact_review_bundle:run-1",
        source_lane="au",
        reasoning_kind="comparison",
        upstream_artifact_ids=["au.fact_review_bundle:run-1"],
        envelope_id="run-1",
        envelope_kind="au_semantic",
        hypotheses=[InterpretationHypothesis(statement="X", assumptions=["A1", "A2"])],
    )

    json.dumps(payload)
    assert payload["summary"]["reasoning_kind"] == "comparison"
    assert payload["summary"]["assumption_count"] == 2
