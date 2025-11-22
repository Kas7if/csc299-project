"""
JSON Storage Layer
Simple, portable storage for notes and tasks using JSON files
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import uuid


class JSONStorage:
    """Manages JSON-based storage for notes and tasks"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize JSON storage"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.notes_file = self.data_dir / "notes.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.links_file = self.data_dir / "links.json"
        
        # Initialize files if they don't exist
        self._ensure_file(self.notes_file, [])
        self._ensure_file(self.tasks_file, [])
        self._ensure_file(self.links_file, [])
    
    def _ensure_file(self, filepath: Path, default_content):
        """Ensure file exists with default content"""
        if not filepath.exists():
            self._write_json(filepath, default_content)
    
    def _read_json(self, filepath: Path):
        """Read JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return [] if filepath.name in ['notes.json', 'tasks.json', 'links.json'] else {}
    
    def _write_json(self, filepath: Path, data):
        """Write JSON file atomically"""
        temp_file = filepath.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2)
        temp_file.replace(filepath)
    
    # ===== NOTES =====
    
    def create_note(self, title: str, content: str = "", tags: List[str] = None) -> Dict:
        """Create a new note"""
        notes = self._read_json(self.notes_file)
        
        note = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        notes.append(note)
        self._write_json(self.notes_file, notes)
        return note
    
    def get_note(self, note_id: str) -> Optional[Dict]:
        """Get a note by ID"""
        notes = self._read_json(self.notes_file)
        for note in notes:
            if note["id"] == note_id:
                return note
        return None
    
    def list_notes(self, tag: Optional[str] = None) -> List[Dict]:
        """List all notes, optionally filtered by tag"""
        notes = self._read_json(self.notes_file)
        if tag:
            notes = [n for n in notes if tag in n.get("tags", [])]
        return notes
    
    def update_note(self, note_id: str, **kwargs) -> Optional[Dict]:
        """Update a note"""
        notes = self._read_json(self.notes_file)
        
        for note in notes:
            if note["id"] == note_id:
                for key, value in kwargs.items():
                    if key in note and value is not None:
                        note[key] = value
                note["updated_at"] = datetime.now().isoformat()
                self._write_json(self.notes_file, notes)
                return note
        return None
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note"""
        notes = self._read_json(self.notes_file)
        original_len = len(notes)
        notes = [n for n in notes if n["id"] != note_id]
        
        if len(notes) < original_len:
            self._write_json(self.notes_file, notes)
            # Also remove any links involving this note
            self._remove_links_for_item(note_id)
            return True
        return False
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by query"""
        notes = self._read_json(self.notes_file)
        query_lower = query.lower()
        
        results = []
        for note in notes:
            if (query_lower in note["title"].lower() or 
                query_lower in note.get("content", "").lower() or
                any(query_lower in tag.lower() for tag in note.get("tags", []))):
                results.append(note)
        return results
    
    # ===== TASKS =====
    
    def create_task(self, title: str, description: str = "", 
                   status: str = "pending", priority: str = "medium",
                   due_date: Optional[str] = None, tags: List[str] = None,
                   linked_note_id: Optional[str] = None) -> Dict:
        """Create a new task"""
        tasks = self._read_json(self.tasks_file)
        
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "tags": tags or [],
            "linked_note_id": linked_note_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        tasks.append(task)
        self._write_json(self.tasks_file, tasks)
        return task
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a task by ID"""
        tasks = self._read_json(self.tasks_file)
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def list_tasks(self, status: Optional[str] = None, 
                  priority: Optional[str] = None) -> List[Dict]:
        """List all tasks with optional filters"""
        tasks = self._read_json(self.tasks_file)
        
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]
        
        return tasks
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Dict]:
        """Update a task"""
        tasks = self._read_json(self.tasks_file)
        
        for task in tasks:
            if task["id"] == task_id:
                for key, value in kwargs.items():
                    if key in task and value is not None:
                        task[key] = value
                task["updated_at"] = datetime.now().isoformat()
                self._write_json(self.tasks_file, tasks)
                return task
        return None
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        tasks = self._read_json(self.tasks_file)
        original_len = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]
        
        if len(tasks) < original_len:
            self._write_json(self.tasks_file, tasks)
            self._remove_links_for_item(task_id)
            return True
        return False
    
    def search_tasks(self, query: str) -> List[Dict]:
        """Search tasks by query"""
        tasks = self._read_json(self.tasks_file)
        query_lower = query.lower()
        
        results = []
        for task in tasks:
            if (query_lower in task["title"].lower() or 
                query_lower in task.get("description", "").lower() or
                any(query_lower in tag.lower() for tag in task.get("tags", []))):
                results.append(task)
        return results
    
    # ===== LINKS =====
    
    def create_link(self, from_id: str, to_id: str, link_type: str = "relates_to") -> Dict:
        """Create a link between notes or tasks"""
        links = self._read_json(self.links_file)
        
        # Check if link already exists
        for link in links:
            if link["from_id"] == from_id and link["to_id"] == to_id:
                return link
        
        link = {
            "id": str(uuid.uuid4()),
            "from_id": from_id,
            "to_id": to_id,
            "link_type": link_type,
            "created_at": datetime.now().isoformat()
        }
        
        links.append(link)
        self._write_json(self.links_file, links)
        return link
    
    def get_links(self, item_id: str) -> List[Dict]:
        """Get all links for an item (both from and to)"""
        links = self._read_json(self.links_file)
        return [l for l in links if l["from_id"] == item_id or l["to_id"] == item_id]
    
    def _remove_links_for_item(self, item_id: str):
        """Remove all links involving an item"""
        links = self._read_json(self.links_file)
        links = [l for l in links if l["from_id"] != item_id and l["to_id"] != item_id]
        self._write_json(self.links_file, links)
    
    # ===== UNIFIED SEARCH =====
    
    def search_all(self, query: str) -> Dict[str, List[Dict]]:
        """Search across notes and tasks"""
        return {
            "notes": self.search_notes(query),
            "tasks": self.search_tasks(query)
        }
