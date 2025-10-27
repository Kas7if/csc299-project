#!/usr/bin/env python3
"""
Basic tests for KnowledgeFlow
Run with: python -m pytest tests/test_basic.py -v
"""

import sqlite3
import os
import sys
from pathlib import Path

# Add parent directory to path to import knowledgeflow modules
sys.path.insert(0, str(Path(__file__).parent.parent / "knowledgeflow"))

from main import init_db, create_note, create_task, DB_PATH


def setup_test_db():
    """Setup a fresh test database"""
    if DB_PATH.exists():
        os.remove(DB_PATH)
    init_db()


def test_create_note():
    """Test note creation"""
    print("Testing note creation...")
    note_id = create_note("Test Note", "This is a test", ["test", "prototype"])
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Note not found in database"
    assert result[0] == "Test Note", "Note title doesn't match"
    print("✓ Note creation test passed")


def test_create_task():
    """Test task creation"""
    print("Testing task creation...")
    task_id = create_task("Test Task", priority="high", due_date="2025-11-01")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, priority FROM tasks WHERE id = ?", (task_id,))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None, "Task not found in database"
    assert result[0] == "Test Task", "Task title doesn't match"
    assert result[1] == "high", "Task priority doesn't match"
    print("✓ Task creation test passed")


def test_search():
    """Test search functionality"""
    print("Testing search...")
    create_note("Python Tutorial", "Learn Python programming", ["python", "tutorial"])
    create_note("JavaScript Guide", "Learn JavaScript", ["javascript"])
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notes WHERE content LIKE ?", ("%Python%",))
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count >= 1, "Search should find at least one note"
    print("✓ Search test passed")


if __name__ == "__main__":
    print("\n🧪 Running Prototype 1 Tests\n")
    setup_test_db()
    
    try:
        test_create_note()
        test_create_task()
        test_search()
        print("\n✅ All tests passed!\n")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
    finally:
        # Cleanup
        if DB_PATH.exists():
            os.remove(DB_PATH)
            print("🧹 Test database cleaned up")
