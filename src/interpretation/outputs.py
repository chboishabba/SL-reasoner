"""
Output helpers for interpretive payloads.

All outputs must carry a disclaimer and remain separate from core schemas.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from interpretation.contracts import build_reasoner_derived_artifact
from interpretation.hypotheses import InterpretationHypothesis

INTERPRETATION_VERSION = "interpretation.v0.experimental"
DISCLAIMER = "Interpretive and non-authoritative; do not treat as legal advice."


def to_payload(hypotheses: list[InterpretationHypothesis]) -> Mapping[str, Any]:
    return {
        "version": INTERPRETATION_VERSION,
        "disclaimer": DISCLAIMER,
        "hypotheses": [asdict(h) for h in hypotheses],
    }


def to_derived_artifact(
    *,
    artifact_id: str,
    source_artifact_ref: str,
    source_lane: str,
    reasoning_kind: str,
    upstream_artifact_ids: list[str],
    envelope_id: str,
    envelope_kind: str,
    hypotheses: list[InterpretationHypothesis],
    unresolved_pressure_status: str = "none",
    follow_obligation: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    return build_reasoner_derived_artifact(
        artifact_id=artifact_id,
        source_artifact_ref=source_artifact_ref,
        source_lane=source_lane,
        reasoning_kind=reasoning_kind,
        upstream_artifact_ids=upstream_artifact_ids,
        envelope_id=envelope_id,
        envelope_kind=envelope_kind,
        unresolved_pressure_status=unresolved_pressure_status,
        follow_obligation=follow_obligation,
        assumptions=[item for hypothesis in hypotheses for item in hypothesis.assumptions],
    )
