# ZeroDB MCP Python Client - Quick Start Guide

Get up and running with the ZeroDB MCP Python Client in 5 minutes.

## Installation

```bash
pip install zerodb-mcp
```

## Authentication

Get your API key from [https://ainative.studio/dashboard](https://ainative.studio/dashboard).

### Option 1: Environment Variable (Recommended)

Create a `.env` file:
```bash
ZERODB_API_KEY=your_api_key_here
```

```python
from zerodb_mcp import ZeroDBClient

client = ZeroDBClient()  # Automatically loads from .env
```

### Option 2: Direct Initialization

```python
from zerodb_mcp import ZeroDBClient

client = ZeroDBClient(api_key="your_api_key_here")
```

## Basic Usage

### 1. Create a Project

```python
import asyncio
from zerodb_mcp import ZeroDBClient

async def main():
    client = ZeroDBClient(api_key="your_api_key")

    # Create a project
    project = await client.projects.create(
        name="My AI Project",
        tier="free"
    )

    project_id = project["project_id"]
    print(f"Created project: {project_id}")

    await client.close()

asyncio.run(main())
```

### 2. Store and Search Vectors

```python
async def vector_demo():
    client = ZeroDBClient(api_key="your_api_key")
    project_id = "your_project_id"

    # Store a vector
    result = await client.vectors.upsert(
        project_id=project_id,
        embedding=[0.1, 0.2, 0.3] * 512,  # 1536 dimensions
        document="Introduction to machine learning",
        metadata={"category": "education", "level": "beginner"}
    )

    print(f"Stored vector: {result['vector_id']}")

    # Search vectors
    results = await client.vectors.search(
        project_id=project_id,
        query_vector=[0.15, 0.25, 0.35] * 512,
        limit=5,
        threshold=0.7
    )

    for item in results["results"]:
        print(f"Match: {item['document']} (similarity: {item['similarity']:.3f})")

    await client.close()

asyncio.run(vector_demo())
```

### 3. Batch Operations

```python
async def batch_demo():
    client = ZeroDBClient(api_key="your_api_key")
    project_id = "your_project_id"

    # Prepare multiple vectors
    vectors = [
        {
            "embedding": [0.1] * 1536,
            "document": "Document 1",
            "metadata": {"id": 1}
        },
        {
            "embedding": [0.2] * 1536,
            "document": "Document 2",
            "metadata": {"id": 2}
        },
        {
            "embedding": [0.3] * 1536,
            "document": "Document 3",
            "metadata": {"id": 3}
        }
    ]

    # Batch upsert
    result = await client.vectors.batch_upsert(
        project_id=project_id,
        vectors=vectors
    )

    print(f"Uploaded {result['successful']} vectors")

    await client.close()

asyncio.run(batch_demo())
```

### 4. File Storage

```python
async def file_demo():
    client = ZeroDBClient(api_key="your_api_key")
    project_id = "your_project_id"

    # Upload a file
    result = await client.files.upload(
        project_id=project_id,
        file_path="/path/to/document.pdf",
        metadata={"category": "legal"}
    )

    file_id = result["file_id"]
    print(f"Uploaded file: {file_id}")

    # Download the file
    content = await client.files.download(
        project_id=project_id,
        file_id=file_id
    )

    print(f"Downloaded {len(content)} bytes")

    await client.close()

asyncio.run(file_demo())
```

### 5. Quantum Operations

```python
async def quantum_demo():
    client = ZeroDBClient(api_key="your_api_key")
    project_id = "your_project_id"

    # Compress vector using quantum algorithms
    result = await client.quantum.compress_vector(
        project_id=project_id,
        vector_id="your_vector_id",
        target_dimensions=128,
        backend="simulator"  # or "ionq" for real quantum hardware
    )

    print(f"Compression ratio: {result['compression_ratio']:.2f}x")
    print(f"Quantum fidelity: {result['quantum_fidelity']:.3f}")

    # Quantum-enhanced similarity search
    results = await client.quantum.hybrid_similarity(
        project_id=project_id,
        query_vector=[0.1] * 1536,
        top_k=10,
        quantum_weight=0.6  # 60% quantum, 40% classical
    )

    print(f"Quantum advantage: {results['quantum_advantage']:.4f}")

    await client.close()

asyncio.run(quantum_demo())
```

## Context Manager (Recommended)

Use the async context manager for automatic cleanup:

```python
async def context_demo():
    async with ZeroDBClient(api_key="your_api_key") as client:
        project = await client.projects.create(name="Test")
        # Client automatically closes when exiting context

asyncio.run(context_demo())
```

## Error Handling

```python
from zerodb_mcp import (
    ZeroDBError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

async def error_handling_demo():
    client = ZeroDBClient(api_key="your_api_key")

    try:
        result = await client.vectors.upsert(
            project_id="invalid_id",
            embedding=[0.1] * 1536,
            document="Test"
        )
    except AuthenticationError:
        print("Authentication failed - check your API key")
    except RateLimitError as e:
        print(f"Rate limited - retry after {e.retry_after} seconds")
    except ValidationError as e:
        print(f"Validation error: {e.errors}")
    except ZeroDBError as e:
        print(f"API error: {e}")
    finally:
        await client.close()

asyncio.run(error_handling_demo())
```

## Complete Example: Semantic Search Application

```python
import asyncio
from zerodb_mcp import ZeroDBClient

async def semantic_search_app():
    """Complete semantic search application"""

    # Initialize client
    client = ZeroDBClient(api_key="your_api_key")

    try:
        # 1. Create project
        project = await client.projects.create(
            name="Knowledge Base",
            tier="pro"
        )
        project_id = project["project_id"]
        print(f"✓ Created project: {project['name']}")

        # 2. Prepare documents (you would use actual embeddings here)
        documents = [
            {
                "embedding": [0.1 + i * 0.01] * 1536,
                "document": f"Document {i}: Machine learning concepts",
                "metadata": {"topic": "ML", "doc_id": i}
            }
            for i in range(100)
        ]

        # 3. Batch upload
        result = await client.vectors.batch_upsert(
            project_id=project_id,
            vectors=documents
        )
        print(f"✓ Uploaded {result['successful']} documents")

        # 4. Search
        query = [0.15] * 1536  # Your query embedding
        results = await client.vectors.search(
            project_id=project_id,
            query_vector=query,
            limit=5
        )

        print(f"\n✓ Found {len(results['results'])} matches:")
        for i, match in enumerate(results['results'], 1):
            print(f"  {i}. {match['document']}")
            print(f"     Similarity: {match['similarity']:.3f}")

        # 5. Get project stats
        stats = await client.projects.get_stats(project_id)
        print(f"\n✓ Project stats:")
        print(f"  Total vectors: {stats['vectors']['total']}")
        print(f"  Storage: {stats['vectors']['storage_mb']:.2f} MB")

    except Exception as e:
        print(f"✗ Error: {e}")

    finally:
        await client.close()

# Run the application
asyncio.run(semantic_search_app())
```

## Next Steps

- Read the [Full Documentation](README.md)
- Explore [Examples](examples/)
- Check [API Reference](https://docs.ainative.studio/sdk/python)
- Join our [Discord Community](https://discord.gg/ainative)

## Getting Help

- **Documentation**: https://docs.ainative.studio/sdk/python
- **GitHub Issues**: https://github.com/ainative/zerodb-mcp-python/issues
- **Email**: support@ainative.studio

## Common Patterns

### Processing Large Datasets

```python
from zerodb_mcp.utils import chunk_list

documents = [...]  # Large list

for chunk in chunk_list(documents, chunk_size=100):
    await client.vectors.batch_upsert(project_id, chunk)
```

### Parallel Operations

```python
import asyncio

# Execute multiple searches in parallel
results = await asyncio.gather(
    client.vectors.search(project_id, query1),
    client.vectors.search(project_id, query2),
    client.vectors.search(project_id, query3)
)
```

### Retry Logic

The client has built-in retry logic, but you can customize it:

```python
client = ZeroDBClient(
    api_key="your_key",
    max_retries=5,      # Retry up to 5 times
    retry_delay=2.0     # Wait 2 seconds between retries
)
```

Happy coding! 🚀
