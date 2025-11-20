"""
Tasks Manager
A simple task management system with CLI and API.
"""

from .storage import TaskStorage
from .cli import main

__version__ = "1.0.0"
__all__ = ["TaskStorage", "main"]
