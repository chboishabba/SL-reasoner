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
    "from src.storage.versioned_store import",
    "from src.transcript_semantic.semantic import",
    "from src.au_semantic.semantic import",
    "from src.gwb_us_law.semantic import",
    "from src.logic_tree import",
    "from src.pipeline import",
    "from src.policy.product_gate import",
    "from src.policy.compiler_contract import",
]
