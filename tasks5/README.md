# 📝 Tasks Manager

A simple, elegant task management system built using spec-driven development principles.

## Features

- ✅ **Create, Read, Update, Delete** tasks
- 📋 **List and filter** tasks by status and priority
- 🔍 **Search** tasks by keywords
- 💾 **Local storage** in JSON format
- 🎨 **Beautiful CLI** with emojis and colors
- 🏗️ **Clean architecture** with separated layers (CLI → API → Storage)

## Installation

```bash
# Run the CLI directly
python -m src.tasks_manager.cli <command>
```

## Usage

### Add a new task
```bash
python -m src.tasks_manager.cli add "Complete CSC299 project" --priority high --due 2025-11-24 -t "school,urgent"
```

### List all tasks
```bash
python -m src.tasks_manager.cli list
```

### List with filters
```bash
python -m src.tasks_manager.cli list --status pending --priority high
```

### Show task details
```bash
python -m src.tasks_manager.cli show <task-id>
```

### Update a task
```bash
python -m src.tasks_manager.cli update <task-id> --status completed
```

### Delete a task
```bash
python -m src.tasks_manager.cli delete <task-id>
```

### Search tasks
```bash
python -m src.tasks_manager.cli search "project"
```

## Architecture

The project follows a clean, layered architecture:

- **Storage Layer** (`storage.py`): Handles persistent storage in JSON
- **API Layer**: Public functions in `TaskStorage` class
- **CLI Layer** (`cli.py`): Command-line interface that uses the API

This separation ensures:
- Each component is independently testable
- CLI doesn't directly access storage
- Clear boundaries between concerns

## Testing

Run the tests:
```bash
python tests/test_storage.py
```

## Storage Format

Tasks are stored in `~/.tasks/tasks.json` in human-readable JSON format:

```json
[
  {
    "id": "uuid-here",
    "title": "Complete project",
    "description": "Finish all remaining tasks",
    "status": "pending",
    "priority": "high",
    "due_date": "2025-11-24",
    "tags": ["school", "urgent"],
    "created_at": "2025-11-19T...",
    "updated_at": "2025-11-19T..."
  }
]
```

## Constitution

This project follows strict development principles defined in `.specify/memory/constitution.md`:
- Code quality standards
- Testing requirements (NON-NEGOTIABLE)
- User experience consistency
- Documentation requirements
- Performance standards

## License

MIT
