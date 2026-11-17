"""
Refs #4: the README's `from zerodb_mcp import ZeroDBClient, ZeroDBEmbeddings`
example raised ImportError on the real published package, because
ZeroDBEmbeddings was never exported from zerodb_mcp/__init__.py. Fixing that
naively (an eager `from .langchain_embeddings import ZeroDBEmbeddings` at
module level) would introduce a second, worse regression: langchain_core is
not declared anywhere as a dependency, so importing zerodb_mcp at all would
then unconditionally require it.

These tests cover both required behaviors: ZeroDBEmbeddings importable when
langchain-core is installed, and plain `import zerodb_mcp` / `from
zerodb_mcp import ZeroDBClient` never requiring it.
"""

import subprocess
import sys

import pytest


def test_zerodb_client_imports_without_langchain_core():
    """
    `from zerodb_mcp import ZeroDBClient` must succeed even if langchain_core
    were not installed. Run in a subprocess with langchain_core hidden from
    sys.modules via a stub-free import, so this test fails loudly if
    __init__.py ever goes back to an eager top-level import.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.modules['langchain_core'] = None; "
            "from zerodb_mcp import ZeroDBClient; print('ok')",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout


def test_zerodb_embeddings_is_importable():
    """ZeroDBEmbeddings must be importable from the top-level package."""
    from zerodb_mcp import ZeroDBEmbeddings

    assert ZeroDBEmbeddings.__name__ == "ZeroDBEmbeddings"


def test_zerodb_embeddings_in_dunder_all():
    import zerodb_mcp

    assert "ZeroDBEmbeddings" in zerodb_mcp.__all__


def test_unknown_attribute_still_raises_attribute_error():
    import zerodb_mcp

    with pytest.raises(AttributeError):
        zerodb_mcp.ThisDoesNotExist
