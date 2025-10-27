"""
Core package for KnowledgeFlow
"""

from .database import init_database, get_connection, migrate_existing_data
from .models import Note, Task, NoteLink, Category

__all__ = [
    'init_database',
    'get_connection',
    'migrate_existing_data',
    'Note',
    'Task',
    'NoteLink',
    'Category'
]
