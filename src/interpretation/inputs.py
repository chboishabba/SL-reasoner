"""
Adapters for ingesting core payloads in a read-only manner.

Implementation intentionally deferred until interpretation experiments begin.
When implemented, adapters must:
- accept already-materialized core payload dicts
- never mutate inputs in-place
- record hashes/provenance for traceability
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from interpretation.contracts import validate_reasoner_input_artifact


def as_read_only(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """
    Return a shallow read-only view of the payload.

    This enforces a minimal "read-only" boundary for the interpretive layer:
    callers cannot mutate the returned mapping in-place. (Nested values may
    still be mutable; deep-freezing is intentionally out of scope here.)
    """
    return MappingProxyType(dict(payload))


def as_reasoner_input(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """
    Return a validated, read-only reasoner input artifact.

    This is the approved deferred seam from producer-owned deterministic
    reducers into `SL-reasoner`. It validates only the boundary contract and
    keeps the payload read-only at the top level.
    """

    validate_reasoner_input_artifact(payload)
    return as_read_only(payload)
