#!/usr/bin/env python3
"""
Tests for enhanced data model (Phase 1.2)
Tests note linking, categories, and task-note associations
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "knowledgeflow"))

from core.database import init_database, get_connection, DB_PATH
from core.links import create_link, get_forward_links, get_backlinks, detect_links_in_content, auto_create_links
from core.categories import (
    create_category, get_all_categories, assign_category_to_note,
    assign_category_to_task, get_notes_by_category, get_tasks_by_category
)
from core.models import Note, Task
import json
from datetime import datetime


def setup_test_db():
    """Setup fresh test database"""
    if DB_PATH.exists():
        os.remove(DB_PATH)
    init_database()
    print("✓ Test database initialized")


def create_test_note(title, content="Test content", tags=None):
    """Helper to create a test note"""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    tags_str = json.dumps(tags or [])
    
    cursor.execute("""
        INSERT INTO notes (title, content, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (title, content, tags_str, now, now))
    
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return note_id


def create_test_task(title, priority="medium"):
    """Helper to create a test task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute("""
        INSERT INTO tasks (title, priority, created_at)
        VALUES (?, ?, ?)
    """, (title, priority, now))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def test_note_linking():
    """Test note linking functionality"""
    print("\n📎 Testing note linking...")
    
    # Create test notes
    note1 = create_test_note("Python Basics", "Learn Python programming")
    note2 = create_test_note("Django Tutorial", "Web framework for Python")
    note3 = create_test_note("Flask Guide", "Lightweight Python web framework")
    
    # Create links
    link1 = create_link(note2, note1, "reference")  # Django references Python
    link2 = create_link(note3, note1, "reference")  # Flask references Python
    
    assert link1 is not None, "Failed to create link 1"
    assert link2 is not None, "Failed to create link 2"
    print("  ✓ Created note links")
    
    # Test forward links (from Django)
    forward = get_forward_links(note2)
    assert len(forward) == 1, f"Expected 1 forward link, got {len(forward)}"
    assert forward[0][0] == note1, "Forward link should point to Python Basics"
    print("  ✓ Forward links work")
    
    # Test backlinks (to Python Basics)
    backlinks = get_backlinks(note1)
    assert len(backlinks) == 2, f"Expected 2 backlinks, got {len(backlinks)}"
    print("  ✓ Backlinks work")
    
    # Test duplicate prevention
    duplicate = create_link(note2, note1)
    assert duplicate is None, "Should not allow duplicate links"
    print("  ✓ Duplicate prevention works")
    
    print("✅ Note linking tests passed!")


def test_link_detection():
    """Test automatic link detection in content"""
    print("\n🔍 Testing link detection...")
    
    # Create notes
    note1 = create_test_note("Python", "Programming language")
    note2 = create_test_note("Django", "See [[Python]] for basics")
    
    # Detect links
    links = detect_links_in_content("See [[Python]] for basics")
    assert len(links) == 1, f"Expected 1 link, found {len(links)}"
    assert links[0] == "Python", f"Expected 'Python', got '{links[0]}'"
    print("  ✓ Link detection works")
    
    # Auto-create links
    created = auto_create_links(note2, "See [[Python]] for basics")
    assert created == 1, f"Expected 1 link created, got {created}"
    print("  ✓ Auto-link creation works")
    
    # Verify link was created
    forward = get_forward_links(note2)
    assert len(forward) == 1, "Auto-created link should exist"
    print("  ✓ Auto-created link verified")
    
    print("✅ Link detection tests passed!")


def test_categories():
    """Test category functionality"""
    print("\n🗂️  Testing categories...")
    
    # Create categories
    coding = create_category("Coding", type='note')
    python = create_category("Python", parent_id=coding, type='note')
    work = create_category("Work", type='task')
    
    assert coding is not None, "Failed to create 'Coding' category"
    assert python is not None, "Failed to create 'Python' category"
    assert work is not None, "Failed to create 'Work' category"
    print("  ✓ Created categories")
    
    # Get all categories
    all_cats = get_all_categories()
    assert len(all_cats) >= 3, f"Expected at least 3 categories, got {len(all_cats)}"
    print("  ✓ Retrieved categories")
    
    # Filter by type
    note_cats = get_all_categories(type='note')
    task_cats = get_all_categories(type='task')
    assert len(note_cats) >= 2, "Should have note categories"
    assert len(task_cats) >= 1, "Should have task categories"
    print("  ✓ Category filtering works")
    
    # Assign category to note
    note_id = create_test_note("Test Note")
    success = assign_category_to_note(note_id, python)
    assert success, "Failed to assign category to note"
    print("  ✓ Assigned category to note")
    
    # Get notes by category
    notes = get_notes_by_category(python)
    assert len(notes) >= 1, "Should have notes in category"
    print("  ✓ Retrieved notes by category")
    
    # Assign category to task
    task_id = create_test_task("Test Task")
    success = assign_category_to_task(task_id, work)
    assert success, "Failed to assign category to task"
    print("  ✓ Assigned category to task")
    
    print("✅ Category tests passed!")


def test_task_note_association():
    """Test linking tasks to notes"""
    print("\n📋 Testing task-note associations...")
    
    # Create a note and task
    note_id = create_test_note("Project Documentation", "Write docs for the project")
    task_id = create_test_task("Write documentation", priority="high")
    
    # Link task to note
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET linked_note_id = ? WHERE id = ?", (note_id, task_id))
    conn.commit()
    conn.close()
    print("  ✓ Linked task to note")
    
    # Verify link
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT linked_note_id FROM tasks WHERE id = ?", (task_id,))
    result = cursor.fetchone()
    conn.close()
    
    assert result['linked_note_id'] == note_id, "Task should be linked to note"
    print("  ✓ Verified task-note link")
    
    print("✅ Task-note association tests passed!")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("🧪 Running Enhanced Data Model Tests (Phase 1.2)")
    print("="*60)
    
    setup_test_db()
    
    try:
        test_note_linking()
        test_link_detection()
        test_categories()
        test_task_note_association()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    
    finally:
        # Cleanup
        if DB_PATH.exists():
            os.remove(DB_PATH)
            print("\n🧹 Test database cleaned up")
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
