from pathlib import Path

import pytest

from guards.no_core_imports import FORBIDDEN_IMPORT_SUBSTRINGS


@pytest.mark.parametrize("pattern", FORBIDDEN_IMPORT_SUBSTRINGS)
def test_no_forbidden_core_imports(pattern: str):
    """Fail fast if interpretation code imports core SensibLaw modules for mutation."""
    files = Path("src").rglob("*.py")
    for file in files:
        if file.name == "no_core_imports.py":
            continue  # pattern definitions live here; ignore self
        text = file.read_text(encoding="utf-8")
        assert pattern not in text, f"Forbidden import found in {file}: {pattern}"
