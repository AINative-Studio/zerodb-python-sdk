"""
Quantum operations example for ZeroDB MCP Python Client
"""

import asyncio
from zerodb_mcp import ZeroDBClient


async def main():
    client = ZeroDBClient(api_key="your_api_key_here")

    try:
        project_id = "your_project_id_here"

        # 1. Compress vector using quantum algorithms
        print("1. Compressing vector with quantum algorithms...")
        compression_result = await client.quantum.compress_vector(
            project_id=project_id,
            vector_id="your_vector_id_here",
            target_dimensions=128,
            backend="simulator"  # Use "ionq" for real quantum hardware
        )
        print(f"Compression ratio: {compression_result['compression_ratio']:.2f}x")
        print(f"Quantum fidelity: {compression_result['quantum_fidelity']:.3f}")

        # 2. Quantum hybrid similarity search
        print("\n2. Running quantum hybrid similarity search...")
        results = await client.quantum.hybrid_similarity(
            project_id=project_id,
            query_vector=[0.1] * 1536,
            top_k=10,
            quantum_weight=0.6,  # 60% quantum, 40% classical
            backend="simulator"
        )
        print(f"Quantum advantage: {results['quantum_advantage']:.4f}")
        for i, result in enumerate(results['results'][:3], 1):
            print(f"{i}. Hybrid score: {result['hybrid_score']:.3f}")
            print(f"   Classical: {result['classical_similarity']:.3f}")
            print(f"   Quantum: {result['quantum_similarity']:.3f}")

        # 3. Quantum space optimization
        print("\n3. Optimizing vector space with quantum algorithms...")
        optimization_result = await client.quantum.optimize_space(
            project_id=project_id,
            namespace="default",
            target_compression=0.5,  # 50% compression
            backend="simulator"
        )
        saved_mb = (
            optimization_result['original_size_mb'] -
            optimization_result['optimized_size_mb']
        )
        print(f"Space saved: {saved_mb:.2f} MB")
        print(f"Search quality preserved: {optimization_result['search_quality_preserved']:.1%}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
