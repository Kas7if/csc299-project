"""
Tests for TaskStorage
"""

import os
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tasks_manager.storage import TaskStorage


def test_create_task():
    """Test creating a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(os.path.join(tmpdir, "tasks.json"))
        
        task = storage.create_task(
            title="Test Task",
            description="Test Description",
            priority="high"
        )
        
        assert task["title"] == "Test Task"
        assert task["description"] == "Test Description"
        assert task["priority"] == "high"
        assert task["status"] == "pending"
        assert "id" in task


def test_list_tasks():
    """Test listing tasks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(os.path.join(tmpdir, "tasks.json"))
        
        storage.create_task("Task 1", priority="high")
        storage.create_task("Task 2", priority="low")
        
        all_tasks = storage.list_tasks()
        assert len(all_tasks) == 2
        
        high_tasks = storage.list_tasks(priority="high")
        assert len(high_tasks) == 1
        assert high_tasks[0]["title"] == "Task 1"


def test_update_task():
    """Test updating a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(os.path.join(tmpdir, "tasks.json"))
        
        task = storage.create_task("Original Title")
        task_id = task["id"]
        
        updated = storage.update_task(task_id, title="Updated Title", status="completed")
        
        assert updated["title"] == "Updated Title"
        assert updated["status"] == "completed"


def test_delete_task():
    """Test deleting a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(os.path.join(tmpdir, "tasks.json"))
        
        task = storage.create_task("Task to Delete")
        task_id = task["id"]
        
        assert storage.delete_task(task_id) == True
        assert storage.get_task(task_id) is None


def test_search_tasks():
    """Test searching tasks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(os.path.join(tmpdir, "tasks.json"))
        
        storage.create_task("Python Project", tags=["coding"])
        storage.create_task("Java Assignment", tags=["coding"])
        storage.create_task("Buy Groceries")
        
        results = storage.search_tasks("project")
        assert len(results) == 1
        assert "Python" in results[0]["title"]
        
        coding_results = storage.search_tasks("coding")
        assert len(coding_results) == 2


if __name__ == "__main__":
    # Run tests
    test_create_task()
    test_list_tasks()
    test_update_task()
    test_delete_task()
    test_search_tasks()
    print("✅ All tests passed!")
