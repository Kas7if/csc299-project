#!/usr/bin/env python3
"""
Tasks2 - Iteration on PKMS/Task Management System
Enhanced from tasks1 with note management and linking capabilities
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

# Database setup
DB_PATH = Path(__file__).parent / "pkms.db"


def init_db():
    """Initialize database with notes and tasks tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Notes table - NEW in tasks2!
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
    
    # Tasks table - Enhanced from tasks1
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
    
    # Note links table - NEW for knowledge graph!
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
    print("✓ Database initialized")


# Note operations - NEW in tasks2!

def create_note(title: str, content: str = "", tags: List[str] = None) -> int:
    """Create a new note"""
    conn = sqlite3.connect(DB_PATH)
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


def list_notes() -> List[Dict]:
    """List all notes"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    for note in notes:
        note['tags'] = json.loads(note['tags'])
    
    return notes


def search_notes(query: str) -> List[Dict]:
    """Search notes by title or content"""
    conn = sqlite3.connect(DB_PATH)
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


def link_notes(source_id: int, target_id: int) -> bool:
    """Create a link between two notes - NEW feature!"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO note_links (source_note_id, target_note_id, created_at)
            VALUES (?, ?, ?)
        """, (source_id, target_id, now))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_linked_notes(note_id: int) -> List[Dict]:
    """Get all notes linked to this note"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.id, n.title
        FROM note_links nl
        JOIN notes n ON nl.target_note_id = n.id
        WHERE nl.source_note_id = ?
    """, (note_id,))
    
    links = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return links


# Task operations - Enhanced from tasks1

def create_task(title: str, description: str = "", priority: str = "medium", 
                due_date: str = None, tags: List[str] = None) -> int:
    """Create a new task"""
    conn = sqlite3.connect(DB_PATH)
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


def list_tasks(status: str = None) -> List[Dict]:
    """List tasks, optionally filtered by status"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if status:
        cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY priority, due_date", (status,))
    else:
        cursor.execute("SELECT * FROM tasks ORDER BY priority, due_date")
    
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    for task in tasks:
        task['tags'] = json.loads(task['tags'])
    
    return tasks


def complete_task(task_id: int) -> bool:
    """Mark a task as complete"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    success = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return success


def link_task_to_note(task_id: int, note_id: int) -> bool:
    """Link a task to a note - NEW feature!"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET linked_note_id = ? WHERE id = ?", (note_id, task_id))
    success = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return success


# CLI Interface

def print_help():
    """Print available commands"""
    print("\n📖 Available Commands:")
    print("-" * 60)
    print("  NOTES:")
    print("    note <title>       - Create a new note")
    print("    notes              - List all notes")
    print("    search <query>     - Search notes")
    print("    link <id1> <id2>   - Link two notes together")
    print("    links <id>         - Show links for a note")
    print()
    print("  TASKS:")
    print("    task <title>       - Create a new task")
    print("    tasks              - List all tasks")
    print("    tasks pending      - List pending tasks")
    print("    done <id>          - Mark task as complete")
    print("    attach <task> <note> - Link task to note")
    print()
    print("  GENERAL:")
    print("    help               - Show this help")
    print("    quit               - Exit")
    print("-" * 60)


def main():
    """Main CLI interface"""
    init_db()
    
    print("\n" + "="*60)
    print("📚 Personal Knowledge & Task Management System (tasks2)")
    print("="*60)
    print("Type 'help' for commands, 'quit' to exit")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Note commands
            if command == "note":
                if not args:
                    print("Usage: note <title>")
                else:
                    content = input("Content: ")
                    tags_input = input("Tags (comma-separated): ")
                    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                    note_id = create_note(args, content, tags)
                    print(f"✓ Note #{note_id} created: {args}")
            
            elif command == "notes":
                notes = list_notes()
                if not notes:
                    print("No notes found.")
                else:
                    print(f"\n📝 Notes ({len(notes)}):")
                    for note in notes:
                        tags_str = f" [{', '.join(note['tags'])}]" if note['tags'] else ""
                        print(f"  #{note['id']} - {note['title']}{tags_str}")
            
            elif command == "search":
                if not args:
                    print("Usage: search <query>")
                else:
                    results = search_notes(args)
                    print(f"\n🔍 Found {len(results)} results for '{args}':")
                    for note in results:
                        print(f"  #{note['id']} - {note['title']}")
            
            elif command == "link":
                try:
                    ids = args.split()
                    if len(ids) != 2:
                        print("Usage: link <note_id1> <note_id2>")
                    else:
                        id1, id2 = int(ids[0]), int(ids[1])
                        if link_notes(id1, id2):
                            print(f"✓ Linked notes #{id1} → #{id2}")
                        else:
                            print("✗ Could not create link")
                except ValueError:
                    print("Usage: link <note_id1> <note_id2>")
            
            elif command == "links":
                try:
                    note_id = int(args)
                    links = get_linked_notes(note_id)
                    if not links:
                        print(f"No links found for note #{note_id}")
                    else:
                        print(f"\n🔗 Links from note #{note_id}:")
                        for link in links:
                            print(f"  → #{link['id']} - {link['title']}")
                except ValueError:
                    print("Usage: links <note_id>")
            
            # Task commands
            elif command == "task":
                if not args:
                    print("Usage: task <title>")
                else:
                    priority = input("Priority (high/medium/low) [medium]: ") or "medium"
                    due_date = input("Due date (YYYY-MM-DD): ") or None
                    task_id = create_task(args, priority=priority, due_date=due_date)
                    print(f"✓ Task #{task_id} created: {args}")
            
            elif command == "tasks":
                status = args if args in ['pending', 'done'] else None
                tasks = list_tasks(status)
                if not tasks:
                    print("No tasks found.")
                else:
                    status_str = f" ({args})" if args else ""
                    print(f"\n✅ Tasks{status_str} ({len(tasks)}):")
                    for task in tasks:
                        status_icon = "✓" if task['status'] == 'done' else "○"
                        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                        due_str = f" (Due: {task['due_date']})" if task['due_date'] else ""
                        note_str = f" 📎#{task['linked_note_id']}" if task['linked_note_id'] else ""
                        print(f"  {status_icon} #{task['id']} {priority_icon} {task['title']}{due_str}{note_str}")
            
            elif command == "done":
                try:
                    task_id = int(args)
                    if complete_task(task_id):
                        print(f"✓ Task #{task_id} completed!")
                    else:
                        print(f"✗ Task #{task_id} not found")
                except ValueError:
                    print("Usage: done <task_id>")
            
            elif command == "attach":
                try:
                    ids = args.split()
                    if len(ids) != 2:
                        print("Usage: attach <task_id> <note_id>")
                    else:
                        task_id, note_id = int(ids[0]), int(ids[1])
                        if link_task_to_note(task_id, note_id):
                            print(f"✓ Task #{task_id} linked to note #{note_id}")
                        else:
                            print("✗ Could not link task to note")
                except ValueError:
                    print("Usage: attach <task_id> <note_id>")
            
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
