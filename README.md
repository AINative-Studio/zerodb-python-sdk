# ZeroDB MCP Python Client SDK

[![PyPI version](https://badge.fury.io/py/zerodb-mcp.svg)](https://badge.fury.io/py/zerodb-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/zerodb-mcp.svg)](https://pypi.org/project/zerodb-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Python client for the ZeroDB MCP Bridge API. Provides comprehensive async access to all 60+ operations including vectors, quantum computing, NoSQL tables, file storage, events, RLHF, and admin functionality.

## Features

- **Complete API Coverage**: All 60+ MCP Bridge operations
- **Async/Await Support**: Built on `httpx` for high-performance async operations
- **Type Safety**: Full Pydantic model validation
- **Automatic Retries**: Intelligent retry logic with exponential backoff
- **Error Handling**: Comprehensive exception hierarchy
- **Rate Limiting**: Built-in rate limit handling with retry-after support
- **Authentication**: API key and JWT token support
- **Production Ready**: Battle-tested with 90%+ test coverage

## Installation

```bash
pip install zerodb-mcp
```

### Development Installation

```bash
git clone https://github.com/ainative/zerodb-mcp-python.git
cd zerodb-mcp-python
pip install -e ".[dev]"
```

## Quick Start

### Using ZeroDB Cloud

```python
import asyncio
from zerodb_mcp import ZeroDBClient

async def main():
    # Initialize client (cloud)
    client = ZeroDBClient(api_key="your_api_key")

    # Create a project
    project = await client.projects.create(
        name="My AI Project",
        tier="pro"
    )

    # Upsert vectors
    result = await client.vectors.upsert(
        project_id=project["project_id"],
        embedding=[0.1, 0.2, 0.3] * 512,  # 1536 dimensions
        document="Machine learning tutorial on neural networks",
        metadata={"category": "education", "language": "en"}
    )

    # Search vectors
    results = await client.vectors.search(
        project_id=project["project_id"],
        query_vector=[0.15, 0.25, 0.35] * 512,
        limit=10,
        threshold=0.7
    )

    for item in results["results"]:
        print(f"Document: {item['document']}")
        print(f"Similarity: {item['similarity']:.3f}\n")

    # Close client
    await client.close()

# Run async code
asyncio.run(main())
```

### Using ZeroDB Local

```python
import asyncio
from zerodb_mcp import ZeroDBClient

async def main():
    # Initialize client (local)
    client = ZeroDBClient(
        base_url="http://localhost:8000",  # Local ZeroDB instance
        api_key="local-dev-key"  # Any value works for local
    )

    # Same API as cloud - use all operations identically
    project = await client.projects.create(
        name="Local Development Project"
    )

    # Develop offline, sync when ready
    result = await client.vectors.upsert(
        project_id=project["project_id"],
        embedding=[0.1, 0.2, 0.3] * 512,
        document="Test document for local development"
    )

    await client.close()

asyncio.run(main())
```

**Learn more:** See [ZeroDB Local Quick Start](/docs/quick-start/ZERODB_LOCAL_QUICKSTART.md) for installation and setup.

## Authentication

### API Key Authentication

```python
# Method 1: Direct initialization
client = ZeroDBClient(api_key="your_api_key")

# Method 2: Environment variable
# Set ZERODB_API_KEY in .env file
from dotenv import load_dotenv
load_dotenv()

client = ZeroDBClient()  # Automatically loads from env
```

### JWT Token Authentication

```python
# Method 1: Direct initialization
client = ZeroDBClient(jwt_token="your_jwt_token")

# Method 2: Environment variable
# Set ZERODB_JWT_TOKEN in .env file
client = ZeroDBClient()  # Automatically loads from env
```

## Core Operations

### Vector Operations (10 operations)

```python
# 1. Upsert vector
result = await client.vectors.upsert(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    embedding=[0.1, 0.2, ...],
    document="Text content",
    namespace="default",
    metadata={"key": "value"}
)

# 2. Batch upsert
vectors = [
    {"embedding": [0.1, ...], "document": "Doc 1", "metadata": {}},
    {"embedding": [0.2, ...], "document": "Doc 2", "metadata": {}}
]
result = await client.vectors.batch_upsert(project_id, vectors)

# 3. Search vectors
results = await client.vectors.search(
    project_id=project_id,
    query_vector=[0.15, 0.25, ...],
    limit=20,
    threshold=0.8
)

# 4. Delete vector
await client.vectors.delete(project_id, vector_id)

# 5. Get vector
vector = await client.vectors.get(project_id, vector_id)

# 6. List vectors
vectors = await client.vectors.list(project_id, limit=100, offset=0)

# 7. Vector statistics
stats = await client.vectors.stats(project_id)

# 8. Create index
await client.vectors.create_index(project_id, index_type="hnsw")

# 9. Optimize storage
result = await client.vectors.optimize_storage(project_id)

# 10. Export vectors
export = await client.vectors.export(project_id, format="json")
```

### Quantum Operations (6 operations)

```python
# 1. Compress vector using quantum algorithms
result = await client.quantum.compress_vector(
    project_id=project_id,
    vector_id=vector_id,
    target_dimensions=128,
    backend="ionq"  # or "simulator", "braket"
)

# 2. Decompress vector
result = await client.quantum.decompress_vector(
    project_id=project_id,
    compressed_state=state,
    original_dimensions=1536
)

# 3. Quantum hybrid similarity search
results = await client.quantum.hybrid_similarity(
    project_id=project_id,
    query_vector=[0.1, 0.2, ...],
    top_k=10,
    quantum_weight=0.6,
    backend="ionq"
)

# 4. Quantum space optimization
result = await client.quantum.optimize_space(
    project_id=project_id,
    target_compression=0.5
)

# 5. Quantum feature mapping
result = await client.quantum.feature_map(
    project_id=project_id,
    vector_id=vector_id,
    feature_map_type="ZZFeatureMap"
)

# 6. Quantum kernel similarity
result = await client.quantum.kernel_similarity(
    project_id=project_id,
    vector_id_a=vec_a,
    vector_id_b=vec_b,
    kernel_type="fidelity"
)
```

### Table Operations (8 operations)

```python
# 1. Create table
table = await client.tables.create(
    project_id=project_id,
    table_name="users",
    schema_definition={
        "user_id": "string",
        "email": "string",
        "age": "integer"
    },
    indexes=["user_id", "email"]
)

# 2. Insert rows
result = await client.tables.insert_rows(
    project_id=project_id,
    table_name="users",
    rows=[
        {"user_id": "u1", "email": "user1@example.com", "age": 25},
        {"user_id": "u2", "email": "user2@example.com", "age": 30}
    ]
)

# 3. Query rows
results = await client.tables.query_rows(
    project_id=project_id,
    table_name="users",
    filters={"age": {"$gte": 18}},
    sort_by="age",
    order="desc"
)

# 4. Update rows
result = await client.tables.update_rows(
    project_id=project_id,
    table_name="users",
    filters={"age": {"$gte": 18}},
    updates={"verified": True}
)

# 5. Delete rows
result = await client.tables.delete_rows(
    project_id=project_id,
    table_name="users",
    filters={"active": False}
)

# 6. Get table
table = await client.tables.get(project_id, "users")

# 7. List tables
tables = await client.tables.list(project_id)

# 8. Delete table
await client.tables.delete(project_id, "users")
```

### File Operations (6 operations)

```python
# 1. Upload file from path
result = await client.files.upload(
    project_id=project_id,
    file_path="/path/to/document.pdf",
    metadata={"category": "legal"}
)

# 2. Upload file from bytes
content = b"Hello, World!"
result = await client.files.upload_bytes(
    project_id=project_id,
    content=content,
    file_name="hello.txt",
    content_type="text/plain"
)

# 3. Download file
content = await client.files.download(project_id, file_id)

# Save to file
await client.files.download(project_id, file_id, save_path="/path/to/save.pdf")

# 4. List files
files = await client.files.list(project_id, content_type="application/pdf")

# 5. Get file metadata
metadata = await client.files.get_metadata(project_id, file_id)

# 6. Generate presigned URL
url = await client.files.generate_presigned_url(
    project_id=project_id,
    file_id=file_id,
    expires_in=3600  # 1 hour
)
```

### Project Operations (7 operations)

```python
# 1. Create project
project = await client.projects.create(
    name="My Project",
    tier="pro",
    settings={"enable_quantum": True}
)

# 2. Get project
project = await client.projects.get(project_id)

# 3. List projects
projects = await client.projects.list(tier="pro")

# 4. Update project
await client.projects.update(
    project_id=project_id,
    name="Updated Name"
)

# 5. Delete project
await client.projects.delete(project_id, confirm=True)

# 6. Get project stats
stats = await client.projects.get_stats(project_id)

# 7. Enable database
await client.projects.enable_database(
    project_id=project_id,
    database_type="postgres"
)
```

### Event Operations (5 operations)

```python
# 1. Create event
event = await client.events.create(
    project_id=project_id,
    event_type="user.login",
    event_data={"user_id": "u123", "ip": "192.168.1.1"}
)

# 2. List events
events = await client.events.list(
    project_id=project_id,
    event_type="user.login",
    start_date="2025-01-01T00:00:00Z"
)

# 3. Get event
event = await client.events.get(project_id, event_id)

# 4. Subscribe to events
subscription = await client.events.subscribe(
    project_id=project_id,
    event_types=["user.login", "user.logout"]
)

# 5. Event statistics
stats = await client.events.stats(project_id)
```

### RLHF Operations (10 operations)

```python
# 1. Collect interaction
interaction = await client.rlhf.collect_interaction(
    session_id="sess_123",
    project_id=project_id,
    interaction_type="query",
    user_input="What is AI?",
    agent_response="AI is...",
    context={"model": "gpt-4"}
)

# 2. Collect feedback
feedback = await client.rlhf.collect_agent_feedback(
    session_id="sess_123",
    project_id=project_id,
    interaction_id=interaction["interaction_id"],
    rating=5,
    feedback_text="Very helpful!"
)

# 3. Collect workflow feedback
await client.rlhf.collect_workflow_feedback(
    session_id="sess_123",
    project_id=project_id,
    workflow_id="search",
    success=True,
    duration_ms=250
)

# 4. Report error
await client.rlhf.collect_error_report(
    session_id="sess_123",
    project_id=project_id,
    error_type="ValidationError",
    error_message="Invalid input"
)

# 5-10. Status, summary, session management
status = await client.rlhf.get_status(project_id)
summary = await client.rlhf.get_summary(project_id)
session = await client.rlhf.start_collection(project_id, "sess_123")
await client.rlhf.stop_collection(project_id, "sess_123")
interactions = await client.rlhf.get_session_interactions(project_id, "sess_123")
await client.rlhf.broadcast_event(project_id, "feedback.received", {})
```

### Admin Operations (5 operations)

Requires admin privileges.

```python
# 1. System statistics
stats = await client.admin.get_system_stats()

# 2. List all projects
projects = await client.admin.list_all_projects(tier="enterprise")

# 3. User usage
usage = await client.admin.get_user_usage("user_id")

# 4. System health
health = await client.admin.system_health()

# 5. Optimize database
result = await client.admin.optimize_database(vacuum=True, reindex=True)
```

## Error Handling

```python
from zerodb_mcp import (
    ZeroDBError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError,
    QuotaExceededError
)

try:
    result = await client.vectors.upsert(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Validation error: {e.errors}")
except ResourceNotFoundError as e:
    print(f"Not found: {e.resource_type} {e.resource_id}")
except QuotaExceededError as e:
    print(f"Quota exceeded: {e.quota_type} {e.current}/{e.limit}")
except ZeroDBError as e:
    print(f"API error: {e}")
```

## Context Manager Usage

```python
async with ZeroDBClient(api_key="your_key") as client:
    project = await client.projects.create(name="Test Project")
    # Client automatically closes when exiting context
```

## Configuration

### Environment Variables

Create a `.env` file:

```bash
ZERODB_API_KEY=your_api_key_here
# OR
ZERODB_JWT_TOKEN=your_jwt_token_here
```

### Custom Base URL

```python
client = ZeroDBClient(
    api_key="your_key",
    base_url="https://custom-api.example.com"
)
```

### Timeout Configuration

```python
client = ZeroDBClient(
    api_key="your_key",
    timeout=60.0,  # seconds
    max_retries=5,
    retry_delay=2.0
)
```

## Advanced Usage

### Parallel Operations

```python
import asyncio

# Execute multiple operations in parallel
results = await asyncio.gather(
    client.vectors.search(project_id, query1),
    client.vectors.search(project_id, query2),
    client.vectors.search(project_id, query3)
)
```

### Batch Processing

```python
# Process large datasets in chunks
from zerodb_mcp.utils import chunk_list

documents = [...]  # Large list
embedding_function = ...  # Your embedding function

for chunk in chunk_list(documents, chunk_size=100):
    vectors = [
        {
            "embedding": embedding_function(doc),
            "document": doc,
            "metadata": {}
        }
        for doc in chunk
    ]

    await client.vectors.batch_upsert(project_id, vectors)
```

## Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=zerodb_mcp --cov-report=html

# Run specific test file
pytest tests/test_vectors.py
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black zerodb_mcp/
isort zerodb_mcp/

# Type checking
mypy zerodb_mcp/

# Linting
flake8 zerodb_mcp/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://docs.ainative.studio/sdk/python
- Issues: https://github.com/ainative/zerodb-mcp-python/issues
- Email: support@ainative.studio

## Changelog

### 1.0.0 (2025-01-14)

- Initial production release
- 60+ MCP operations
- Full async support
- Comprehensive error handling
- Type safety with Pydantic
- 90%+ test coverage
