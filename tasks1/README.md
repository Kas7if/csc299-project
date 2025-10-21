# CLI Task Manager (Python)

A tiny, dependency-free task manager for the command line.

- Add tasks with a title and short description
- List tasks in a table or JSON
- Delete tasks by ID
- Search tasks by query (title or description)
- Data saved to `tasks.json` at the project root

## Requirements
- Python 3.8+

## Usage

Add a task:

```bash
python task_cli.py add --title "Pay bills" --desc "Electricity and water"
```

List tasks (table):

```bash
python task_cli.py list
```

List tasks (json):

```bash
python task_cli.py list --format json
```

Delete a task by ID:

```bash
python task_cli.py delete 1
```

Search tasks (case-insensitive, matches title or description):

```bash
python task_cli.py search "bills"
```

Search tasks (json output):

```bash
python task_cli.py search "bills" --format json
```

`tasks.json` is created automatically on first run. If the file is corrupt, the tool will back it up (best effort) to `tasks.json.bak-YYYYMMDD-HHMMSS` and reinitialize.

## Notes
- IDs are incremental and start from 1.
- Duplicate titles are allowed.
- This is a minimal v1; see `specs/PLAN.md` for roadmap.
