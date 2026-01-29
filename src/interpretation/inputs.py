"""
Adapters for ingesting core payloads in a read-only manner.

Implementation intentionally deferred until interpretation experiments begin.
When implemented, adapters must:
- accept already-materialized core payload dicts
- never mutate inputs in-place
- record hashes/provenance for traceability
"""

from __future__ import annotations

from typing import Any, Mapping


def as_read_only(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the payload as-is; callers must not mutate the result."""
    return payload
