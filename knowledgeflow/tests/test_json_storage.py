"""
Tests for JSON Storage Layer
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from core.json_storage import JSONStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage instance"""
    temp_dir = Path(tempfile.mkdtemp())
    storage = JSONStorage(data_dir=temp_dir)
    yield storage
    # Cleanup
    shutil.rmtree(temp_dir)


class TestJSONStorage:
    """Test suite for JSONStorage"""
    
    # ===== NOTE TESTS =====
    
    def test_create_note(self, temp_storage):
        """Test creating a note"""
        note = temp_storage.create_note(
            title="Test Note",
            content="This is test content",
            tags=["test", "example"]
        )
        
        assert note["title"] == "Test Note"
        assert note["content"] == "This is test content"
        assert "test" in note["tags"]
        assert "id" in note
        assert "created_at" in note
    
    def test_get_note(self, temp_storage):
        """Test retrieving a note"""
        created = temp_storage.create_note(title="Get Test")
        retrieved = temp_storage.get_note(created["id"])
        
        assert retrieved is not None
        assert retrieved["id"] == created["id"]
        assert retrieved["title"] == "Get Test"
    
    def test_list_notes(self, temp_storage):
        """Test listing notes"""
        temp_storage.create_note(title="Note 1", tags=["work"])
        temp_storage.create_note(title="Note 2", tags=["personal"])
        temp_storage.create_note(title="Note 3", tags=["work"])
        
        all_notes = temp_storage.list_notes()
        assert len(all_notes) == 3
        
        work_notes = temp_storage.list_notes(tag="work")
        assert len(work_notes) == 2
    
    def test_update_note(self, temp_storage):
        """Test updating a note"""
        note = temp_storage.create_note(title="Original Title")
        
        updated = temp_storage.update_note(
            note["id"],
            title="Updated Title",
            content="New content"
        )
        
        assert updated["title"] == "Updated Title"
        assert updated["content"] == "New content"
    
    def test_delete_note(self, temp_storage):
        """Test deleting a note"""
        note = temp_storage.create_note(title="To Delete")
        note_id = note["id"]
        
        result = temp_storage.delete_note(note_id)
        assert result is True
        
        deleted = temp_storage.get_note(note_id)
        assert deleted is None
    
    def test_search_notes(self, temp_storage):
        """Test searching notes"""
        temp_storage.create_note(
            title="Python Tutorial",
            content="Learn Python programming"
        )
        temp_storage.create_note(
            title="JavaScript Guide",
            content="Learn JavaScript"
        )
        temp_storage.create_note(
            title="Python Advanced",
            content="Advanced Python concepts"
        )
        
        results = temp_storage.search_notes("python")
        assert len(results) == 2
        
        results = temp_storage.search_notes("javascript")
        assert len(results) == 1
    
    # ===== TASK TESTS =====
    
    def test_create_task(self, temp_storage):
        """Test creating a task"""
        task = temp_storage.create_task(
            title="Test Task",
            description="Task description",
            status="pending",
            priority="high",
            tags=["urgent"]
        )
        
        assert task["title"] == "Test Task"
        assert task["status"] == "pending"
        assert task["priority"] == "high"
        assert "urgent" in task["tags"]
    
    def test_get_task(self, temp_storage):
        """Test retrieving a task"""
        created = temp_storage.create_task(title="Get Task Test")
        retrieved = temp_storage.get_task(created["id"])
        
        assert retrieved is not None
        assert retrieved["id"] == created["id"]
    
    def test_list_tasks_filtered(self, temp_storage):
        """Test listing tasks with filters"""
        temp_storage.create_task(title="Task 1", status="pending", priority="high")
        temp_storage.create_task(title="Task 2", status="completed", priority="low")
        temp_storage.create_task(title="Task 3", status="pending", priority="medium")
        
        pending = temp_storage.list_tasks(status="pending")
        assert len(pending) == 2
        
        high_priority = temp_storage.list_tasks(priority="high")
        assert len(high_priority) == 1
    
    def test_update_task(self, temp_storage):
        """Test updating a task"""
        task = temp_storage.create_task(title="Original", status="pending")
        
        updated = temp_storage.update_task(
            task["id"],
            status="completed",
            priority="low"
        )
        
        assert updated["status"] == "completed"
        assert updated["priority"] == "low"
    
    def test_delete_task(self, temp_storage):
        """Test deleting a task"""
        task = temp_storage.create_task(title="To Delete")
        task_id = task["id"]
        
        result = temp_storage.delete_task(task_id)
        assert result is True
        
        deleted = temp_storage.get_task(task_id)
        assert deleted is None
    
    def test_search_tasks(self, temp_storage):
        """Test searching tasks"""
        temp_storage.create_task(
            title="Fix bug in authentication",
            description="Login not working"
        )
        temp_storage.create_task(
            title="Add new feature",
            description="Authentication improvements"
        )
        
        results = temp_storage.search_tasks("authentication")
        assert len(results) == 2
        
        results = temp_storage.search_tasks("bug")
        assert len(results) == 1
    
    # ===== LINK TESTS =====
    
    def test_create_link(self, temp_storage):
        """Test creating a link"""
        note = temp_storage.create_note(title="Note")
        task = temp_storage.create_task(title="Task")
        
        link = temp_storage.create_link(
            from_id=note["id"],
            to_id=task["id"],
            link_type="supports"
        )
        
        assert link["from_id"] == note["id"]
        assert link["to_id"] == task["id"]
        assert link["link_type"] == "supports"
    
    def test_get_links(self, temp_storage):
        """Test retrieving links"""
        note1 = temp_storage.create_note(title="Note 1")
        note2 = temp_storage.create_note(title="Note 2")
        task = temp_storage.create_task(title="Task")
        
        temp_storage.create_link(note1["id"], note2["id"])
        temp_storage.create_link(note1["id"], task["id"])
        
        links = temp_storage.get_links(note1["id"])
        assert len(links) == 2
    
    def test_delete_removes_links(self, temp_storage):
        """Test that deleting an item removes its links"""
        note = temp_storage.create_note(title="Note")
        task = temp_storage.create_task(title="Task")
        
        temp_storage.create_link(note["id"], task["id"])
        
        temp_storage.delete_note(note["id"])
        
        links = temp_storage.get_links(task["id"])
        assert len(links) == 0
    
    # ===== UNIFIED SEARCH TEST =====
    
    def test_search_all(self, temp_storage):
        """Test unified search across notes and tasks"""
        temp_storage.create_note(title="Python Note", content="About Python")
        temp_storage.create_task(title="Python Task", description="Learn Python")
        temp_storage.create_note(title="JavaScript Note")
        
        results = temp_storage.search_all("python")
        
        assert len(results["notes"]) == 1
        assert len(results["tasks"]) == 1
