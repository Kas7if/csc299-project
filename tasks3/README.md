# tasks3 - PKMS with pytest Integration

**CSC299 Final Project - tasks3 Deliverable**  
Due: November 5, 2025

## Overview

This is the third iteration of the Personal Knowledge Management System (PKMS), now with comprehensive **pytest** test coverage. tasks3 demonstrates:

- ✅ Clean, testable Python package structure using `uv`
- ✅ 10 comprehensive pytest tests covering all core functionality
- ✅ SQLite database for persistent storage
- ✅ Notes, tasks, and linking capabilities
- ✅ Proper fixtures for test isolation

## Setup & Installation

### Prerequisites
- Python 3.10+
- uv package manager

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/Kas7if/csc299-project.git
cd csc299-project/tasks3

# Install dependencies (pytest is already configured)
uv sync
```

## Running the Application

```bash
# Run the main application
uv run tasks3
```

This will:
1. Initialize the SQLite database
2. Display usage examples
3. Show the database location

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_pkms.py

# Run specific test
uv run pytest tests/test_pkms.py::test_create_note
```

## Test Coverage

### Basic Tests (1)
- `test_inc.py` - Simple increment function test (requirement verification)

### PKMS Tests (9)
All tests use pytest fixtures for database isolation:

1. **test_create_note** - Verify note creation with title, content, and tags
2. **test_search_notes** - Test full-text search across note titles and content
3. **test_link_notes** - Verify bidirectional note linking (knowledge graph)
4. **test_duplicate_link_prevented** - Ensure link uniqueness constraints
5. **test_create_task** - Test task creation with priority, due date, and tags
6. **test_complete_task** - Verify task status transitions (pending → done)
7. **test_link_task_to_note** - Test task-note associations
8. **test_list_tasks_by_status** - Filter tasks by status (pending/done)
9. **test_list_all_notes** - List and count all notes

## Project Structure

```
tasks3/
├── src/
│   └── tasks3/
│       ├── __init__.py      # Main entry point, exports PKMS class
│       └── pkms.py          # Core PKMS functionality
├── tests/
│   ├── test_inc.py          # Basic test (requirement)
│   └── test_pkms.py         # Comprehensive PKMS tests
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── README.md                # This file
```

## Usage Examples

### As a Library

```python
from tasks3 import PKMS

# Create PKMS instance
pkms = PKMS()

# Create notes
note1 = pkms.create_note("Python Tutorial", "Learn Python basics", ["python", "tutorial"])
note2 = pkms.create_note("Advanced Topics", "Decorators and generators", ["python", "advanced"])

# Link notes together (knowledge graph)
pkms.link_notes(note1, note2)

# Search notes
results = pkms.search_notes("python")

# Create tasks
task = pkms.create_task(
    "Complete Python course",
    priority="high",
    due_date="2025-11-24",
    tags=["learning"]
)

# Link task to note
pkms.link_task_to_note(task, note1)

# Complete task
pkms.complete_task(task)

# List pending tasks
pending = pkms.list_tasks(status="pending")
```

## Key Features

### 1. Clean Architecture
- Separation of concerns: PKMS class handles all database operations
- Pytest fixtures ensure test isolation (each test gets fresh database)
- No global state or side effects

### 2. Comprehensive Testing
- **Unit tests** for individual functions (create, read, update)
- **Integration tests** for multi-step workflows (create → link → verify)
- **Edge case testing** (duplicate prevention, status filtering)

### 3. SQLite Database
- Lightweight, file-based storage
- Foreign key constraints for data integrity
- Full-text search capabilities

## Differences from tasks2

| Feature | tasks2 | tasks3 |
|---------|--------|--------|
| **Structure** | Single script | Proper package (src layout) |
| **Testing** | Manual testing | 10 automated pytest tests |
| **Package Manager** | pip/manual | uv with lock file |
| **Entry Point** | Direct script | `uv run tasks3` |
| **Interface** | Interactive CLI | Library + programmatic API |
| **Test Isolation** | Shared database | Temporary databases per test |

## Evolution from tasks1 → tasks2 → tasks3

### tasks1 (Oct 20)
- JSON-based task storage
- CLI with argparse
- Basic CRUD operations

### tasks2 (Nov 3)
- **Added**: SQLite database
- **Added**: Notes system with tagging
- **Added**: Note-to-note linking (knowledge graph)
- **Added**: Task-to-note associations
- **Added**: Interactive shell interface
- **Added**: Search functionality

### tasks3 (Nov 5) - **Current**
- **Added**: Pytest framework with 10 tests
- **Added**: Proper Python package structure
- **Added**: Test fixtures for isolation
- **Added**: uv package management
- **Added**: Programmatic API (library usage)
- **Improved**: Clean architecture for testability

## Assignment Requirements Met

✅ Installed `uv`  
✅ Ran `uv init tasks3 --vcs none --package`  
✅ Added pytest with `uv add --dev pytest`  
✅ Created `inc()` function in `__init__.py`  
✅ Created `tests/test_inc.py` with passing test  
✅ Verified with `uv run pytest` (1 passed)  
✅ Incorporated **9 additional tests** (>2 required) for PKMS  
✅ Main method callable via `uv run tasks3`  
✅ All tests pass (10/10)

## Running the Complete Test Suite

```bash
cd /Users/kashifyaboi/299\ final\ project/tasks3
uv run pytest -v
```

Expected output:
```
tests/test_inc.py::test_inc PASSED                           [ 10%]
tests/test_pkms.py::test_create_note PASSED                  [ 20%]
tests/test_pkms.py::test_search_notes PASSED                 [ 30%]
tests/test_pkms.py::test_link_notes PASSED                   [ 40%]
tests/test_pkms.py::test_duplicate_link_prevented PASSED     [ 50%]
tests/test_pkms.py::test_create_task PASSED                  [ 60%]
tests/test_pkms.py::test_complete_task PASSED                [ 70%]
tests/test_pkms.py::test_link_task_to_note PASSED            [ 80%]
tests/test_pkms.py::test_list_tasks_by_status PASSED         [ 90%]
tests/test_pkms.py::test_list_all_notes PASSED               [100%]

============ 10 passed in 0.09s ============
```

## License

MIT License - CSC299 Final Project

## Author

Kashif - DePaul University CSC299
