import dataclasses

import pytest

from interpretation.hypotheses import InterpretationHypothesis
from interpretation.outputs import DISCLAIMER, INTERPRETATION_VERSION, to_payload


def test_hypothesis_is_frozen():
    hypothesis = InterpretationHypothesis(statement="X", assumptions=[])
    with pytest.raises(dataclasses.FrozenInstanceError):
        hypothesis.statement = "Y"  # type: ignore[misc]


def test_to_payload_includes_defaults():
    hypothesis = InterpretationHypothesis(statement="X", assumptions=["a"])
    payload = to_payload([hypothesis])

    assert payload["version"] == INTERPRETATION_VERSION
    assert payload["disclaimer"] == DISCLAIMER

    assert len(payload["hypotheses"]) == 1
    row = payload["hypotheses"][0]
    assert row["statement"] == "X"
    assert row["assumptions"] == ["a"]
    assert row["confidence"] is None
    assert row["disclaimer"] == hypothesis.disclaimer

