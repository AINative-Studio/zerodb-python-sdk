#!/usr/bin/env python3
"""
Verify ZeroDB MCP Python SDK package structure and imports
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))


def verify_imports():
    """Verify all package imports work correctly"""
    print("=" * 60)
    print("ZeroDB MCP Python SDK - Package Verification")
    print("=" * 60)

    errors = []

    # Test main package import
    print("\n1. Testing main package import...")
    try:
        import zerodb_mcp
        print(f"   ✓ zerodb_mcp imported successfully")
        print(f"   Version: {zerodb_mcp.__version__}")
    except Exception as e:
        errors.append(f"Failed to import zerodb_mcp: {e}")
        print(f"   ✗ Error: {e}")

    # Test client import
    print("\n2. Testing client import...")
    try:
        from zerodb_mcp import ZeroDBClient
        print(f"   ✓ ZeroDBClient imported")
    except Exception as e:
        errors.append(f"Failed to import ZeroDBClient: {e}")
        print(f"   ✗ Error: {e}")

    # Test exceptions
    print("\n3. Testing exception imports...")
    try:
        from zerodb_mcp import (
            ZeroDBError,
            AuthenticationError,
            RateLimitError,
            ValidationError,
            ResourceNotFoundError,
            QuotaExceededError,
        )
        print(f"   ✓ All exceptions imported")
    except Exception as e:
        errors.append(f"Failed to import exceptions: {e}")
        print(f"   ✗ Error: {e}")

    # Test models
    print("\n4. Testing model imports...")
    try:
        from zerodb_mcp import (
            VectorUpsertRequest,
            VectorSearchRequest,
            VectorSearchResult,
            QuantumCompressionRequest,
            TableCreateRequest,
            FileUploadRequest,
            ProjectCreateRequest,
        )
        print(f"   ✓ All models imported")
    except Exception as e:
        errors.append(f"Failed to import models: {e}")
        print(f"   ✗ Error: {e}")

    # Test operation modules
    print("\n5. Testing operation modules...")
    try:
        from zerodb_mcp.operations import (
            VectorOperations,
            QuantumOperations,
            TableOperations,
            FileOperations,
            EventOperations,
            ProjectOperations,
            RLHFOperations,
            AdminOperations,
        )
        print(f"   ✓ All operation modules imported")
    except Exception as e:
        errors.append(f"Failed to import operations: {e}")
        print(f"   ✗ Error: {e}")

    # Count operations
    print("\n6. Verifying operation counts...")
    try:
        from zerodb_mcp.operations import vectors, quantum, tables, files, events, projects, rlhf, admin

        operations_count = {
            "vectors": len([m for m in dir(vectors.VectorOperations) if not m.startswith('_') and m != 'client']),
            "quantum": len([m for m in dir(quantum.QuantumOperations) if not m.startswith('_') and m != 'client']),
            "tables": len([m for m in dir(tables.TableOperations) if not m.startswith('_') and m != 'client']),
            "files": len([m for m in dir(files.FileOperations) if not m.startswith('_') and m != 'client']),
            "events": len([m for m in dir(events.EventOperations) if not m.startswith('_') and m != 'client']),
            "projects": len([m for m in dir(projects.ProjectOperations) if not m.startswith('_') and m != 'client']),
            "rlhf": len([m for m in dir(rlhf.RLHFOperations) if not m.startswith('_') and m != 'client']),
            "admin": len([m for m in dir(admin.AdminOperations) if not m.startswith('_') and m != 'client']),
        }

        total_ops = sum(operations_count.values())
        print(f"   ✓ Total operations: {total_ops}")
        for module, count in operations_count.items():
            print(f"     - {module}: {count} operations")

    except Exception as e:
        errors.append(f"Failed to count operations: {e}")
        print(f"   ✗ Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("VERIFICATION FAILED")
        print(f"Errors found: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ ALL VERIFICATIONS PASSED")
        print("\nPackage is ready for use!")
        return True


def verify_files():
    """Verify all expected files exist"""
    print("\n" + "=" * 60)
    print("File Structure Verification")
    print("=" * 60)

    base_path = Path(__file__).parent

    required_files = [
        # Root files
        "README.md",
        "QUICKSTART.md",
        "CHANGELOG.md",
        "LICENSE",
        "setup.py",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        ".env.example",
        ".gitignore",

        # Package files
        "zerodb_mcp/__init__.py",
        "zerodb_mcp/client.py",
        "zerodb_mcp/auth.py",
        "zerodb_mcp/exceptions.py",
        "zerodb_mcp/models.py",
        "zerodb_mcp/utils.py",

        # Operations
        "zerodb_mcp/operations/__init__.py",
        "zerodb_mcp/operations/vectors.py",
        "zerodb_mcp/operations/quantum.py",
        "zerodb_mcp/operations/tables.py",
        "zerodb_mcp/operations/files.py",
        "zerodb_mcp/operations/events.py",
        "zerodb_mcp/operations/projects.py",
        "zerodb_mcp/operations/rlhf.py",
        "zerodb_mcp/operations/admin.py",

        # Tests
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_client.py",
        "tests/test_vectors.py",
        "tests/test_utils.py",

        # Examples
        "examples/basic_usage.py",
        "examples/quantum_operations.py",
        "examples/file_upload.py",
        "examples/rlhf_tracking.py",
    ]

    missing_files = []
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (MISSING)")
            missing_files.append(file_path)

    print("\n" + "=" * 60)
    if missing_files:
        print(f"MISSING FILES: {len(missing_files)}")
        return False
    else:
        print(f"✓ ALL {len(required_files)} FILES PRESENT")
        return True


if __name__ == "__main__":
    print("\n")
    files_ok = verify_files()
    imports_ok = verify_imports()

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    if files_ok and imports_ok:
        print("✓ Package verification SUCCESSFUL")
        print("\nThe ZeroDB MCP Python SDK is ready for distribution!")
        print("\nNext steps:")
        print("  1. Install in dev mode: pip install -e .[dev]")
        print("  2. Run tests: pytest")
        print("  3. Build package: python -m build")
        print("  4. Publish to PyPI: python -m twine upload dist/*")
        sys.exit(0)
    else:
        print("✗ Package verification FAILED")
        print("\nPlease fix the errors above before proceeding.")
        sys.exit(1)
