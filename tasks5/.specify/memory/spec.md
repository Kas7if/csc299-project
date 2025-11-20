# Tasks Manager Specification

## Project Overview
This project should store and manage a list of tasks. It provides both an API and a CLI interface for task management operations.

## Core Requirements

### 1. Task Storage
- Store a list of tasks with their details (title, description, status, priority, due date, tags)
- Tasks should be stored locally in a file (JSON format for easy reading/editing)
- Persistent storage across application restarts
- Support for CRUD operations (Create, Read, Update, Delete)

### 2. API Component
- Provide a programmatic API for task operations
- API should be clean and well-documented
- Support all task management operations:
  - Create new tasks
  - List all tasks
  - Get specific task details
  - Update task information
  - Delete tasks
  - Search/filter tasks by various criteria

### 3. CLI Component
- Command-line interface to interact with tasks
- CLI should use the API (not directly access storage)
- **Logically separate from the task storage component**
- User-friendly commands for:
  - Adding new tasks
  - Listing all tasks
  - Viewing task details
  - Updating tasks
  - Deleting tasks
  - Filtering/searching tasks

### 4. Architecture Requirements
- **Separation of Concerns**: CLI component must be logically separate from the task storage component
- CLI → API → Storage (clear separation of layers)
- Each component should be independently testable
- Storage format should be easily readable and editable

### 5. Task Data Model
Each task should include:
- **ID**: Unique identifier
- **Title**: Short description of the task
- **Description**: Optional detailed description
- **Status**: (e.g., "pending", "in-progress", "completed")
- **Priority**: (e.g., "low", "medium", "high")
- **Due Date**: Optional deadline
- **Tags**: Optional list of tags for categorization
- **Created At**: Timestamp when task was created
- **Updated At**: Timestamp when task was last modified

## User Experience Requirements

### CLI Commands (Examples)
```bash
# Add a new task
tasks add "Complete CSC299 project" --priority high --due 2025-11-24

# List all tasks
tasks list

# List tasks with filtering
tasks list --status pending --priority high

# Show task details
tasks show <task-id>

# Update a task
tasks update <task-id> --status completed

# Delete a task
tasks delete <task-id>

# Search tasks
tasks search "project"
```

### Output Format
- Use emojis for visual clarity (✅, 📝, 🔥, etc.)
- Color-coded output for different priorities/statuses
- Table format for listing multiple tasks
- Human-readable date formats

## Technical Constraints

### Storage
- Use a simple, local file-based storage (JSON)
- Default location: `~/.tasks/tasks.json`
- File should be human-readable and easily editable
- Atomic writes to prevent data corruption

### Testing
- Unit tests for API functions
- Integration tests for CLI commands
- Test coverage for edge cases (empty lists, invalid IDs, etc.)
- Tests for file I/O operations

### Documentation
- README with installation and usage instructions
- API documentation for all public functions
- CLI help text for all commands
- Examples for common use cases

## Success Criteria
- Can create, read, update, and delete tasks via CLI
- Tasks persist across application restarts
- CLI is intuitive and easy to use
- Clear separation between CLI and storage layers
- All tests pass
- Code follows constitution principles

**Version**: 1.0.0 | **Created**: 2025-11-19
