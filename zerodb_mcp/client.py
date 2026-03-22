"""
Main ZeroDB MCP Client
"""

import asyncio
from typing import Dict, Any, Optional
import httpx

from .auth import AuthHandler
from .exceptions import (
    ZeroDBError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError,
    ServerError,
    NetworkError,
    TimeoutError as ZeroDBTimeoutError,
)
from .utils import format_error_message, parse_retry_after

# Import operation modules
from .operations.vectors import VectorOperations
from .operations.quantum import QuantumOperations
from .operations.tables import TableOperations
from .operations.files import FileOperations
from .operations.events import EventOperations
from .operations.projects import ProjectOperations
from .operations.rlhf import RLHFOperations
from .operations.admin import AdminOperations
from .operations.embeddings import EmbeddingOperations
from .operations.memory import MemoryOperations


class ZeroDBClient:
    """
    ZeroDB MCP Bridge Python Client

    A production-ready async client for interacting with the ZeroDB MCP Bridge API.
    Provides comprehensive access to all 60+ operations including vectors, quantum
    computing, NoSQL tables, file storage, events, RLHF, and admin functionality.

    Example:
        >>> client = ZeroDBClient(api_key="your_api_key")
        >>>
        >>> # Create a project
        >>> project = await client.projects.create(
        ...     name="AI Assistant Project",
        ...     tier="pro"
        ... )
        >>>
        >>> # Upsert vectors
        >>> result = await client.vectors.upsert(
        ...     project_id=project["project_id"],
        ...     embedding=[0.1, 0.2, 0.3, ...],
        ...     document="Sample document for semantic search"
        ... )
        >>>
        >>> # Search vectors
        >>> results = await client.vectors.search(
        ...     project_id=project["project_id"],
        ...     query_vector=[0.15, 0.25, 0.35, ...],
        ...     limit=10,
        ...     threshold=0.7
        ... )
        >>>
        >>> # Close client when done
        >>> await client.close()

    Args:
        api_key: ZeroDB API key (or set ZERODB_API_KEY env var)
        jwt_token: JWT authentication token (or set ZERODB_JWT_TOKEN env var)
        base_url: API base URL (default: https://api.ainative.studio)
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retries for failed requests (default: 3)
        retry_delay: Delay between retries in seconds (default: 1.0)

    Attributes:
        vectors: Vector operations (10 operations)
        quantum: Quantum computing operations (6 operations)
        tables: NoSQL table operations (8 operations)
        files: File storage operations (6 operations)
        events: Event operations (5 operations)
        projects: Project management operations (7 operations)
        rlhf: RLHF feedback operations (10 operations)
        admin: Admin operations (5 operations)
        embeddings: Embedding generation operations (6 operations)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        base_url: str = "https://api.ainative.studio",
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        extract_entities: bool = False,
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._extract_entities = extract_entities

        # Initialize authentication
        self.auth = AuthHandler(api_key=api_key, jwt_token=jwt_token)

        # Create HTTP client
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.auth.get_headers(),
            timeout=self.timeout,
            follow_redirects=True,
        )

        # Initialize operation modules
        self.vectors = VectorOperations(self)
        self.quantum = QuantumOperations(self)
        self.tables = TableOperations(self)
        self.files = FileOperations(self)
        self.events = EventOperations(self)
        self.projects = ProjectOperations(self)
        self.rlhf = RLHFOperations(self)
        self.admin = AdminOperations(self)
        self.embeddings = EmbeddingOperations(self)
        self.memory = MemoryOperations(self)

    async def execute(
        self,
        operation: str,
        params: Dict[str, Any],
        retry: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a raw MCP operation

        Args:
            operation: Operation name (e.g., 'upsert_vector')
            params: Operation parameters
            retry: Whether to retry on failure (default: True)

        Returns:
            Operation result as dictionary

        Raises:
            AuthenticationError: Authentication failed
            RateLimitError: Rate limit exceeded
            ValidationError: Invalid parameters
            ZeroDBError: Other API errors
        """
        endpoint = "/api/v1/public/zerodb/mcp/execute"

        payload = {
            "operation": operation,
            "params": params
        }

        retries = self.max_retries if retry else 0
        last_error = None

        for attempt in range(retries + 1):
            try:
                response = await self._client.post(endpoint, json=payload)

                # Handle successful response
                if response.status_code == 200:
                    return response.json()

                # Handle error responses
                await self._handle_error_response(response)

            except httpx.TimeoutException as e:
                last_error = ZeroDBTimeoutError(
                    f"Request timeout after {self.timeout}s",
                    timeout=self.timeout
                )
                if attempt < retries:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise last_error from e

            except httpx.NetworkError as e:
                last_error = NetworkError(f"Network error: {str(e)}")
                if attempt < retries:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise last_error from e

            except (AuthenticationError, RateLimitError, ValidationError):
                # Don't retry auth/rate limit/validation errors
                raise

            except Exception as e:
                if attempt < retries:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise ZeroDBError(f"Unexpected error: {str(e)}") from e

        # Should not reach here, but just in case
        if last_error:
            raise last_error
        raise ZeroDBError("Request failed after retries")

    async def _handle_error_response(self, response: httpx.Response) -> None:
        """Handle error responses from API"""
        try:
            error_data = response.json()
        except Exception:
            error_data = {"detail": response.text}

        error_message = format_error_message(error_data)

        # Authentication errors
        if response.status_code == 401:
            raise AuthenticationError(error_message, response_data=error_data)

        # Rate limiting
        if response.status_code == 429:
            retry_after = parse_retry_after(response.headers.get('Retry-After'))
            raise RateLimitError(
                error_message,
                retry_after=retry_after,
                response_data=error_data
            )

        # Validation errors
        if response.status_code == 422:
            raise ValidationError(
                error_message,
                errors=error_data.get('detail'),
                response_data=error_data
            )

        # Not found
        if response.status_code == 404:
            raise ResourceNotFoundError(
                resource_type="Resource",
                resource_id="unknown",
                response_data=error_data
            )

        # Server errors
        if response.status_code >= 500:
            raise ServerError(error_message, response_data=error_data)

        # Generic error
        raise ZeroDBError(
            error_message,
            status_code=response.status_code,
            response_data=error_data
        )

    async def health_check(self) -> Dict[str, Any]:
        """
        Check API health status

        Returns:
            Health check response with status and version info
        """
        try:
            response = await self._client.get("/api/v1/public/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    async def get_operations(self) -> Dict[str, Any]:
        """
        Get list of available MCP operations

        Returns:
            Dictionary of available operations with descriptions
        """
        endpoint = "/api/v1/public/zerodb/mcp/operations"
        response = await self._client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def update_auth_token(self, jwt_token: str, expires_in: Optional[int] = None):
        """
        Update JWT authentication token

        Useful for token refresh workflows.

        Args:
            jwt_token: New JWT token
            expires_in: Token expiry in seconds (optional)
        """
        self.auth.update_jwt_token(jwt_token, expires_in)
        self._client.headers.update(self.auth.get_headers())

    async def close(self):
        """Close the HTTP client and cleanup resources"""
        await self._client.aclose()

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    def __repr__(self):
        return (
            f"ZeroDBClient(base_url='{self.base_url}', "
            f"auth_type='{self.auth.auth_type}')"
        )
