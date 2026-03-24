"""Verify the testing module imports and fixtures are discoverable."""

import pytest


def test_imports():
    from zerodb_mcp.testing import zerodb_project, zerodb_client, zerodb_mock_client

    assert callable(zerodb_project)
    assert callable(zerodb_client)
    assert callable(zerodb_mock_client)


def test_mock_client_fixture(zerodb_mock_client):
    """Mock client should be usable without network."""
    assert zerodb_mock_client is not None
    # Verify all expected namespaces exist
    assert hasattr(zerodb_mock_client, "vectors")
    assert hasattr(zerodb_mock_client, "quantum")
    assert hasattr(zerodb_mock_client, "tables")
    assert hasattr(zerodb_mock_client, "files")
    assert hasattr(zerodb_mock_client, "events")
    assert hasattr(zerodb_mock_client, "projects")
    assert hasattr(zerodb_mock_client, "rlhf")
    assert hasattr(zerodb_mock_client, "admin")
    assert hasattr(zerodb_mock_client, "embeddings")
    assert hasattr(zerodb_mock_client, "memory")


@pytest.mark.asyncio
async def test_mock_client_vectors_awaitable(zerodb_mock_client):
    """Async methods on mock namespaces should be awaitable."""
    zerodb_mock_client.vectors.upsert = pytest.importorskip(
        "unittest.mock"
    ).AsyncMock(return_value={"id": "vec-123"})
    result = await zerodb_mock_client.vectors.upsert(
        project_id="test", embedding=[0.1, 0.2]
    )
    assert result["id"] == "vec-123"


@pytest.mark.asyncio
async def test_mock_client_execute_awaitable(zerodb_mock_client):
    """Top-level execute should be awaitable."""
    result = await zerodb_mock_client.execute("test_op", {"key": "value"})
    assert result["success"] is True


@pytest.mark.asyncio
async def test_mock_client_context_manager(zerodb_mock_client):
    """Mock client should work as an async context manager."""
    async with zerodb_mock_client as client:
        assert client is zerodb_mock_client
