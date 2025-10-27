"""
Category management operations
"""

import sqlite3
from typing import List, Optional
from core.database import get_connection
from core.models import Category
from datetime import datetime


def create_category(name: str, parent_id: Optional[int] = None, type: str = 'note') -> Optional[int]:
    """
    Create a new category
    
    Args:
        name: Category name
        parent_id: Parent category ID (for hierarchical categories)
        type: Category type ('note', 'task', or 'both')
    
    Returns:
        Category ID if successful, None otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO categories (name, parent_id, type, created_at)
            VALUES (?, ?, ?, ?)
        """, (name, parent_id, type, now))
        
        category_id = cursor.lastrowid
        conn.commit()
        return category_id
    
    except sqlite3.IntegrityError:
        # Category name already exists
        return None
    finally:
        conn.close()


def get_category(category_id: int) -> Optional[Category]:
    """Get category by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return Category.from_db_row(row)
    return None


def get_all_categories(type: Optional[str] = None) -> List[Category]:
    """
    Get all categories, optionally filtered by type
    
    Args:
        type: Filter by type ('note', 'task', 'both'), or None for all
    
    Returns:
        List of Category objects
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if type:
        cursor.execute("SELECT * FROM categories WHERE type IN (?, 'both') ORDER BY name", (type,))
    else:
        cursor.execute("SELECT * FROM categories ORDER BY name")
    
    categories = [Category.from_db_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return categories


def get_category_tree(type: Optional[str] = None) -> dict:
    """
    Get categories as a hierarchical tree
    
    Args:
        type: Filter by type
    
    Returns:
        Dictionary representing category tree
    """
    categories = get_all_categories(type)
    
    # Build tree
    tree = {}
    category_dict = {c.id: c for c in categories}
    
    for cat in categories:
        if cat.parent_id is None:
            tree[cat.id] = {
                'category': cat,
                'children': []
            }
    
    # Add children
    for cat in categories:
        if cat.parent_id is not None and cat.parent_id in tree:
            tree[cat.parent_id]['children'].append(cat)
    
    return tree


def assign_category_to_note(note_id: int, category_id: Optional[int]) -> bool:
    """
    Assign a category to a note
    
    Args:
        note_id: Note ID
        category_id: Category ID (None to remove category)
    
    Returns:
        True if successful
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE notes SET category_id = ? WHERE id = ?", (category_id, note_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def assign_category_to_task(task_id: int, category_id: Optional[int]) -> bool:
    """
    Assign a category to a task
    
    Args:
        task_id: Task ID
        category_id: Category ID (None to remove category)
    
    Returns:
        True if successful
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET category_id = ? WHERE id = ?", (category_id, task_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def get_notes_by_category(category_id: int) -> List[dict]:
    """Get all notes in a category"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, tags, created_at
        FROM notes
        WHERE category_id = ?
        ORDER BY created_at DESC
    """, (category_id,))
    
    notes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return notes


def get_tasks_by_category(category_id: int) -> List[dict]:
    """Get all tasks in a category"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, status, priority, due_date
        FROM tasks
        WHERE category_id = ?
        ORDER BY priority, due_date
    """, (category_id,))
    
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return tasks


def delete_category(category_id: int) -> bool:
    """
    Delete a category
    Note: This will set category_id to NULL for associated notes/tasks
    
    Args:
        category_id: Category ID
    
    Returns:
        True if successful
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Set category_id to NULL for notes and tasks
    cursor.execute("UPDATE notes SET category_id = NULL WHERE category_id = ?", (category_id,))
    cursor.execute("UPDATE tasks SET category_id = NULL WHERE category_id = ?", (category_id,))
    
    # Delete category
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success
