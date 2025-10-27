# Specification: Enhanced Data Model

**Version:** 1.0  
**Date:** October 27, 2025  
**Phase:** 1.2

## Overview
Enhance the basic data model from prototype_1 to support note linking, categories, and task-note associations for a richer knowledge management experience.

## Goals
1. Enable bidirectional links between notes (like Obsidian)
2. Organize notes and tasks with categories/folders
3. Associate tasks with related notes
4. Maintain backward compatibility with prototype_1 data

## Database Schema Changes

### New Table: `note_links`
Links between notes for building a knowledge graph.

```sql
CREATE TABLE note_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_note_id INTEGER NOT NULL,
    target_note_id INTEGER NOT NULL,
    link_type TEXT DEFAULT 'reference',  -- 'reference', 'related', 'parent', 'child'
    created_at TEXT NOT NULL,
    FOREIGN KEY (source_note_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_note_id) REFERENCES notes(id) ON DELETE CASCADE,
    UNIQUE(source_note_id, target_note_id)
);
```

### New Table: `categories`
Hierarchical categories for organizing notes and tasks.

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    type TEXT DEFAULT 'note',  -- 'note', 'task', 'both'
    created_at TEXT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
);
```

### Modified Table: `notes`
Add category support.

```sql
-- Add new column
ALTER TABLE notes ADD COLUMN category_id INTEGER REFERENCES categories(id);
```

### Modified Table: `tasks`
Add category and tags support, plus note association.

```sql
-- Add new columns
ALTER TABLE tasks ADD COLUMN category_id INTEGER REFERENCES categories(id);
ALTER TABLE tasks ADD COLUMN tags TEXT DEFAULT '[]';
ALTER TABLE tasks ADD COLUMN linked_note_id INTEGER REFERENCES notes(id);
```

## API Requirements

### Note Linking

#### `create_link(source_id, target_id, link_type='reference')`
- Create a bidirectional link between two notes
- Validate both notes exist
- Prevent duplicate links
- Return link ID

#### `get_backlinks(note_id)`
- Get all notes that link TO this note
- Return list of (note_id, title, link_type)

#### `get_forward_links(note_id)`
- Get all notes this note links TO
- Return list of (note_id, title, link_type)

#### `delete_link(source_id, target_id)`
- Remove link between notes
- Cascade deletion if note is deleted

### Categories

#### `create_category(name, parent_id=None, type='note')`
- Create a new category
- Support hierarchical structure
- Return category ID

#### `get_categories(type=None)`
- List all categories, optionally filtered by type
- Return tree structure

#### `assign_category(item_id, category_id, item_type='note')`
- Assign a category to a note or task
- Validate category exists and matches type

### Task-Note Association

#### `link_task_to_note(task_id, note_id)`
- Associate a task with a note
- One task can link to one note (1:1 relationship)
- Update task's `linked_note_id`

#### `get_task_notes(task_id)`
- Get the note linked to a task (if any)
- Return note details

#### `get_note_tasks(note_id)`
- Get all tasks linked to a note
- Return list of tasks

## Features to Implement

### 1. Automatic Link Detection
- Parse note content for `[[Note Title]]` syntax
- Automatically create links when notes reference each other
- Update links when note titles change

### 2. Category Browser
- Show hierarchical category tree
- Filter notes/tasks by category
- Move items between categories

### 3. Knowledge Graph View
- Show connected notes
- Calculate note importance (by number of links)
- Find orphaned notes (no links)

## Testing Requirements

### Unit Tests
- [ ] Test link creation and deletion
- [ ] Test bidirectional link integrity
- [ ] Test category hierarchy
- [ ] Test task-note associations
- [ ] Test duplicate link prevention
- [ ] Test cascade deletion

### Integration Tests
- [ ] Test link detection in note content
- [ ] Test category filtering
- [ ] Test graph traversal

## Migration Plan

1. Add new tables (`note_links`, `categories`)
2. Alter existing tables (`notes`, `tasks`)
3. Migrate existing data (no data loss)
4. Test backward compatibility

## Success Criteria
- ✅ Can create and query links between notes
- ✅ Can organize notes/tasks with categories
- ✅ Can associate tasks with notes
- ✅ All tests pass
- ✅ Prototype_1 data remains accessible

## Implementation Order
1. Database schema updates
2. Core linking functions
3. Category management
4. Task-note associations
5. Automatic link detection
6. Tests

---
**Next Spec:** `02-cli-interface.md` - Enhanced CLI with Rich library
