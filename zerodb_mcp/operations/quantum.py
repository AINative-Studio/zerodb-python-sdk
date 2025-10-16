"""
Quantum computing operations for ZeroDB MCP Client

Provides 6 quantum operations leveraging AWS Braket and IonQ:
1. compress_vector - Quantum vector compression
2. decompress_vector - Quantum vector decompression
3. hybrid_similarity - Quantum-enhanced similarity search
4. optimize_space - Quantum space optimization
5. feature_map - Quantum feature mapping
6. kernel_similarity - Quantum kernel similarity
"""

from typing import Dict, Any, List, Optional
from ..utils import validate_embedding


class QuantumOperations:
    """Quantum computing operations powered by AWS Braket and IonQ"""

    def __init__(self, client):
        self._client = client

    async def compress_vector(
        self,
        project_id: str,
        vector_id: str,
        target_dimensions: int,
        backend: str = "simulator"
    ) -> Dict[str, Any]:
        """
        Compress vector using quantum algorithms

        Uses quantum amplitude encoding and optimization to compress high-dimensional
        vectors while preserving semantic information.

        Args:
            project_id: Project ID
            vector_id: Vector ID to compress
            target_dimensions: Target dimensions (2-512)
            backend: Quantum backend (simulator, ionq, braket)

        Returns:
            {
                "compressed_vector_id": "uuid",
                "original_dimensions": 1536,
                "compressed_dimensions": 128,
                "compression_ratio": 12.0,
                "quantum_fidelity": 0.95,
                "backend_used": "ionq"
            }

        Example:
            >>> result = await client.quantum.compress_vector(
            ...     project_id="550e8400-...",
            ...     vector_id="660e8400-...",
            ...     target_dimensions=128,
            ...     backend="ionq"
            ... )
            >>> print(f"Compressed to {result['compressed_dimensions']} dims")
        """
        if not 2 <= target_dimensions <= 512:
            raise ValueError("Target dimensions must be between 2 and 512")

        if backend not in ["simulator", "ionq", "braket"]:
            raise ValueError("Backend must be simulator, ionq, or braket")

        params = {
            "project_id": project_id,
            "vector_id": vector_id,
            "target_dimensions": target_dimensions,
            "backend": backend
        }

        return await self._client.execute("quantum_compress_vector", params)

    async def decompress_vector(
        self,
        project_id: str,
        compressed_state: List[complex],
        original_dimensions: int,
        backend: str = "simulator"
    ) -> Dict[str, Any]:
        """
        Decompress quantum-compressed vector

        Args:
            project_id: Project ID
            compressed_state: Compressed quantum state
            original_dimensions: Original vector dimensions
            backend: Quantum backend

        Returns:
            {
                "decompressed_vector": [...],
                "fidelity": 0.94,
                "reconstruction_error": 0.06
            }

        Example:
            >>> result = await client.quantum.decompress_vector(
            ...     project_id="550e8400-...",
            ...     compressed_state=complex_state,
            ...     original_dimensions=1536
            ... )
        """
        params = {
            "project_id": project_id,
            "compressed_state": [{"real": c.real, "imag": c.imag} for c in compressed_state],
            "original_dimensions": original_dimensions,
            "backend": backend
        }

        return await self._client.execute("quantum_decompress_vector", params)

    async def hybrid_similarity(
        self,
        project_id: str,
        query_vector: List[float],
        top_k: int = 10,
        quantum_weight: float = 0.5,
        backend: str = "simulator"
    ) -> Dict[str, Any]:
        """
        Quantum-enhanced hybrid similarity search

        Combines classical cosine similarity with quantum kernel methods for
        improved semantic search accuracy.

        Args:
            project_id: Project ID
            query_vector: Query embedding
            top_k: Number of results (1-100)
            quantum_weight: Weight for quantum component (0.0-1.0)
            backend: Quantum backend

        Returns:
            {
                "results": [
                    {
                        "vector_id": "uuid",
                        "classical_similarity": 0.85,
                        "quantum_similarity": 0.92,
                        "hybrid_score": 0.885,
                        "document": "text",
                        "metadata": {...}
                    }
                ],
                "quantum_advantage": 0.035
            }

        Example:
            >>> results = await client.quantum.hybrid_similarity(
            ...     project_id="550e8400-...",
            ...     query_vector=[0.1, 0.2, ...],
            ...     top_k=20,
            ...     quantum_weight=0.6,
            ...     backend="ionq"
            ... )
            >>> print(f"Quantum advantage: {results['quantum_advantage']}")
        """
        validate_embedding(query_vector)

        if not 1 <= top_k <= 100:
            raise ValueError("top_k must be between 1 and 100")

        if not 0.0 <= quantum_weight <= 1.0:
            raise ValueError("quantum_weight must be between 0.0 and 1.0")

        params = {
            "project_id": project_id,
            "query_vector": query_vector,
            "top_k": top_k,
            "quantum_weight": quantum_weight,
            "backend": backend
        }

        return await self._client.execute("quantum_hybrid_similarity", params)

    async def optimize_space(
        self,
        project_id: str,
        namespace: str = "default",
        target_compression: float = 0.5,
        backend: str = "simulator"
    ) -> Dict[str, Any]:
        """
        Quantum space optimization for vector database

        Uses quantum algorithms to optimize storage while preserving search quality.

        Args:
            project_id: Project ID
            namespace: Vector namespace
            target_compression: Target compression ratio (0.1-0.9)
            backend: Quantum backend

        Returns:
            {
                "original_size_mb": 500.0,
                "optimized_size_mb": 250.0,
                "compression_achieved": 0.5,
                "search_quality_preserved": 0.98,
                "vectors_optimized": 10000
            }

        Example:
            >>> result = await client.quantum.optimize_space(
            ...     project_id="550e8400-...",
            ...     target_compression=0.4
            ... )
            >>> saved_mb = result['original_size_mb'] - result['optimized_size_mb']
            >>> print(f"Saved {saved_mb:.2f} MB")
        """
        if not 0.1 <= target_compression <= 0.9:
            raise ValueError("target_compression must be between 0.1 and 0.9")

        params = {
            "project_id": project_id,
            "namespace": namespace,
            "target_compression": target_compression,
            "backend": backend
        }

        return await self._client.execute("quantum_optimize_space", params)

    async def feature_map(
        self,
        project_id: str,
        vector_id: str,
        feature_map_type: str = "ZZFeatureMap",
        backend: str = "simulator"
    ) -> Dict[str, Any]:
        """
        Apply quantum feature mapping to vector

        Maps classical vectors to quantum feature space for enhanced representations.

        Args:
            project_id: Project ID
            vector_id: Vector ID
            feature_map_type: Type of quantum feature map
                (ZZFeatureMap, PauliFeatureMap, StatePreparation)
            backend: Quantum backend

        Returns:
            {
                "mapped_state": [...],
                "feature_map_type": "ZZFeatureMap",
                "qubits_used": 10,
                "entanglement_measure": 0.75
            }

        Example:
            >>> result = await client.quantum.feature_map(
            ...     project_id="550e8400-...",
            ...     vector_id="660e8400-...",
            ...     feature_map_type="ZZFeatureMap"
            ... )
        """
        valid_maps = ["ZZFeatureMap", "PauliFeatureMap", "StatePreparation"]
        if feature_map_type not in valid_maps:
            raise ValueError(f"feature_map_type must be one of {valid_maps}")

        params = {
            "project_id": project_id,
            "vector_id": vector_id,
            "feature_map_type": feature_map_type,
            "backend": backend
        }

        return await self._client.execute("quantum_feature_map", params)

    async def kernel_similarity(
        self,
        project_id: str,
        vector_id_a: str,
        vector_id_b: str,
        kernel_type: str = "fidelity",
        backend: str = "simulator"
    ) -> Dict[str, Any]:
        """
        Compute quantum kernel similarity between two vectors

        Uses quantum kernel methods to compute advanced similarity metrics.

        Args:
            project_id: Project ID
            vector_id_a: First vector ID
            vector_id_b: Second vector ID
            kernel_type: Kernel type (fidelity, swap_test, inner_product)
            backend: Quantum backend

        Returns:
            {
                "quantum_similarity": 0.89,
                "classical_cosine": 0.82,
                "kernel_type": "fidelity",
                "quantum_advantage": 0.07
            }

        Example:
            >>> result = await client.quantum.kernel_similarity(
            ...     project_id="550e8400-...",
            ...     vector_id_a="660e8400-...",
            ...     vector_id_b="770e8400-...",
            ...     kernel_type="fidelity",
            ...     backend="ionq"
            ... )
            >>> print(f"Quantum similarity: {result['quantum_similarity']}")
        """
        valid_kernels = ["fidelity", "swap_test", "inner_product"]
        if kernel_type not in valid_kernels:
            raise ValueError(f"kernel_type must be one of {valid_kernels}")

        params = {
            "project_id": project_id,
            "vector_id_a": vector_id_a,
            "vector_id_b": vector_id_b,
            "kernel_type": kernel_type,
            "backend": backend
        }

        return await self._client.execute("quantum_kernel_similarity", params)
