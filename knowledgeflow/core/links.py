"""
Note linking operations
"""

import sqlite3
from typing import List, Optional, Tuple
from core.database import get_connection
from core.models import NoteLink
from datetime import datetime


def create_link(source_id: int, target_id: int, link_type: str = 'reference') -> Optional[int]:
    """
    Create a link between two notes
    
    Args:
        source_id: Source note ID
        target_id: Target note ID
        link_type: Type of link ('reference', 'related', 'parent', 'child')
    
    Returns:
        Link ID if successful, None otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Validate notes exist
        cursor.execute("SELECT id FROM notes WHERE id IN (?, ?)", (source_id, target_id))
        if len(cursor.fetchall()) != 2:
            return None
        
        # Create link
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO note_links (source_note_id, target_note_id, link_type, created_at)
            VALUES (?, ?, ?, ?)
        """, (source_id, target_id, link_type, now))
        
        link_id = cursor.lastrowid
        conn.commit()
        return link_id
    
    except sqlite3.IntegrityError:
        # Link already exists
        return None
    finally:
        conn.close()


def delete_link(source_id: int, target_id: int) -> bool:
    """
    Delete a link between two notes
    
    Args:
        source_id: Source note ID
        target_id: Target note ID
    
    Returns:
        True if deleted, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM note_links
        WHERE source_note_id = ? AND target_note_id = ?
    """, (source_id, target_id))
    
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted


def get_forward_links(note_id: int) -> List[Tuple[int, str, str]]:
    """
    Get all notes this note links TO
    
    Args:
        note_id: Note ID
    
    Returns:
        List of (note_id, title, link_type) tuples
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.id, n.title, nl.link_type
        FROM note_links nl
        JOIN notes n ON nl.target_note_id = n.id
        WHERE nl.source_note_id = ?
        ORDER BY nl.created_at DESC
    """, (note_id,))
    
    links = cursor.fetchall()
    conn.close()
    
    return [(row['id'], row['title'], row['link_type']) for row in links]


def get_backlinks(note_id: int) -> List[Tuple[int, str, str]]:
    """
    Get all notes that link TO this note
    
    Args:
        note_id: Note ID
    
    Returns:
        List of (note_id, title, link_type) tuples
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.id, n.title, nl.link_type
        FROM note_links nl
        JOIN notes n ON nl.source_note_id = n.id
        WHERE nl.target_note_id = ?
        ORDER BY nl.created_at DESC
    """, (note_id,))
    
    links = cursor.fetchall()
    conn.close()
    
    return [(row['id'], row['title'], row['link_type']) for row in links]


def get_all_links(note_id: int) -> Tuple[List, List]:
    """
    Get both forward links and backlinks for a note
    
    Args:
        note_id: Note ID
    
    Returns:
        Tuple of (forward_links, backlinks)
    """
    return (get_forward_links(note_id), get_backlinks(note_id))


def detect_links_in_content(content: str) -> List[str]:
    """
    Detect [[Note Title]] style links in content
    
    Args:
        content: Note content
    
    Returns:
        List of note titles referenced
    """
    import re
    pattern = r'\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    return matches


def auto_create_links(note_id: int, content: str) -> int:
    """
    Automatically create links based on [[Title]] syntax in content
    
    Args:
        note_id: Source note ID
        content: Note content
    
    Returns:
        Number of links created
    """
    titles = detect_links_in_content(content)
    if not titles:
        return 0
    
    conn = get_connection()
    cursor = conn.cursor()
    
    links_created = 0
    for title in titles:
        # Find note with this title
        cursor.execute("SELECT id FROM notes WHERE title = ?", (title,))
        result = cursor.fetchone()
        
        if result:
            target_id = result['id']
            if create_link(note_id, target_id):
                links_created += 1
    
    conn.close()
    return links_created
