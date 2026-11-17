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

__version__ = "1.3.0"
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
from .x402 import (
    parse_x402_payment_header,
    parse_x402_payment_header_or_raise,
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

    # x402 payment protocol
    "parse_x402_payment_header",
    "parse_x402_payment_header_or_raise",

    # LangChain integration (optional, requires the `langchain` extra)
    "ZeroDBEmbeddings",
]


def __getattr__(name):
    """
    Refs #4: lazily import ZeroDBEmbeddings so that importing this package
    at all does not require langchain-core to be installed. `langchain_core`
    is only needed if a caller actually uses ZeroDBEmbeddings -- install it
    via `pip install zerodb-mcp[langchain]`. A plain `from zerodb_mcp import
    ZeroDBClient` must keep working with zero extra dependencies.
    """
    if name == "ZeroDBEmbeddings":
        try:
            from .langchain_embeddings import ZeroDBEmbeddings
        except ImportError as exc:
            raise ImportError(
                "ZeroDBEmbeddings requires the 'langchain' extra: "
                "pip install zerodb-mcp[langchain]"
            ) from exc
        return ZeroDBEmbeddings
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
