"""
LangChain-compatible ZeroDB Embeddings wrapper

Provides FREE embedding generation using ZeroDB's Railway-hosted HuggingFace service.
Compatible with all LangChain vector stores and embedding consumers.

Cost Comparison:
- OpenAI: $0.0001 per 1K tokens = $100/month for 1M embeddings
- Cohere: $0.0001 per 1K tokens = $100/month for 1M embeddings
- ZeroDB: $0.00 (FREE, self-hosted via Railway)

Supported Models:
- BAAI/bge-small-en-v1.5 (384 dims, very fast, DEFAULT)
- sentence-transformers/all-MiniLM-L6-v2 (384 dims, fast)
- sentence-transformers/all-mpnet-base-v2 (768 dims, better quality)
"""

import asyncio
from typing import List, Optional

from langchain_core.embeddings import Embeddings

from zerodb_mcp.client import ZeroDBClient


class ZeroDBEmbeddings(Embeddings):
    """
    LangChain-compatible embeddings using ZeroDB's FREE HuggingFace service

    This class provides a LangChain-compatible interface to ZeroDB's
    self-hosted HuggingFace embedding service running on Railway.

    **Why ZeroDB Embeddings?**
    - **FREE**: $0.00 cost vs $100/month for OpenAI/Cohere at scale
    - **Fast**: Railway-optimized inference with batching
    - **Compatible**: Works with all LangChain vector stores
    - **Privacy**: Self-hosted, your data stays private

    **Usage Example:**

        >>> from zerodb_mcp.langchain_embeddings import ZeroDBEmbeddings
        >>> from langchain_community.vectorstores import Chroma
        >>>
        >>> # Initialize embeddings (FREE!)
        >>> embeddings = ZeroDBEmbeddings(
        ...     api_key="your-api-key",
        ...     model="BAAI/bge-small-en-v1.5"  # 384 dimensions
        ... )
        >>>
        >>> # Embed documents
        >>> docs = ["Machine learning tutorial", "Python programming guide"]
        >>> doc_embeddings = embeddings.embed_documents(docs)
        >>> print(f"Generated {len(doc_embeddings)} embeddings (COST: $0.00)")
        >>>
        >>> # Use with any LangChain vector store
        >>> vectorstore = Chroma.from_documents(
        ...     documents=docs,
        ...     embedding=embeddings  # FREE embeddings!
        ... )

    **Attributes:**
        api_key: ZeroDB API key
        base_url: ZeroDB API base URL (default: https://api.ainative.studio/v1)
        model: Embedding model name (default: BAAI/bge-small-en-v1.5)
        normalize: Normalize embeddings to unit length (default: True)
        batch_size: Maximum texts per batch (default: 100, max: 100)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.ainative.studio/v1",
        model: str = "BAAI/bge-small-en-v1.5",
        normalize: bool = True,
        batch_size: int = 100,
    ):
        """
        Initialize ZeroDB embeddings client

        Args:
            api_key: ZeroDB API key (get from https://www.ainative.studio)
            base_url: ZeroDB API base URL (default: production)
            model: Embedding model to use:
                - "BAAI/bge-small-en-v1.5" (384 dims, very fast, DEFAULT)
                - "sentence-transformers/all-MiniLM-L6-v2" (384 dims, fast)
                - "sentence-transformers/all-mpnet-base-v2" (768 dims, better)
            normalize: Normalize embeddings to unit length (default: True)
            batch_size: Maximum texts per request (max: 100, default: 100)

        Raises:
            ValueError: Invalid parameters
        """
        if not api_key:
            raise ValueError("api_key is required")

        if batch_size < 1 or batch_size > 100:
            raise ValueError("batch_size must be between 1 and 100")

        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.normalize = normalize
        self.batch_size = batch_size

        # Initialize ZeroDB client (sync wrapper for async client)
        self._client: Optional[ZeroDBClient] = None

    def _get_client(self) -> ZeroDBClient:
        """Get or create ZeroDB client"""
        if self._client is None:
            self._client = ZeroDBClient(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        return self._client

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts (internal helper)

        Args:
            texts: List of texts to embed (max 100)

        Returns:
            List of embedding vectors

        Raises:
            ValueError: Invalid parameters
            RuntimeError: API error
        """
        if not texts:
            return []

        if len(texts) > 100:
            raise ValueError(f"Maximum 100 texts per batch, got {len(texts)}")

        client = self._get_client()

        # Run async operation in sync context
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Already in async context, create new loop
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    client.embeddings.generate(
                        texts=texts,
                        model=self.model,
                        normalize=self.normalize,
                    ),
                )
                result = future.result()
        else:
            # Not in async context, use existing loop
            result = loop.run_until_complete(
                client.embeddings.generate(
                    texts=texts,
                    model=self.model,
                    normalize=self.normalize,
                )
            )

        return result.get("embeddings", [])

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed search documents using ZeroDB's FREE HuggingFace service

        This method handles batching automatically if you provide more than
        100 texts. Each batch is processed independently.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (one per text)

        Raises:
            ValueError: Empty texts list
            RuntimeError: API error

        Example:
            >>> embeddings = ZeroDBEmbeddings(api_key="your-key")
            >>> docs = [
            ...     "Introduction to machine learning",
            ...     "Deep learning with neural networks",
            ...     "Natural language processing basics"
            ... ]
            >>> vectors = embeddings.embed_documents(docs)
            >>> print(f"Generated {len(vectors)} embeddings")
            >>> print(f"Dimensions: {len(vectors[0])}")
            >>> print("Cost: $0.00 (FREE!)")
        """
        if not texts:
            raise ValueError("texts list cannot be empty")

        # Handle batching for large lists
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch_embeddings = self._embed_batch(batch)
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    def embed_query(self, text: str) -> List[float]:
        """
        Embed query text using ZeroDB's FREE HuggingFace service

        Args:
            text: Query text to embed

        Returns:
            Embedding vector

        Raises:
            ValueError: Empty text
            RuntimeError: API error

        Example:
            >>> embeddings = ZeroDBEmbeddings(api_key="your-key")
            >>> query = "What is quantum computing?"
            >>> vector = embeddings.embed_query(query)
            >>> print(f"Query embedding: {len(vector)} dimensions")
            >>> print("Cost: $0.00 (FREE!)")
        """
        if not text:
            raise ValueError("text cannot be empty")

        embeddings = self._embed_batch([text])
        return embeddings[0] if embeddings else []

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Async: Embed search documents using ZeroDB's FREE HuggingFace service

        This method provides true async support for better performance in
        async applications.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (one per text)

        Raises:
            ValueError: Empty texts list
            RuntimeError: API error
        """
        if not texts:
            raise ValueError("texts list cannot be empty")

        client = self._get_client()

        # Handle batching for large lists
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            result = await client.embeddings.generate(
                texts=batch,
                model=self.model,
                normalize=self.normalize,
            )
            all_embeddings.extend(result.get("embeddings", []))

        return all_embeddings

    async def aembed_query(self, text: str) -> List[float]:
        """
        Async: Embed query text using ZeroDB's FREE HuggingFace service

        Args:
            text: Query text to embed

        Returns:
            Embedding vector

        Raises:
            ValueError: Empty text
            RuntimeError: API error
        """
        if not text:
            raise ValueError("text cannot be empty")

        client = self._get_client()
        result = await client.embeddings.generate(
            texts=[text],
            model=self.model,
            normalize=self.normalize,
        )

        embeddings = result.get("embeddings", [])
        return embeddings[0] if embeddings else []


# Export for convenience
__all__ = ["ZeroDBEmbeddings"]
