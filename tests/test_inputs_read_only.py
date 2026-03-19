import pytest

from interpretation.inputs import as_read_only


def test_as_read_only_returns_read_only_mapping():
    src = {"a": 1}
    ro = as_read_only(src)

    assert ro["a"] == 1
    with pytest.raises(TypeError):
        ro["a"] = 2  # type: ignore[misc]


def test_as_read_only_is_shallow_copy_not_live_view():
    src = {"a": 1}
    ro = as_read_only(src)

    src["a"] = 999
    assert ro["a"] == 1

