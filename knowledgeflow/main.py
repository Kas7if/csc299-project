#!/usr/bin/env python3
"""
Prototype 1: KnowledgeFlow Basic
Exploring: SQLite storage, simple CLI, basic AI integration
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Database setup
DB_PATH = Path(__file__).parent / "knowledgeflow.db"


def init_db():
    """Initialize the database with basic schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            tags TEXT,
            created_at TEXT,
            updated_at TEXT
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
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")


def create_note(title, content, tags=None):
    """Create a new note"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    tags_str = json.dumps(tags) if tags else "[]"
    
    cursor.execute("""
        INSERT INTO notes (title, content, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (title, content, tags_str, now, now))
    
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✓ Note created: #{note_id} - {title}")
    return note_id


def list_notes():
    """List all notes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, tags, created_at FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()
    conn.close()
    
    if not notes:
        print("No notes found.")
        return
    
    print("\n📝 Your Notes:")
    print("-" * 60)
    for note_id, title, tags_str, created in notes:
        tags = json.loads(tags_str)
        tag_display = f" [{', '.join(tags)}]" if tags else ""
        created_date = datetime.fromisoformat(created).strftime("%Y-%m-%d")
        print(f"  #{note_id} - {title}{tag_display}")
        print(f"      Created: {created_date}")
    print("-" * 60)


def view_note(note_id):
    """View a specific note"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, content, tags, created_at FROM notes WHERE id = ?", (note_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f"Note #{note_id} not found.")
        return
    
    title, content, tags_str, created = result
    tags = json.loads(tags_str)
    
    print(f"\n{'='*60}")
    print(f"📄 {title}")
    print(f"{'='*60}")
    print(f"Tags: {', '.join(tags) if tags else 'None'}")
    print(f"Created: {datetime.fromisoformat(created).strftime('%Y-%m-%d %H:%M')}")
    print(f"\n{content}\n")
    print(f"{'='*60}")


def search_notes(query):
    """Search notes by title or content"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, content FROM notes 
        WHERE title LIKE ? OR content LIKE ?
    """, (f"%{query}%", f"%{query}%"))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print(f"No notes found for '{query}'")
        return
    
    print(f"\n🔍 Search results for '{query}':")
    print("-" * 60)
    for note_id, title, content in results:
        preview = content[:80] + "..." if len(content) > 80 else content
        print(f"  #{note_id} - {title}")
        print(f"      {preview}")
    print("-" * 60)


def create_task(title, description=None, priority="medium", due_date=None):
    """Create a new task"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute("""
        INSERT INTO tasks (title, description, priority, due_date, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, priority, due_date, now))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✓ Task created: #{task_id} - {title}")
    return task_id


def list_tasks():
    """List all tasks"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, status, priority, due_date 
        FROM tasks 
        ORDER BY 
            CASE priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END,
            due_date
    """)
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        print("No tasks found.")
        return
    
    print("\n✓ Your Tasks:")
    print("-" * 60)
    for task_id, title, status, priority, due_date in tasks:
        status_icon = "✓" if status == "done" else "○"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
        due_display = f" (Due: {due_date})" if due_date else ""
        print(f"  {status_icon} #{task_id} {priority_icon} {title}{due_display}")
    print("-" * 60)


def complete_task(task_id):
    """Mark a task as complete"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    print(f"✓ Task #{task_id} marked as complete!")


def chat_interface():
    """Simple chat-style interface"""
    print("\n" + "="*60)
    print("🌊 KnowledgeFlow - Prototype 1")
    print("="*60)
    print("Type 'help' for commands, 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("📌 > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            # Parse simple commands
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == "note":
                if not args:
                    print("Usage: note <title>")
                else:
                    content = input("Content: ")
                    tags_input = input("Tags (comma-separated, optional): ")
                    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                    create_note(args, content, tags)
            
            elif command == "notes":
                list_notes()
            
            elif command == "view":
                try:
                    note_id = int(args)
                    view_note(note_id)
                except ValueError:
                    print("Usage: view <note_id>")
            
            elif command == "search":
                if not args:
                    print("Usage: search <query>")
                else:
                    search_notes(args)
            
            elif command == "task":
                if not args:
                    print("Usage: task <title>")
                else:
                    priority = input("Priority (high/medium/low) [medium]: ") or "medium"
                    due_date = input("Due date (YYYY-MM-DD, optional): ") or None
                    create_task(args, priority=priority, due_date=due_date)
            
            elif command == "tasks":
                list_tasks()
            
            elif command == "done":
                try:
                    task_id = int(args)
                    complete_task(task_id)
                except ValueError:
                    print("Usage: done <task_id>")
            
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Print help information"""
    print("\n📖 Available Commands:")
    print("-" * 60)
    print("  note <title>       - Create a new note")
    print("  notes              - List all notes")
    print("  view <id>          - View a specific note")
    print("  search <query>     - Search notes")
    print("  task <title>       - Create a new task")
    print("  tasks              - List all tasks")
    print("  done <id>          - Mark task as complete")
    print("  help               - Show this help")
    print("  quit               - Exit")
    print("-" * 60)


if __name__ == "__main__":
    init_db()
    chat_interface()
