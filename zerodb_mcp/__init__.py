"""
ZeroDB MCP Bridge Python Client SDK

A production-ready Python client for interacting with the ZeroDB MCP Bridge API.
Provides async operations for vectors, quantum computing, tables, files, events,
projects, RLHF, and admin functionality.

Example:
    >>> from zerodb_mcp import ZeroDBClient
    >>>
    >>> async def main():
    ...     client = ZeroDBClient(api_key="your_api_key")
    ...
    ...     # Create a project
    ...     project = await client.projects.create(
    ...         name="My AI Project",
    ...         tier="pro"
    ...     )
    ...
    ...     # Upsert vectors
    ...     result = await client.vectors.upsert(
    ...         project_id=project["project_id"],
    ...         embedding=[0.1, 0.2, 0.3, ...],
    ...         document="Sample document"
    ...     )
"""

__version__ = "1.1.0"
__author__ = "AINative Studio"
__license__ = "MIT"

from .client import ZeroDBClient
from .exceptions import (
    ZeroDBError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError,
    QuotaExceededError,
)
from .models import (
    VectorUpsertRequest,
    VectorSearchRequest,
    VectorSearchResult,
    QuantumCompressionRequest,
    TableCreateRequest,
    FileUploadRequest,
    ProjectCreateRequest,
)

__all__ = [
    # Main client
    "ZeroDBClient",

    # Exceptions
    "ZeroDBError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "ResourceNotFoundError",
    "QuotaExceededError",

    # Models
    "VectorUpsertRequest",
    "VectorSearchRequest",
    "VectorSearchResult",
    "QuantumCompressionRequest",
    "TableCreateRequest",
    "FileUploadRequest",
    "ProjectCreateRequest",
]
