"""
Output helpers for interpretive payloads.

All outputs must carry a disclaimer and remain separate from core schemas.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from interpretation.hypotheses import InterpretationHypothesis

INTERPRETATION_VERSION = "interpretation.v0.experimental"
DISCLAIMER = "Interpretive and non-authoritative; do not treat as legal advice."


def to_payload(hypotheses: list[InterpretationHypothesis]) -> Mapping[str, Any]:
    return {
        "version": INTERPRETATION_VERSION,
        "disclaimer": DISCLAIMER,
        "hypotheses": [asdict(h) for h in hypotheses],
    }
