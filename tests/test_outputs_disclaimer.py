from interpretation.hypotheses import InterpretationHypothesis
from interpretation.outputs import DISCLAIMER, INTERPRETATION_VERSION, to_payload


def test_outputs_carry_disclaimer_and_version():
    payload = to_payload([InterpretationHypothesis(statement="X", assumptions=[])])
    assert payload["version"] == INTERPRETATION_VERSION
    assert payload["disclaimer"] == DISCLAIMER
