"""
ZeroDB MCP SDK -- Testing utilities and pytest fixtures.

Usage in conftest.py:
    from zerodb_mcp.testing import zerodb_project, zerodb_client, zerodb_mock_client

Usage in tests:
    @pytest.mark.asyncio
    async def test_vector_store(zerodb_client):
        result = await zerodb_client.vectors.upsert(...)
        assert result.id is not None
"""

import os
from typing import Tuple
from unittest.mock import AsyncMock, MagicMock

import pytest
import httpx


@pytest.fixture(scope="session")
async def zerodb_project() -> Tuple[str, str, str]:
    """
    Session-scoped fixture that provisions a temporary ZeroDB project
    via the instant-db endpoint.

    Yields:
        Tuple of (api_key, project_id, base_url)

    Skips the test if the instant-db endpoint is unreachable or
    ZERODB_TEST_BASE_URL is not configured.
    """
    base_url = os.getenv("ZERODB_TEST_BASE_URL", "https://api.ainative.studio")
    api_key = os.getenv("ZERODB_TEST_API_KEY")

    if not api_key:
        pytest.skip(
            "ZERODB_TEST_API_KEY not set -- skipping integration test "
            "(set ZERODB_TEST_API_KEY and optionally ZERODB_TEST_BASE_URL)"
        )

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    project_id = None
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as http:
        # Provision a temporary project
        try:
            resp = await http.post("/api/v1/public/instant-db", headers=headers, json={})
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            pytest.skip(f"ZeroDB instant-db endpoint unreachable: {exc}")

        if resp.status_code != 200:
            pytest.skip(
                f"instant-db returned {resp.status_code}: {resp.text}"
            )

        data = resp.json()
        project_api_key = data.get("api_key", api_key)
        project_id = data.get("project_id")

        if not project_id:
            pytest.skip("instant-db response missing project_id")

        yield (project_api_key, project_id, base_url)

        # Teardown -- attempt to delete the temporary project
        try:
            await http.delete(
                f"/api/v1/public/zerodb/mcp/execute",
                headers=headers,
                json={
                    "operation": "delete_project",
                    "params": {"project_id": project_id},
                },
            )
        except Exception:
            # Best-effort cleanup; don't fail the suite on teardown errors
            pass


@pytest.fixture
async def zerodb_client(zerodb_project):
    """
    Function-scoped fixture that returns a configured ``ZeroDBClient``
    using credentials from the ``zerodb_project`` fixture.

    The client is automatically closed after each test.
    """
    from zerodb_mcp.client import ZeroDBClient

    api_key, project_id, base_url = zerodb_project
    client = ZeroDBClient(api_key=api_key, base_url=base_url)
    # Stash the project_id so tests can reference it conveniently
    client._test_project_id = project_id
    yield client
    await client.close()


class _OperationsMock(MagicMock):
    """A MagicMock where any undefined attribute returns an AsyncMock."""

    def _get_child_mock(self, /, **kw):
        return AsyncMock(**kw)


@pytest.fixture
def zerodb_mock_client() -> MagicMock:
    """
    Function-scoped fixture providing a mock ``ZeroDBClient`` suitable
    for pure unit tests with no network calls.

    The mock exposes the same top-level namespace attributes as the real
    client: ``vectors``, ``quantum``, ``tables``, ``files``, ``events``,
    ``projects``, ``rlhf``, ``admin``, ``embeddings``, and ``memory``.
    Every method on these namespaces is an ``AsyncMock`` that returns
    ``{"success": True, "data": {}}``.

    Example::

        async def test_something(zerodb_mock_client):
            zerodb_mock_client.vectors.upsert.return_value = {"id": "vec-1"}
            result = await zerodb_mock_client.vectors.upsert(project_id="p", embedding=[0.1])
            assert result["id"] == "vec-1"
    """
    mock = MagicMock()
    mock.base_url = "https://mock.ainative.studio"

    # Create operation namespace mocks
    namespace_names = [
        "vectors",
        "quantum",
        "tables",
        "files",
        "events",
        "projects",
        "rlhf",
        "admin",
        "embeddings",
        "memory",
    ]
    for ns in namespace_names:
        setattr(mock, ns, _OperationsMock())

    # Mock top-level async helpers
    mock.execute = AsyncMock(return_value={"success": True, "data": {}})
    mock.health_check = AsyncMock(return_value={"status": "ok"})
    mock.get_operations = AsyncMock(return_value={"operations": []})
    mock.close = AsyncMock()

    # Support async context manager
    mock.__aenter__ = AsyncMock(return_value=mock)
    mock.__aexit__ = AsyncMock(return_value=False)

    return mock
