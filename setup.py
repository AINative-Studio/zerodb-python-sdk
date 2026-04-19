"""
ZeroDB MCP Python Client SDK Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="zerodb-mcp",
    version="1.1.0",
    author="AINative Studio",
    author_email="support@ainative.studio",
    description="Production-ready Python client for ZeroDB MCP Bridge API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ainative.studio/products/zerodb",
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.24.0,<1.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    keywords="zerodb mcp ainative vector-database semantic-search agent-memory agent-cloud",
    project_urls={
        "Homepage": "https://ainative.studio/products/zerodb",
        "Documentation": "https://docs.ainative.studio",
        "Repository": "https://github.com/AINative-Studio/core",
        "Bug Tracker": "https://github.com/AINative-Studio/core/issues",
    },
)
