"""
Data models for KnowledgeFlow
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class Note:
    """Note model"""
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    category_id: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_db_row(cls, row):
        """Create Note from database row"""
        tags = json.loads(row['tags']) if row['tags'] else []
        return cls(
            id=row['id'],
            title=row['title'],
            content=row['content'] or "",
            tags=tags,
            category_id=row.get('category_id'),
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )


@dataclass
class Task:
    """Task model"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    category_id: Optional[int] = None
    linked_note_id: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date,
            'tags': self.tags,
            'category_id': self.category_id,
            'linked_note_id': self.linked_note_id,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_db_row(cls, row):
        """Create Task from database row"""
        tags = json.loads(row['tags']) if row.get('tags') else []
        return cls(
            id=row['id'],
            title=row['title'],
            description=row.get('description') or "",
            status=row['status'],
            priority=row['priority'],
            due_date=row.get('due_date'),
            tags=tags,
            category_id=row.get('category_id'),
            linked_note_id=row.get('linked_note_id'),
            created_at=row['created_at'],
            completed_at=row.get('completed_at')
        )


@dataclass
class NoteLink:
    """Link between notes"""
    id: Optional[int] = None
    source_note_id: int = 0
    target_note_id: int = 0
    link_type: str = "reference"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            source_note_id=row['source_note_id'],
            target_note_id=row['target_note_id'],
            link_type=row['link_type'],
            created_at=row['created_at']
        )


@dataclass
class Category:
    """Category for organizing notes/tasks"""
    id: Optional[int] = None
    name: str = ""
    parent_id: Optional[int] = None
    type: str = "note"  # 'note', 'task', or 'both'
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            name=row['name'],
            parent_id=row['parent_id'] if row['parent_id'] else None,
            type=row['type'],
            created_at=row['created_at']
        )
