# CLI Task Manager (Python) — Project Plan

## Overview
A minimal command-line task manager written in Python that lets you:
- Add a task (title + short description)
- List existing tasks

All tasks are persisted to `tasks.json` at the project root so data survives between runs.

## Goals
- Simple, dependency-free CLI using Python standard library
- Tasks have: `id` (int), `title` (str), `description` (str)
- Persistent storage to `./tasks.json`
- Clear, friendly UX for add and list commands

## Non-Goals (for v1)
- Edit/delete/complete tasks
- Sorting/filtering beyond basic list
- Concurrency/locking across multiple simultaneous processes
- Multi-user support

## CLI Design
- Entrypoint: `task_cli.py` (run with `python task_cli.py <command> [options]`)
- Subcommands:
  1) `add` — Create a new task
     - Flags:
       - `--title` (required) string
       - `--desc` (required) string (short description)
     - Behavior: assigns a unique incremental `id`, saves to `tasks.json`, prints the created task id
     - Example: `python task_cli.py add --title "Pay bills" --desc "Electricity and water"`
  2) `list` — List tasks
     - Flags:
       - `--format` optional: `table` (default) or `json`
     - Behavior: reads from `tasks.json`, prints all tasks
     - Example: `python task_cli.py list --format table`

- Help: `python task_cli.py -h`, `python task_cli.py add -h`, `python task_cli.py list -h`

## Data Model
Task (dict):
- `id: int` — unique identifier
- `title: str` — short, non-empty
- `description: str` — short, non-empty

## Storage Format (`tasks.json`)
Location: project root (`./tasks.json`)

JSON structure (keeps next id and the task list):
```
{
  "next_id": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Pay bills",
      "description": "Electricity and water"
    }
  ]
}
```
Notes:
- `next_id` starts at 1 if file is first created.
- We increment `next_id` after each successful add.
- If `tasks.json` is missing, create it on first run with `{ "next_id": 1, "tasks": [] }`.

## Validation & Error Handling
- Title and description are required; trim whitespace and reject empty values.
- If `tasks.json` is missing: create a new file.
- If `tasks.json` is empty or invalid JSON:
  - Create a backup `tasks.json.bak-YYYYMMDD-HHMMSS` (best effort) and initialize fresh data.
- Handle I/O errors with readable messages (permissions, read-only fs).

## User Experience
- On successful add: print `Task created: <id>` and no extra noise.
- On list (table): show headers and rows for id, title, description. Keep widths readable; do not truncate content for v1.
- On list (json): pretty-print JSON array of tasks.

## Implementation Outline
1) Project skeleton
   - Create `task_cli.py`
   - Auto-create `tasks.json` as needed
2) Storage helpers (module-level functions)
   - `load_db(path) -> dict`  // returns `{ "next_id": int, "tasks": list }`
   - `save_db(path, db: dict) -> None`
   - `ensure_db(path) -> dict` // creates file if missing, returns loaded db
3) Core operations
   - `add_task(title: str, description: str) -> int` // returns new id
   - `list_tasks() -> list[dict]`
4) CLI layer (argparse)
   - Subparsers for `add` and `list`
   - Input validation and invocation of core ops
   - Output formatting (table/json)
5) Output formatting
   - `print_table(tasks: list[dict])`
6) Minimal logging/messages for errors

## Project Structure
- `task_cli.py` — CLI entrypoint and implementation
- `tasks.json` — data file at project root (auto-created)
- `specs/PLAN.md` — this plan
- `README.md` — optional quickstart and usage

## Edge Cases
- Duplicate titles allowed (ids disambiguate)
- Very long title/description (print fully; no truncation v1)
- Special characters and unicode in text
- `tasks.json` corrupted or partially written (fallback behavior via backup + re-init)
- No tasks yet: `list` prints an empty table or `[]` for json

## Testing Strategy (lightweight)
- Unit-ish tests (optional for v1) by calling functions directly:
  - `ensure_db` initializes correctly when file missing
  - `add_task` increments ids and persists data
  - `list_tasks` returns all tasks
  - Invalid inputs rejected (empty title/desc)
- Manual smoke tests:
  - Add two tasks, list in table and json

## Acceptance Criteria
- Running `python task_cli.py add --title "T" --desc "D"` persists the task to `./tasks.json` with fields `id`, `title`, `description` and outputs `Task created: <id>`
- Running `python task_cli.py list` prints a table of all tasks
- `tasks.json` is created automatically if missing
- Invalid `tasks.json` is handled gracefully (backup + re-init)

## Future Enhancements (post-v1)
- Edit, delete, complete
- Filter/search/sort
- Colored output and nicer table layout
- Optional timestamps and status fields
- Packaging with an installable console script entry point (`tasks` command)

## Rough Estimate
- Implementation: ~60–120 minutes
- Polish and docs: ~20–40 minutes
