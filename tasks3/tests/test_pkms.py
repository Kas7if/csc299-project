"""
Tests for PKMS (Personal Knowledge Management System)
"""

import pytest
from pathlib import Path
import tempfile
import os
from tasks3.pkms import PKMS


@pytest.fixture
def pkms():
    """Create a temporary PKMS instance for testing"""
    # Create a temporary database file
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Create PKMS instance
    pkms_instance = PKMS(Path(db_path))
    
    yield pkms_instance
    
    # Cleanup: remove the temporary database
    os.unlink(db_path)


def test_create_note(pkms):
    """Test creating a note"""
    note_id = pkms.create_note("Test Note", "This is a test", ["test", "example"])
    
    assert note_id == 1
    
    # Verify the note was created
    note = pkms.get_note(note_id)
    assert note is not None
    assert note['title'] == "Test Note"
    assert note['content'] == "This is a test"
    assert note['tags'] == ["test", "example"]


def test_search_notes(pkms):
    """Test searching notes by content"""
    # Create some notes
    pkms.create_note("Python Tutorial", "Learn Python programming")
    pkms.create_note("JavaScript Guide", "Learn JavaScript")
    pkms.create_note("Python Advanced", "Advanced Python topics")
    
    # Search for "Python"
    results = pkms.search_notes("Python")
    
    assert len(results) == 2
    assert all("Python" in note['title'] for note in results)


def test_link_notes(pkms):
    """Test linking two notes together"""
    # Create two notes
    note1_id = pkms.create_note("Note 1", "First note")
    note2_id = pkms.create_note("Note 2", "Second note")
    
    # Link them
    success = pkms.link_notes(note1_id, note2_id)
    assert success is True
    
    # Verify the link
    linked = pkms.get_linked_notes(note1_id)
    assert len(linked) == 1
    assert linked[0]['id'] == note2_id
    assert linked[0]['title'] == "Note 2"


def test_duplicate_link_prevented(pkms):
    """Test that duplicate links are prevented"""
    note1_id = pkms.create_note("Note 1")
    note2_id = pkms.create_note("Note 2")
    
    # Create first link
    success1 = pkms.link_notes(note1_id, note2_id)
    assert success1 is True
    
    # Try to create duplicate link
    success2 = pkms.link_notes(note1_id, note2_id)
    assert success2 is False


def test_create_task(pkms):
    """Test creating a task"""
    task_id = pkms.create_task(
        "Complete assignment", 
        "Finish the CSC299 project",
        priority="high",
        due_date="2025-11-24",
        tags=["school", "urgent"]
    )
    
    assert task_id == 1
    
    # Verify the task was created
    task = pkms.get_task(task_id)
    assert task is not None
    assert task['title'] == "Complete assignment"
    assert task['description'] == "Finish the CSC299 project"
    assert task['priority'] == "high"
    assert task['status'] == "pending"
    assert task['tags'] == ["school", "urgent"]


def test_complete_task(pkms):
    """Test marking a task as complete"""
    task_id = pkms.create_task("Test Task")
    
    # Task should be pending initially
    task = pkms.get_task(task_id)
    assert task['status'] == "pending"
    
    # Complete the task
    success = pkms.complete_task(task_id)
    assert success is True
    
    # Verify status changed
    task = pkms.get_task(task_id)
    assert task['status'] == "done"


def test_link_task_to_note(pkms):
    """Test linking a task to a note"""
    note_id = pkms.create_note("Project Notes", "Important information")
    task_id = pkms.create_task("Review notes")
    
    # Link task to note
    success = pkms.link_task_to_note(task_id, note_id)
    assert success is True
    
    # Verify the link
    task = pkms.get_task(task_id)
    assert task['linked_note_id'] == note_id


def test_list_tasks_by_status(pkms):
    """Test filtering tasks by status"""
    # Create tasks
    task1_id = pkms.create_task("Task 1")
    task2_id = pkms.create_task("Task 2")
    task3_id = pkms.create_task("Task 3")
    
    # Complete one task
    pkms.complete_task(task2_id)
    
    # List pending tasks
    pending = pkms.list_tasks(status="pending")
    assert len(pending) == 2
    assert all(t['status'] == "pending" for t in pending)
    
    # List done tasks
    done = pkms.list_tasks(status="done")
    assert len(done) == 1
    assert done[0]['id'] == task2_id


def test_list_all_notes(pkms):
    """Test listing all notes"""
    # Create multiple notes
    pkms.create_note("Note 1")
    pkms.create_note("Note 2")
    pkms.create_note("Note 3")
    
    # List all notes
    notes = pkms.list_notes()
    assert len(notes) == 3
