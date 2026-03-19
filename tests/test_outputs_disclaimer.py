import json

from interpretation.hypotheses import InterpretationHypothesis
from interpretation.outputs import DISCLAIMER, INTERPRETATION_VERSION, to_payload


def test_outputs_carry_disclaimer_and_version():
    payload = to_payload([InterpretationHypothesis(statement="X", assumptions=[])])
    assert payload["version"] == INTERPRETATION_VERSION
    assert payload["disclaimer"] == DISCLAIMER


def test_output_payload_is_json_serializable_and_hypotheses_have_disclaimer():
    payload = to_payload(
        [
            InterpretationHypothesis(
                statement="X means Y under condition Z",
                assumptions=["Condition Z holds"],
                confidence=0.5,
            )
        ]
    )

    json.dumps(payload)  # must not raise

    hypotheses = payload["hypotheses"]
    assert isinstance(hypotheses, list)
    assert hypotheses and isinstance(hypotheses[0], dict)
    assert hypotheses[0]["statement"] == "X means Y under condition Z"
    assert "disclaimer" in hypotheses[0]
    assert "non-authoritative" in hypotheses[0]["disclaimer"]


def test_interpretation_version_is_namespaced_and_experimental():
    assert INTERPRETATION_VERSION.startswith("interpretation.v")
    assert "experimental" in INTERPRETATION_VERSION
