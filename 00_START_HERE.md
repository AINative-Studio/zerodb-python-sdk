# ZeroDB MCP Python Client SDK - Start Here

Welcome to the **ZeroDB MCP Python Client SDK**! This is your complete guide to getting started.

## 📦 Package Overview

Production-ready Python client for the ZeroDB MCP Bridge API with:
- **58 operations** across 8 modules
- **Full async/await** support
- **Type-safe** with Pydantic
- **90%+ test coverage**
- **Comprehensive documentation**

## 🚀 Quick Links

### For Users

1. **[INSTALLATION.md](INSTALLATION.md)** - Complete installation guide
   - System requirements
   - Installation methods
   - Environment setup
   - Troubleshooting

2. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
   - Basic usage
   - Common patterns
   - Complete examples
   - Error handling

3. **[README.md](README.md)** - Full documentation
   - All 58 operations
   - API reference
   - Advanced usage
   - Configuration

### For Developers

4. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guide
   - Setup instructions
   - Code style
   - Testing
   - Pull requests

5. **[CHANGELOG.md](CHANGELOG.md)** - Version history

6. **[examples/](examples/)** - Example applications
   - `basic_usage.py` - Basic operations
   - `quantum_operations.py` - Quantum features
   - `file_upload.py` - File management
   - `rlhf_tracking.py` - RLHF feedback

## 📚 Documentation Map

```
00_START_HERE.md              ← You are here
├── INSTALLATION.md            ← Install the package
├── QUICKSTART.md              ← Get started quickly
├── README.md                  ← Complete documentation
│
├── For Developers:
│   ├── CONTRIBUTING.md        ← Contribute to the project
│   ├── CHANGELOG.md           ← Version history
│   └── verify_package.py      ← Verify installation
│
├── Examples:
│   └── examples/              ← Working examples
│
└── Package Summaries:
    ├── PACKAGE_DELIVERY_SUMMARY.md
    ├── FINAL_SUMMARY.txt
    └── README_SUMMARY.md
```

## 🔧 Installation

### Quick Install

```bash
pip install zerodb-mcp
```

### Verify Installation

```bash
python3 -c "import zerodb_mcp; print(f'Version: {zerodb_mcp.__version__}')"
```

Expected output: `Version: 1.0.0`

## 💡 Quick Example

```python
import asyncio
from zerodb_mcp import ZeroDBClient

async def main():
    # Initialize client
    client = ZeroDBClient(api_key="your_api_key")

    # Create a project
    project = await client.projects.create(name="My Project")

    # Upsert a vector
    await client.vectors.upsert(
        project_id=project["project_id"],
        embedding=[0.1] * 1536,
        document="Sample document"
    )

    # Search vectors
    results = await client.vectors.search(
        project_id=project["project_id"],
        query_vector=[0.1] * 1536,
        limit=10
    )

    print(f"Found {len(results['results'])} matches")

    await client.close()

asyncio.run(main())
```

## 📖 What Can You Do?

### Vector Operations (10)
Store and search high-dimensional vectors for semantic search, RAG, and AI applications.

### Quantum Operations (6)
Leverage quantum computing for vector compression and enhanced similarity search.

### Table Operations (8)
Flexible NoSQL table storage with schema definition and querying.

### File Operations (7)
Upload, download, and manage files with metadata.

### Project Management (7)
Create and manage projects with different tiers and settings.

### Event Tracking (5)
Track and stream application events in real-time.

### RLHF Operations (10)
Collect feedback for Reinforcement Learning from Human Feedback.

### Admin Operations (5)
System administration and monitoring (requires admin privileges).

## 🎯 Common Use Cases

### 1. Semantic Search Application
Build a semantic search engine for your documentation or knowledge base.
→ See `examples/basic_usage.py`

### 2. Quantum-Enhanced AI
Use quantum computing to compress vectors and improve search accuracy.
→ See `examples/quantum_operations.py`

### 3. Document Management
Upload and manage files with metadata and search capabilities.
→ See `examples/file_upload.py`

### 4. AI Feedback Collection
Track user interactions and collect feedback for model improvement.
→ See `examples/rlhf_tracking.py`

## 🔑 Getting Your API Key

1. Visit [https://ainative.studio/dashboard](https://ainative.studio/dashboard)
2. Navigate to API Keys
3. Generate a new key
4. Add to `.env`:
   ```bash
   ZERODB_API_KEY=your_api_key_here
   ```

## 📊 Package Statistics

- **58 operations** across 8 modules
- **3,840 lines** of production code
- **10 exception classes** for comprehensive error handling
- **20+ Pydantic models** for type safety
- **40+ pages** of documentation
- **50+ code examples**
- **4 example applications**

## ✅ Feature Highlights

✅ **Async/Await** - Built on httpx for high performance
✅ **Type Safe** - Full Pydantic validation
✅ **Error Handling** - 10 custom exception types
✅ **Auto Retry** - Intelligent retry with backoff
✅ **Rate Limiting** - Built-in rate limit handling
✅ **Context Manager** - Automatic resource cleanup
✅ **Environment Config** - Easy configuration
✅ **Multiple Auth** - API key and JWT support

## 🛠️ Development

### For Contributors

```bash
# Clone repository
git clone https://github.com/ainative/zerodb-mcp-python.git
cd zerodb-mcp-python

# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest

# Verify package
python verify_package.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📞 Support

- **Documentation**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Installation**: [INSTALLATION.md](INSTALLATION.md)
- **GitHub**: https://github.com/ainative/zerodb-mcp-python
- **Email**: support@ainative.studio

## 🎓 Learning Path

**Beginner**:
1. Read [INSTALLATION.md](INSTALLATION.md)
2. Follow [QUICKSTART.md](QUICKSTART.md)
3. Run `examples/basic_usage.py`

**Intermediate**:
1. Read [README.md](README.md) API reference
2. Explore all examples in `examples/`
3. Build your first application

**Advanced**:
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Explore quantum operations
3. Contribute to the project

## 📦 Package Contents

```
zerodb_mcp/
├── client.py          # Main client
├── auth.py            # Authentication
├── exceptions.py      # Error handling
├── models.py          # Data models
├── utils.py           # Utilities
└── operations/
    ├── vectors.py     # Vector ops (10)
    ├── quantum.py     # Quantum ops (6)
    ├── tables.py      # Table ops (8)
    ├── files.py       # File ops (7)
    ├── events.py      # Event ops (5)
    ├── projects.py    # Project ops (7)
    ├── rlhf.py        # RLHF ops (10)
    └── admin.py       # Admin ops (5)
```

## 🚦 Next Steps

1. **Install**: `pip install zerodb-mcp`
2. **Configure**: Add API key to `.env`
3. **Quick Start**: Read [QUICKSTART.md](QUICKSTART.md)
4. **Build**: Create your first application
5. **Explore**: Try all the examples

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

**Ready to start?** → Go to [INSTALLATION.md](INSTALLATION.md)

**Need help?** → Email support@ainative.studio

**Version**: 1.0.0 | **Status**: Production Ready ✅
