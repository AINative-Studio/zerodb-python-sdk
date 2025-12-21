"""
Embedding operations for ZeroDB MCP Client

Provides 6 embedding operations via Railway self-hosted HuggingFace service:
1. generate - Generate embeddings for texts
2. embed_and_store - Generate embeddings and store in ZeroDB
3. semantic_search - Text-based semantic search
4. list_models - List available embedding models
5. health_check - Check embedding service health
6. get_usage - Get embedding usage statistics
"""

from typing import Any, Dict, List, Optional


class EmbeddingOperations:
    """Embedding generation and search operations (FREE via Railway HuggingFace)"""

    def __init__(self, client):
        self._client = client

    async def generate(
        self,
        texts: List[str],
        model: str = "BAAI/bge-small-en-v1.5",
        normalize: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate embeddings for texts using Railway HuggingFace service

        Uses FREE self-hosted HuggingFace service via Railway with
        BAAI/bge-small-en-v1.5 model (384 dimensions).

        Args:
            texts: List of texts to embed (max 100)
            model: Embedding model to use (default: BAAI/bge-small-en-v1.5)
            normalize: Normalize embeddings to unit length (default: True)

        Returns:
            {
                "embeddings": [[0.1, 0.2, ...], ...],
                "model": "BAAI/bge-small-en-v1.5",
                "dimensions": 384,
                "count": 2,
                "processing_time_ms": 125.5,
                "cost_usd": 0.0  # FREE!
            }

        Raises:
            ValueError: Invalid parameters
            ZeroDBError: API error

        Example:
            >>> embeddings = await client.embeddings.generate(
            ...     texts=["Machine learning tutorial", "Python programming guide"],
            ...     model="BAAI/bge-small-en-v1.5",
            ...     normalize=True
            ... )
            >>> print(f"Generated {len(embeddings['embeddings'])} embeddings")
            >>> print(f"Dimensions: {embeddings['dimensions']}")
            >>> print(f"Cost: ${embeddings['cost_usd']}")  # Always $0.00
        """
        if not texts:
            raise ValueError("texts list cannot be empty")

        if len(texts) > 100:
            raise ValueError("Maximum 100 texts per request")

        params = {"texts": texts, "model": model, "normalize": normalize}

        return await self._client.execute("generate_embeddings", params)

    async def embed_and_store(
        self,
        project_id: str,
        texts: List[str],
        metadata_list: Optional[List[Dict[str, Any]]] = None,
        namespace: str = "default",
        model: str = "BAAI/bge-small-en-v1.5",
    ) -> Dict[str, Any]:
        """
        Generate embeddings and store in ZeroDB (one-step workflow)

        Combines embedding generation with vector storage in a single operation.
        Automatically embeds texts and stores them in your ZeroDB vectors.

        Args:
            project_id: Project ID (UUID string)
            texts: List of texts to embed and store (max 100)
            metadata_list: Optional metadata for each text (must match texts length)
            namespace: Vector namespace (default: "default")
            model: Embedding model to use (default: BAAI/bge-small-en-v1.5)

        Returns:
            {
                "success": True,
                "vectors_stored": 100,
                "embeddings_generated": 100,
                "model": "BAAI/bge-small-en-v1.5",
                "dimensions": 384,
                "namespace": "default",
                "processing_time_ms": 350.2
            }

        Raises:
            ValueError: Invalid parameters
            ZeroDBError: API error

        Example:
            >>> texts = [
            ...     "Introduction to machine learning",
            ...     "Advanced deep learning techniques",
            ...     "Natural language processing basics"
            ... ]
            >>> metadata = [
            ...     {"category": "ml", "difficulty": "beginner"},
            ...     {"category": "dl", "difficulty": "advanced"},
            ...     {"category": "nlp", "difficulty": "beginner"}
            ... ]
            >>> result = await client.embeddings.embed_and_store(
            ...     project_id="550e8400-e29b-41d4-a716-446655440000",
            ...     texts=texts,
            ...     metadata_list=metadata,
            ...     namespace="tutorials"
            ... )
            >>> print(f"Stored {result['vectors_stored']} vectors")
        """
        if not texts:
            raise ValueError("texts list cannot be empty")

        if len(texts) > 100:
            raise ValueError("Maximum 100 texts per request")

        if metadata_list and len(metadata_list) != len(texts):
            raise ValueError("metadata_list length must match texts length")

        params = {
            "project_id": project_id,
            "texts": texts,
            "metadata_list": metadata_list or [],
            "namespace": namespace,
            "model": model,
        }

        return await self._client.execute("embed_and_store", params)

    async def semantic_search(
        self,
        project_id: str,
        query: str,
        limit: int = 10,
        threshold: float = 0.7,
        namespace: str = "default",
        filter_metadata: Optional[Dict[str, Any]] = None,
        model: str = "BAAI/bge-small-en-v1.5",
    ) -> Dict[str, Any]:
        """
        Text-based semantic search (auto-embed query + search)

        Performs semantic search using natural language queries. Automatically
        generates embedding for the query text and searches your vector database.

        Args:
            project_id: Project ID (UUID string)
            query: Natural language search query
            limit: Maximum results (1-100, default: 10)
            threshold: Similarity threshold (0.0-1.0, default: 0.7)
            namespace: Vector namespace to search (default: "default")
            filter_metadata: Optional metadata filters (MongoDB-style)
            model: Embedding model to use (default: BAAI/bge-small-en-v1.5)

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
                "query": "What is quantum computing?",
                "total_results": 10,
                "model": "BAAI/bge-small-en-v1.5",
                "processing_time_ms": 200.5
            }

        Raises:
            ValueError: Invalid parameters
            ZeroDBError: API error

        Example:
            >>> results = await client.embeddings.semantic_search(
            ...     project_id="550e8400-e29b-41d4-a716-446655440000",
            ...     query="How do I train a neural network?",
            ...     limit=5,
            ...     threshold=0.8,
            ...     filter_metadata={"category": "ml"}
            ... )
            >>> for result in results["results"]:
            ...     print(f"{result['document']}: {result['similarity']}")
        """
        if not query:
            raise ValueError("query cannot be empty")

        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0.0 and 1.0")

        params = {
            "project_id": project_id,
            "query": query,
            "limit": limit,
            "threshold": threshold,
            "namespace": namespace,
            "model": model,
        }

        if filter_metadata:
            params["filter_metadata"] = filter_metadata

        return await self._client.execute("semantic_search", params)

    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List available embedding models

        Returns information about available embedding models including
        dimensions, speed, and whether they're currently loaded.

        Returns:
            [
                {
                    "id": "BAAI/bge-small-en-v1.5",
                    "dimensions": 384,
                    "description": "Modern, efficient, high quality (DEFAULT)",
                    "speed": "⚡⚡⚡ Very Fast",
                    "loaded": True,
                    "cost_per_1k": 0.0
                }
            ]

        Raises:
            ZeroDBError: API error

        Example:
            >>> models = await client.embeddings.list_models()
            >>> for model in models:
            ...     print(f"{model['id']}: {model['dimensions']} dims, {model['speed']}")
        """
        return await self._client.execute("list_embedding_models", {})

    async def health_check(self) -> Dict[str, Any]:
        """
        Check embedding service health

        Verifies that the Railway HuggingFace embedding service is running
        and responding correctly.

        Returns:
            {
                "status": "healthy",
                "embedding_service": {
                    "status": "running",
                    "model_loaded": True
                },
                "url": "http://embedding-service.railway.internal:8000",
                "cost_per_embedding": 0.0
            }

        Raises:
            ZeroDBError: API error

        Example:
            >>> health = await client.embeddings.health_check()
            >>> print(f"Service status: {health['status']}")
            >>> print(f"Model loaded: {health['embedding_service']['model_loaded']}")
        """
        return await self._client.execute("embedding_health_check", {})

    async def get_usage(self) -> Dict[str, Any]:
        """
        Get embedding usage statistics

        Returns embedding generation statistics for the current user.
        Since embeddings are FREE (self-hosted), cost is always $0.00.

        Returns:
            {
                "user_id": "uuid",
                "embeddings_generated_today": 1000,
                "embeddings_generated_month": 50000,
                "cost_today_usd": 0.0,  # Always FREE
                "cost_month_usd": 0.0,  # Always FREE
                "model": "BAAI/bge-small-en-v1.5",
                "service": "Railway Self-Hosted (FREE)"
            }

        Raises:
            ZeroDBError: API error

        Example:
            >>> usage = await client.embeddings.get_usage()
            >>> print(f"Embeddings today: {usage['embeddings_generated_today']}")
            >>> print(f"Embeddings this month: {usage['embeddings_generated_month']}")
            >>> print(f"Total cost: ${usage['cost_month_usd']}")  # Always $0.00
        """
        return await self._client.execute("embedding_usage", {})
