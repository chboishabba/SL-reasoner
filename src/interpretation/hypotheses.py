"""
Data shapes for interpretive hypotheses (non-authoritative).

These are placeholders to be versioned separately as interpretation.v0.*
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class InterpretationHypothesis:
    statement: str
    assumptions: List[str]
    confidence: Optional[float] = None
    disclaimer: str = "Interpretive and non-authoritative."
