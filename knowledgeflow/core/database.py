"""
Database module for KnowledgeFlow
Handles all database operations and schema management
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json

# Database path
DB_PATH = Path(__file__).parent.parent / "knowledgeflow.db"


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_database():
    """Initialize database with all tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            tags TEXT DEFAULT '[]',
            category_id INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
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
            category_id INTEGER,
            linked_note_id INTEGER,
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (linked_note_id) REFERENCES notes(id)
        )
    """)
    
    # Note links table (NEW)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_note_id INTEGER NOT NULL,
            target_note_id INTEGER NOT NULL,
            link_type TEXT DEFAULT 'reference',
            created_at TEXT NOT NULL,
            FOREIGN KEY (source_note_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY (target_note_id) REFERENCES notes(id) ON DELETE CASCADE,
            UNIQUE(source_note_id, target_note_id)
        )
    """)
    
    # Categories table (NEW)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            type TEXT DEFAULT 'note',
            created_at TEXT NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    
    return True


# Migration functions
def migrate_existing_data():
    """Migrate data from old schema if needed"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if we need to add new columns to existing tables
    cursor.execute("PRAGMA table_info(notes)")
    notes_columns = [col[1] for col in cursor.fetchall()]
    
    if 'category_id' not in notes_columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN category_id INTEGER REFERENCES categories(id)")
    
    cursor.execute("PRAGMA table_info(tasks)")
    tasks_columns = [col[1] for col in cursor.fetchall()]
    
    if 'tags' not in tasks_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN tags TEXT DEFAULT '[]'")
    if 'category_id' not in tasks_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN category_id INTEGER REFERENCES categories(id)")
    if 'linked_note_id' not in tasks_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN linked_note_id INTEGER REFERENCES notes(id)")
    if 'completed_at' not in tasks_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN completed_at TEXT")
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    migrate_existing_data()
    print("✓ Database initialized and migrated")
