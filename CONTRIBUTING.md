# Contributing to ZeroDB MCP Python Client

Thank you for your interest in contributing to the ZeroDB MCP Python Client! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip and virtualenv
- Git

### Setting Up Your Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/zerodb-mcp-python.git
cd zerodb-mcp-python
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **flake8**: Linting

Format your code before committing:
```bash
# Format code
black zerodb_mcp/
isort zerodb_mcp/

# Type check
mypy zerodb_mcp/

# Lint
flake8 zerodb_mcp/
```

### Running Tests

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=zerodb_mcp --cov-report=html

# Run specific test file
pytest tests/test_vectors.py

# Run specific test
pytest tests/test_vectors.py::TestVectorOperations::test_upsert_vector
```

### Writing Tests

All new features should include tests. We aim for 90%+ coverage.

Example test structure:
```python
import pytest
from unittest.mock import MagicMock

class TestNewFeature:
    """Test new feature"""

    @pytest.mark.asyncio
    async def test_new_operation(self, client, mock_httpx_client):
        """Test description"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_httpx_client.post.return_value = mock_response

        # Act
        result = await client.feature.operation()

        # Assert
        assert result["status"] == "success"
```

## Pull Request Process

1. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**:
   - Write code following our style guidelines
   - Add tests for new features
   - Update documentation as needed

3. **Commit your changes**:
```bash
git add .
git commit -m "feat: add new feature"
```

We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

4. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

5. **Create a Pull Request**:
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Request review

### Pull Request Checklist

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] Type checking passes (`mypy`)
- [ ] Linting passes (`flake8`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] All tests have clear descriptions
- [ ] No decrease in test coverage

## Adding New Operations

To add a new operation to an existing module:

1. **Add the operation method** in `zerodb_mcp/operations/`:
```python
async def new_operation(
    self,
    project_id: str,
    param1: str,
    param2: Optional[int] = None
) -> Dict[str, Any]:
    """
    Operation description

    Args:
        project_id: Project ID
        param1: Description
        param2: Optional parameter

    Returns:
        Result dictionary

    Example:
        >>> result = await client.module.new_operation(
        ...     project_id="...",
        ...     param1="value"
        ... )
    """
    params = {
        "project_id": project_id,
        "param1": param1
    }
    if param2 is not None:
        params["param2"] = param2

    return await self._client.execute("operation_name", params)
```

2. **Add Pydantic models** if needed in `models.py`:
```python
class NewOperationRequest(BaseModel):
    """Request model"""
    project_id: str
    param1: str = Field(..., min_length=1)
    param2: Optional[int] = None
```

3. **Write tests** in `tests/`:
```python
@pytest.mark.asyncio
async def test_new_operation(self, client, mock_httpx_client):
    """Test new operation"""
    # ... test implementation
```

4. **Update documentation**:
   - Add example to README.md
   - Update CHANGELOG.md
   - Add example file if complex

## Code Review Guidelines

When reviewing PRs, consider:

- **Correctness**: Does the code do what it's supposed to?
- **Tests**: Are there adequate tests?
- **Documentation**: Is the code well-documented?
- **Style**: Does it follow our conventions?
- **Performance**: Are there any performance concerns?
- **Security**: Are there any security implications?

## Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Environment**: Python version, OS, package version
3. **Reproduction**: Minimal code to reproduce
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Traceback**: Full error traceback if applicable

Example bug report:
```markdown
## Description
Vector search returns incorrect results

## Environment
- Python: 3.11.0
- OS: macOS 14.0
- Package: zerodb-mcp 1.0.0

## Reproduction
```python
client = ZeroDBClient(api_key="...")
results = await client.vectors.search(...)
```

## Expected
Should return 10 results

## Actual
Returns 0 results

## Traceback
```
...
```
```

## Feature Requests

We welcome feature requests! Please include:

1. **Use case**: Why is this needed?
2. **Proposed solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Examples**: Example code showing usage

## Questions?

- Check the [Documentation](https://docs.ainative.studio/sdk/python)
- Open a [GitHub Discussion](https://github.com/ainative/zerodb-mcp-python/discussions)
- Email: support@ainative.studio

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
