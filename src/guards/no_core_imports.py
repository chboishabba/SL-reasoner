"""
Guard helpers to discourage importing core SensibLaw modules for mutation.

Tests can import this module to assert that interpretation code avoids
forbidden imports such as `from sensiblaw import obligations`.
"""

FORBIDDEN_IMPORT_SUBSTRINGS = [
    "from sensiblaw import obligations",
    "from sensiblaw import activation",
    "import sensiblaw.obligations",
    "import sensiblaw.activation",
]
