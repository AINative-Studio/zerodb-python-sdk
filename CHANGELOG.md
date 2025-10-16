# Changelog

All notable changes to the ZeroDB MCP Python Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-14

### Added

#### Core Features
- Initial production release of ZeroDB MCP Python Client
- Full async/await support using httpx
- Comprehensive type safety with Pydantic models
- Automatic retry logic with exponential backoff
- Intelligent rate limiting with retry-after support
- Async context manager support

#### Authentication
- API key authentication support
- JWT token authentication support
- Environment variable configuration
- Token refresh capabilities

#### Vector Operations (10 operations)
- `upsert` - Store or update vectors
- `batch_upsert` - Batch vector operations
- `search` - Semantic vector search
- `delete` - Delete vectors
- `get` - Retrieve vector by ID
- `list` - List vectors with pagination
- `stats` - Vector statistics
- `create_index` - Index creation
- `optimize_storage` - Storage optimization
- `export` - Vector export

#### Quantum Operations (6 operations)
- `compress_vector` - Quantum vector compression
- `decompress_vector` - Quantum vector decompression
- `hybrid_similarity` - Quantum-enhanced similarity search
- `optimize_space` - Quantum space optimization
- `feature_map` - Quantum feature mapping
- `kernel_similarity` - Quantum kernel similarity

#### Table Operations (8 operations)
- `create` - Create NoSQL tables
- `list` - List tables
- `get` - Get table details
- `delete` - Delete tables
- `insert_rows` - Insert table rows
- `query_rows` - Query table data
- `update_rows` - Update table rows
- `delete_rows` - Delete table rows

#### File Operations (6 operations)
- `upload` - Upload files from filesystem
- `upload_bytes` - Upload files from bytes
- `download` - Download files
- `list` - List files
- `delete` - Delete files
- `get_metadata` - Get file metadata
- `generate_presigned_url` - Generate download URLs

#### Project Operations (7 operations)
- `create` - Create projects
- `get` - Get project details
- `list` - List projects
- `update` - Update projects
- `delete` - Delete projects
- `get_stats` - Project statistics
- `enable_database` - Enable database features

#### Event Operations (5 operations)
- `create` - Create events
- `list` - List events
- `get` - Get event details
- `subscribe` - Subscribe to event streams
- `stats` - Event statistics

#### RLHF Operations (10 operations)
- `collect_interaction` - Collect user-agent interactions
- `collect_agent_feedback` - Collect feedback
- `collect_workflow_feedback` - Collect workflow data
- `collect_error_report` - Report errors
- `get_status` - Get RLHF status
- `get_summary` - Get feedback summary
- `start_collection` - Start collection session
- `stop_collection` - Stop collection session
- `get_session_interactions` - Get session data
- `broadcast_event` - Broadcast RLHF events

#### Admin Operations (5 operations)
- `get_system_stats` - System statistics
- `list_all_projects` - List all projects (admin)
- `get_user_usage` - User usage statistics
- `system_health` - System health check
- `optimize_database` - Database optimization

#### Error Handling
- `ZeroDBError` - Base exception class
- `AuthenticationError` - Authentication failures
- `RateLimitError` - Rate limiting
- `ValidationError` - Validation errors
- `ResourceNotFoundError` - Resource not found
- `QuotaExceededError` - Quota exceeded
- `NetworkError` - Network issues
- `TimeoutError` - Request timeouts
- `ServerError` - Server errors
- `ConflictError` - Resource conflicts

#### Documentation
- Comprehensive README with examples
- API reference documentation
- Error handling guide
- Quick start guide
- Configuration guide

#### Examples
- Basic usage example
- Quantum operations example
- File upload example
- RLHF tracking example
- Batch processing example

#### Testing
- 90%+ test coverage
- Unit tests for all operations
- Mock-based testing
- Pytest configuration
- Coverage reporting

#### Development Tools
- Black code formatting
- isort import sorting
- mypy type checking
- flake8 linting
- pytest testing framework

### Package Information
- Python 3.9+ support
- MIT License
- Available on PyPI as `zerodb-mcp`

## [Unreleased]

### Planned Features
- WebSocket support for real-time events
- Streaming response support
- Advanced caching mechanisms
- Batch operation optimization
- Enhanced logging configuration
- CLI tool for common operations

---

For more information, visit:
- Documentation: https://docs.ainative.studio/sdk/python
- GitHub: https://github.com/ainative/zerodb-mcp-python
- PyPI: https://pypi.org/project/zerodb-mcp/
