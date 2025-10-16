"""
Operation modules for ZeroDB MCP Client

Each module provides a specialized set of operations:
- vectors: Vector storage and search (10 operations)
- quantum: Quantum computing features (6 operations)
- tables: NoSQL table operations (8 operations)
- files: File storage and management (6 operations)
- events: Event tracking (5 operations)
- projects: Project management (7 operations)
- rlhf: Reinforcement Learning from Human Feedback (10 operations)
- admin: Administrative operations (5 operations)
"""

from .vectors import VectorOperations
from .quantum import QuantumOperations
from .tables import TableOperations
from .files import FileOperations
from .events import EventOperations
from .projects import ProjectOperations
from .rlhf import RLHFOperations
from .admin import AdminOperations

__all__ = [
    "VectorOperations",
    "QuantumOperations",
    "TableOperations",
    "FileOperations",
    "EventOperations",
    "ProjectOperations",
    "RLHFOperations",
    "AdminOperations",
]
