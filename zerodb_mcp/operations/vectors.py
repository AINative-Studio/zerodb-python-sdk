"""
Vector operations for ZeroDB MCP Client

Provides 10 vector operations:
1. upsert - Store or update a vector
2. batch_upsert - Batch upsert multiple vectors
3. search - Semantic vector search
4. delete - Delete a vector
5. get - Get vector by ID
6. list - List vectors with pagination
7. stats - Get vector statistics
8. create_index - Create vector index
9. optimize_storage - Optimize vector storage
10. export - Export vectors
"""

from typing import Dict, Any, List, Optional
from ..utils import validate_embedding, validate_uuid, build_query_params


class VectorOperations:
    """Vector storage and search operations"""

    def __init__(self, client):
        self._client = client

    async def upsert(
        self,
        project_id: str,
        embedding: List[float],
        document: str,
        namespace: str = "default",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store or update a vector in ZeroDB

        Args:
            project_id: Project ID (UUID string)
            embedding: Vector embedding (list of floats, max 4096 dimensions)
            document: Associated document text
            namespace: Vector namespace (default: "default")
            metadata: Optional metadata dictionary

        Returns:
            {
                "vector_id": "uuid",
                "status": "success"
            }

        Raises:
            ValueError: Invalid parameters
            ZeroDBError: API error

        Example:
            >>> result = await client.vectors.upsert(
            ...     project_id="550e8400-e29b-41d4-a716-446655440000",
            ...     embedding=[0.1, 0.2, 0.3, ...],
            ...     document="Machine learning tutorial",
            ...     metadata={"category": "education", "language": "en"}
            ... )
        """
        validate_embedding(embedding)

        params = {
            "project_id": project_id,
            "embedding": embedding,
            "document": document,
            "namespace": namespace,
            "metadata": metadata or {}
        }

        return await self._client.execute("upsert_vector", params)

    async def batch_upsert(
        self,
        project_id: str,
        vectors: List[Dict[str, Any]],
        namespace: str = "default"
    ) -> Dict[str, Any]:
        """
        Batch upsert multiple vectors

        Args:
            project_id: Project ID
            vectors: List of vector dicts with 'embedding', 'document', 'metadata'
            namespace: Vector namespace (default: "default")

        Returns:
            {
                "total": 100,
                "successful": 98,
                "failed": 2,
                "errors": [...]
            }

        Example:
            >>> vectors = [
            ...     {
            ...         "embedding": [0.1, 0.2, ...],
            ...         "document": "First doc",
            ...         "metadata": {"id": 1}
            ...     },
            ...     {
            ...         "embedding": [0.3, 0.4, ...],
            ...         "document": "Second doc",
            ...         "metadata": {"id": 2}
            ...     }
            ... ]
            >>> result = await client.vectors.batch_upsert(
            ...     project_id="550e8400-...",
            ...     vectors=vectors
            ... )
        """
        if not vectors:
            raise ValueError("Vectors list cannot be empty")

        if len(vectors) > 1000:
            raise ValueError("Maximum 1000 vectors per batch")

        # Validate all vectors
        for i, vec in enumerate(vectors):
            if 'embedding' not in vec or 'document' not in vec:
                raise ValueError(f"Vector {i} missing required fields")
            validate_embedding(vec['embedding'])

        params = {
            "project_id": project_id,
            "vectors": vectors,
            "namespace": namespace
        }

        return await self._client.execute("batch_upsert_vectors", params)

    async def search(
        self,
        project_id: str,
        query_vector: List[float],
        limit: int = 10,
        threshold: float = 0.7,
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Semantic vector search

        Args:
            project_id: Project ID
            query_vector: Query embedding
            limit: Maximum results (1-1000, default: 10)
            threshold: Similarity threshold (0.0-1.0, default: 0.7)
            namespace: Optional namespace filter

        Returns:
            {
                "results": [
                    {
                        "vector_id": "uuid",
                        "similarity": 0.95,
                        "document": "text",
                        "metadata": {...},
                        "namespace": "default"
                    }
                ],
                "total": 10
            }

        Example:
            >>> results = await client.vectors.search(
            ...     project_id="550e8400-...",
            ...     query_vector=[0.15, 0.25, 0.35, ...],
            ...     limit=20,
            ...     threshold=0.8
            ... )
            >>> for result in results["results"]:
            ...     print(f"{result['document']}: {result['similarity']}")
        """
        validate_embedding(query_vector)

        if not 1 <= limit <= 1000:
            raise ValueError("Limit must be between 1 and 1000")

        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")

        params = {
            "project_id": project_id,
            "query_vector": query_vector,
            "limit": limit,
            "threshold": threshold
        }

        if namespace:
            params["namespace"] = namespace

        return await self._client.execute("search_vectors", params)

    async def delete(
        self,
        project_id: str,
        vector_id: str
    ) -> Dict[str, Any]:
        """
        Delete a vector by ID

        Args:
            project_id: Project ID
            vector_id: Vector ID to delete

        Returns:
            {"status": "success"}

        Example:
            >>> await client.vectors.delete(
            ...     project_id="550e8400-...",
            ...     vector_id="660e8400-..."
            ... )
        """
        params = {
            "project_id": project_id,
            "vector_id": vector_id
        }

        return await self._client.execute("delete_vector", params)

    async def get(
        self,
        project_id: str,
        vector_id: str
    ) -> Dict[str, Any]:
        """
        Get vector by ID

        Args:
            project_id: Project ID
            vector_id: Vector ID

        Returns:
            {
                "vector_id": "uuid",
                "embedding": [...],
                "document": "text",
                "metadata": {...},
                "namespace": "default"
            }

        Example:
            >>> vector = await client.vectors.get(
            ...     project_id="550e8400-...",
            ...     vector_id="660e8400-..."
            ... )
        """
        params = {
            "project_id": project_id,
            "vector_id": vector_id
        }

        return await self._client.execute("get_vector", params)

    async def list(
        self,
        project_id: str,
        limit: int = 100,
        offset: int = 0,
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List vectors with pagination

        Args:
            project_id: Project ID
            limit: Results per page (1-10000, default: 100)
            offset: Number of results to skip (default: 0)
            namespace: Optional namespace filter

        Returns:
            {
                "vectors": [...],
                "total": 1000,
                "limit": 100,
                "offset": 0
            }

        Example:
            >>> page1 = await client.vectors.list(
            ...     project_id="550e8400-...",
            ...     limit=50,
            ...     offset=0
            ... )
            >>> page2 = await client.vectors.list(
            ...     project_id="550e8400-...",
            ...     limit=50,
            ...     offset=50
            ... )
        """
        params = build_query_params(
            limit=limit,
            offset=offset,
            filters={"namespace": namespace} if namespace else None
        )
        params["project_id"] = project_id

        return await self._client.execute("list_vectors", params)

    async def stats(
        self,
        project_id: str,
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get vector statistics

        Args:
            project_id: Project ID
            namespace: Optional namespace filter

        Returns:
            {
                "total_vectors": 10000,
                "dimensions": 1536,
                "namespaces": ["default", "custom"],
                "storage_size_mb": 125.5
            }

        Example:
            >>> stats = await client.vectors.stats(
            ...     project_id="550e8400-..."
            ... )
            >>> print(f"Total vectors: {stats['total_vectors']}")
        """
        params = {"project_id": project_id}
        if namespace:
            params["namespace"] = namespace

        return await self._client.execute("vector_stats", params)

    async def create_index(
        self,
        project_id: str,
        namespace: str = "default",
        index_type: str = "hnsw"
    ) -> Dict[str, Any]:
        """
        Create vector index for faster search

        Args:
            project_id: Project ID
            namespace: Namespace to index
            index_type: Index type (hnsw, ivf, flat)

        Returns:
            {"status": "success", "index_type": "hnsw"}

        Example:
            >>> await client.vectors.create_index(
            ...     project_id="550e8400-...",
            ...     index_type="hnsw"
            ... )
        """
        params = {
            "project_id": project_id,
            "namespace": namespace,
            "index_type": index_type
        }

        return await self._client.execute("create_vector_index", params)

    async def optimize_storage(
        self,
        project_id: str,
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize vector storage (vacuum, reindex)

        Args:
            project_id: Project ID
            namespace: Optional namespace filter

        Returns:
            {
                "status": "success",
                "space_freed_mb": 15.2
            }

        Example:
            >>> result = await client.vectors.optimize_storage(
            ...     project_id="550e8400-..."
            ... )
        """
        params = {"project_id": project_id}
        if namespace:
            params["namespace"] = namespace

        return await self._client.execute("optimize_vector_storage", params)

    async def export(
        self,
        project_id: str,
        namespace: Optional[str] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Export vectors

        Args:
            project_id: Project ID
            namespace: Optional namespace filter
            format: Export format (json, csv, parquet)

        Returns:
            {
                "export_url": "https://...",
                "total_vectors": 1000,
                "expires_at": "2025-01-15T12:00:00Z"
            }

        Example:
            >>> export = await client.vectors.export(
            ...     project_id="550e8400-...",
            ...     format="json"
            ... )
            >>> print(f"Download: {export['export_url']}")
        """
        params = {
            "project_id": project_id,
            "format": format
        }
        if namespace:
            params["namespace"] = namespace

        return await self._client.execute("export_vectors", params)
