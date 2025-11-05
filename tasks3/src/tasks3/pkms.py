"""
PKMS (Personal Knowledge Management System) core functionality
Adapted from tasks2 for tasks3 with pytest integration
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict


class PKMS:
    """Personal Knowledge Management System with notes, tasks, and linking"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize PKMS with a database path"""
        if db_path is None:
            db_path = Path.cwd() / "pkms.db"
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with notes and tasks tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                tags TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                tags TEXT DEFAULT '[]',
                linked_note_id INTEGER,
                created_at TEXT NOT NULL,
                FOREIGN KEY (linked_note_id) REFERENCES notes(id)
            )
        """)
        
        # Note links table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS note_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_note_id INTEGER NOT NULL,
                target_note_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (source_note_id) REFERENCES notes(id) ON DELETE CASCADE,
                FOREIGN KEY (target_note_id) REFERENCES notes(id) ON DELETE CASCADE,
                UNIQUE(source_note_id, target_note_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_note(self, title: str, content: str = "", tags: List[str] = None) -> int:
        """Create a new note and return its ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        tags_json = json.dumps(tags or [])
        
        cursor.execute("""
            INSERT INTO notes (title, content, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, content, tags_json, now, now))
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a single note by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            note = dict(row)
            note['tags'] = json.loads(note['tags'])
            return note
        return None
    
    def list_notes(self) -> List[Dict]:
        """List all notes"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for note in notes:
            note['tags'] = json.loads(note['tags'])
        
        return notes
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by title or content"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM notes 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_at DESC
        """, (f"%{query}%", f"%{query}%"))
        
        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for note in notes:
            note['tags'] = json.loads(note['tags'])
        
        return notes
    
    def link_notes(self, source_id: int, target_id: int) -> bool:
        """Create a link between two notes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO note_links (source_note_id, target_note_id, created_at)
                VALUES (?, ?, ?)
            """, (source_id, target_id, now))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_linked_notes(self, note_id: int) -> List[Dict]:
        """Get all notes linked from a given note"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT n.* 
            FROM note_links nl
            JOIN notes n ON nl.target_note_id = n.id
            WHERE nl.source_note_id = ?
        """, (note_id,))
        
        links = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for link in links:
            link['tags'] = json.loads(link['tags'])
        
        return links
    
    def create_task(self, title: str, description: str = "", priority: str = "medium", 
                    due_date: str = None, tags: List[str] = None) -> int:
        """Create a new task and return its ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        tags_json = json.dumps(tags or [])
        
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, due_date, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, priority, due_date, tags_json, now))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a single task by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            task = dict(row)
            task['tags'] = json.loads(task['tags'])
            return task
        return None
    
    def list_tasks(self, status: str = None) -> List[Dict]:
        """List tasks, optionally filtered by status"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY due_date", (status,))
        else:
            cursor.execute("SELECT * FROM tasks ORDER BY due_date")
        
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for task in tasks:
            task['tags'] = json.loads(task['tags'])
        
        return tasks
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def link_task_to_note(self, task_id: int, note_id: int) -> bool:
        """Link a task to a note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE tasks SET linked_note_id = ? WHERE id = ?", (note_id, task_id))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
