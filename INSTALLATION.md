# Installation and Setup Guide

Complete guide for installing and configuring the ZeroDB MCP Python Client SDK.

## System Requirements

- **Python**: 3.9 or higher
- **Operating Systems**: Linux, macOS, Windows
- **Dependencies**: httpx, pydantic, python-dotenv

## Installation Methods

### 1. Install from PyPI (Recommended)

```bash
pip install zerodb-mcp
```

### 2. Install from Source

```bash
git clone https://github.com/ainative/zerodb-mcp-python.git
cd zerodb-mcp-python
pip install .
```

### 3. Development Installation

For contributing or development:

```bash
git clone https://github.com/ainative/zerodb-mcp-python.git
cd zerodb-mcp-python
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies.

## Verify Installation

```bash
python3 -c "import zerodb_mcp; print(f'Version: {zerodb_mcp.__version__}')"
```

Expected output:
```
Version: 1.0.0
```

## Configuration

### 1. Get Your API Key

1. Visit [https://ainative.studio/dashboard](https://ainative.studio/dashboard)
2. Navigate to API Keys
3. Generate a new API key
4. Copy the key (it won't be shown again)

### 2. Configure Environment Variables

Create a `.env` file in your project root:

```bash
# Authentication
ZERODB_API_KEY=your_api_key_here

# Optional: Custom API endpoint
# ZERODB_BASE_URL=https://api.ainative.studio

# Optional: Timeout and retry settings
# ZERODB_TIMEOUT=30
# ZERODB_MAX_RETRIES=3
```

### 3. Load Environment Variables

#### Option A: Using python-dotenv (Recommended)

```python
from dotenv import load_dotenv
from zerodb_mcp import ZeroDBClient

load_dotenv()  # Load .env file

client = ZeroDBClient()  # Automatically uses ZERODB_API_KEY
```

#### Option B: Direct Initialization

```python
from zerodb_mcp import ZeroDBClient

client = ZeroDBClient(api_key="your_api_key_here")
```

#### Option C: Export to Shell

```bash
export ZERODB_API_KEY=your_api_key_here
python your_script.py
```

## Virtual Environment Setup

### Using venv (Built-in)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install package
pip install zerodb-mcp

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create environment
conda create -n zerodb python=3.11

# Activate
conda activate zerodb

# Install package
pip install zerodb-mcp

# Deactivate
conda deactivate
```

## Testing Your Installation

Create `test_installation.py`:

```python
import asyncio
from zerodb_mcp import ZeroDBClient

async def test_connection():
    """Test ZeroDB connection"""
    client = ZeroDBClient(api_key="your_api_key_here")

    try:
        # Test health endpoint
        health = await client.health_check()
        print(f"✓ Connection successful")
        print(f"  Status: {health.get('status', 'unknown')}")

        # Test creating a project
        project = await client.projects.create(
            name="Test Project",
            tier="free"
        )
        print(f"✓ Project created: {project['project_id']}")

        # Clean up
        await client.projects.delete(
            project_id=project['project_id'],
            confirm=True
        )
        print(f"✓ Test project deleted")

    except Exception as e:
        print(f"✗ Error: {e}")

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run the test:
```bash
python test_installation.py
```

## Dependency Management

### requirements.txt

For production deployments:

```txt
zerodb-mcp==1.0.0
```

### poetry

```bash
poetry add zerodb-mcp
```

### pipenv

```bash
pipenv install zerodb-mcp
```

## Docker Setup

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "your_app.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - ZERODB_API_KEY=${ZERODB_API_KEY}
    volumes:
      - .:/app
    command: python your_app.py
```

Run with Docker:
```bash
docker-compose up
```

## Troubleshooting

### Import Error

**Problem**: `ModuleNotFoundError: No module named 'zerodb_mcp'`

**Solution**:
```bash
# Verify installation
pip list | grep zerodb-mcp

# Reinstall if needed
pip install --force-reinstall zerodb-mcp
```

### Authentication Error

**Problem**: `AuthenticationError: Authentication failed`

**Solutions**:
1. Check your API key is correct
2. Verify environment variable is loaded:
   ```python
   import os
   print(os.getenv('ZERODB_API_KEY'))
   ```
3. Try direct initialization:
   ```python
   client = ZeroDBClient(api_key="your_key")
   ```

### SSL/Certificate Errors

**Problem**: `SSLError` or certificate verification failed

**Solution**:
```python
import httpx

client = ZeroDBClient(api_key="your_key")
# Custom HTTP client with SSL verification disabled (not recommended for production)
client._client = httpx.AsyncClient(verify=False)
```

### Timeout Errors

**Problem**: Requests timing out

**Solution**:
```python
# Increase timeout
client = ZeroDBClient(
    api_key="your_key",
    timeout=60.0  # 60 seconds
)
```

### Rate Limiting

**Problem**: `RateLimitError: Rate limit exceeded`

**Solution**:
```python
from zerodb_mcp.exceptions import RateLimitError
import asyncio

try:
    result = await client.vectors.search(...)
except RateLimitError as e:
    # Wait and retry
    await asyncio.sleep(e.retry_after or 60)
    result = await client.vectors.search(...)
```

## Development Tools

### IDE Setup

#### VS Code

Install recommended extensions:
- Python
- Pylance
- Python Test Explorer

Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

#### PyCharm

1. Open project
2. Configure interpreter: File → Settings → Project → Python Interpreter
3. Install package in dev mode
4. Enable pytest in settings

### Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

Install:
```bash
pip install pre-commit
pre-commit install
```

## Upgrading

### Check for Updates

```bash
pip list --outdated | grep zerodb-mcp
```

### Upgrade to Latest

```bash
pip install --upgrade zerodb-mcp
```

### Upgrade to Specific Version

```bash
pip install zerodb-mcp==1.1.0
```

## Uninstallation

```bash
pip uninstall zerodb-mcp
```

## Next Steps

After installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for basic usage
2. Explore [examples/](examples/) directory
3. Review [README.md](README.md) for full documentation
4. Join our community for support

## Support

- **Documentation**: https://docs.ainative.studio/sdk/python
- **GitHub Issues**: https://github.com/ainative/zerodb-mcp-python/issues
- **Discord**: https://discord.gg/ainative
- **Email**: support@ainative.studio
