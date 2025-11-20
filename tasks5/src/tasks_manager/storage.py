"""
Task Storage Module
Handles persistent storage of tasks in JSON format.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import uuid


class TaskStorage:
    """Manages task storage in a local JSON file."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize task storage.
        
        Args:
            storage_path: Path to the storage file. Defaults to ~/.tasks/tasks.json
        """
        if storage_path is None:
            storage_path = Path.home() / ".tasks" / "tasks.json"
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize empty file if it doesn't exist
        if not self.storage_path.exists():
            self._save_tasks([])
    
    def _load_tasks(self) -> List[Dict]:
        """Load all tasks from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_tasks(self, tasks: List[Dict]):
        """Save all tasks to storage atomically."""
        # Write to temp file first, then rename (atomic operation)
        temp_path = self.storage_path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(tasks, f, indent=2)
        temp_path.replace(self.storage_path)
    
    def create_task(self, title: str, description: str = "", 
                   status: str = "pending", priority: str = "medium",
                   due_date: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description
            status: Task status (pending, in-progress, completed)
            priority: Task priority (low, medium, high)
            due_date: Due date (ISO format string)
            tags: List of tags
            
        Returns:
            Created task dictionary
        """
        tasks = self._load_tasks()
        
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        tasks.append(task)
        self._save_tasks(tasks)
        return task
    
    def list_tasks(self, status: Optional[str] = None, 
                   priority: Optional[str] = None) -> List[Dict]:
        """
        List all tasks, optionally filtered.
        
        Args:
            status: Filter by status
            priority: Filter by priority
            
        Returns:
            List of task dictionaries
        """
        tasks = self._load_tasks()
        
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
            
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task dictionary or None if not found
        """
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Dict]:
        """
        Update a task.
        
        Args:
            task_id: Task ID
            **kwargs: Fields to update
            
        Returns:
            Updated task dictionary or None if not found
        """
        tasks = self._load_tasks()
        
        for task in tasks:
            if task["id"] == task_id:
                # Update fields
                for key, value in kwargs.items():
                    if key in task and value is not None:
                        task[key] = value
                task["updated_at"] = datetime.now().isoformat()
                
                self._save_tasks(tasks)
                return task
        
        return None
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if deleted, False if not found
        """
        tasks = self._load_tasks()
        original_len = len(tasks)
        
        tasks = [t for t in tasks if t["id"] != task_id]
        
        if len(tasks) < original_len:
            self._save_tasks(tasks)
            return True
        return False
    
    def search_tasks(self, query: str) -> List[Dict]:
        """
        Search tasks by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching tasks
        """
        tasks = self._load_tasks()
        query_lower = query.lower()
        
        results = []
        for task in tasks:
            if (query_lower in task["title"].lower() or 
                query_lower in task["description"].lower() or
                any(query_lower in tag.lower() for tag in task["tags"])):
                results.append(task)
        
        return results
