#!/usr/bin/env python3
"""
CLI Task Manager

Features:
- Add task: --title, --desc
- List tasks: --format table|json
- Delete task by ID
- Search tasks by query

Data persisted to ./tasks.json
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), 'tasks.json')


@dataclass
class Task:
    id: int
    title: str
    description: str


def _now_str() -> str:
    return datetime.now().strftime('%Y%m%d-%H%M%S')


def ensure_db(path: str = DB_PATH) -> Dict[str, Any]:
    """Ensure tasks DB exists; if missing create a new one.
    Returns the loaded DB dict with shape {"next_id": int, "tasks": list}.
    If file is invalid JSON, back it up and re-init.
    """
    if not os.path.exists(path):
        db = {"next_id": 1, "tasks": []}
        _write_json(path, db)
        return db

    # Try to read existing file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Basic shape validation
        if not isinstance(data, dict) or 'next_id' not in data or 'tasks' not in data:
            raise ValueError('Invalid DB shape')
        return data
    except Exception:
        # Backup and re-init
        try:
            backup_path = f"{path}.bak-{_now_str()}"
            if os.path.getsize(path) > 0:
                with open(path, 'rb') as src, open(backup_path, 'wb') as dst:
                    dst.write(src.read())
        except Exception:
            # Best effort; continue to re-init
            pass
        db = {"next_id": 1, "tasks": []}
        _write_json(path, db)
        return db


def load_db(path: str = DB_PATH) -> Dict[str, Any]:
    """Load the DB, ensuring it exists and is valid."""
    return ensure_db(path)


def save_db(db: Dict[str, Any], path: str = DB_PATH) -> None:
    _write_json(path, db)


def _write_json(path: str, data: Dict[str, Any]) -> None:
    tmp_path = f"{path}.tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp_path, path)


# Core operations

def add_task(title: str, description: str, path: str = DB_PATH) -> int:
    title = (title or '').strip()
    description = (description or '').strip()
    if not title:
        raise ValueError('Title is required and cannot be empty.')
    if not description:
        raise ValueError('Description is required and cannot be empty.')

    db = load_db(path)
    new_id = int(db.get('next_id', 1))
    task = Task(id=new_id, title=title, description=description)
    db['tasks'].append(asdict(task))
    db['next_id'] = new_id + 1
    save_db(db, path)
    return new_id


def list_tasks(path: str = DB_PATH) -> List[Dict[str, Any]]:
    db = load_db(path)
    tasks = db.get('tasks', [])
    if not isinstance(tasks, list):
        return []
    return tasks


def delete_task(task_id: int, path: str = DB_PATH) -> bool:
    """Delete a task by ID. Returns True if a task was deleted, False if not found."""
    db = load_db(path)
    tasks = db.get('tasks', [])
    if not isinstance(tasks, list):
        db['tasks'] = []
        save_db(db, path)
        return False

    original_len = len(tasks)
    tasks = [t for t in tasks if int(t.get('id', -1)) != int(task_id)]
    deleted = len(tasks) != original_len
    db['tasks'] = tasks
    save_db(db, path)
    return deleted


def search_tasks(query: str, path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Search tasks by matching query in title or description (case-insensitive).
    Returns a list of matching tasks."""
    db = load_db(path)
    tasks = db.get('tasks', [])
    if not isinstance(tasks, list):
        return []
    
    query_lower = query.lower()
    matches = []
    for t in tasks:
        title = str(t.get('title', '')).lower()
        desc = str(t.get('description', '')).lower()
        if query_lower in title or query_lower in desc:
            matches.append(t)
    return matches


# Output formatting

def print_table(tasks: List[Dict[str, Any]]) -> None:
    if not tasks:
        print('No tasks found.')
        return

    # Calculate column widths
    headers = ['ID', 'Title', 'Description']
    id_width = max(len(headers[0]), max((len(str(t.get('id', ''))) for t in tasks), default=0))
    title_width = max(len(headers[1]), max((len(str(t.get('title', ''))) for t in tasks), default=0))
    desc_width = max(len(headers[2]), max((len(str(t.get('description', ''))) for t in tasks), default=0))

    def row_sep():
        print('+' + '-' * (id_width + 2) + '+' + '-' * (title_width + 2) + '+' + '-' * (desc_width + 2) + '+')

    def print_row(vals):
        print(f"| {str(vals[0]).ljust(id_width)} | {str(vals[1]).ljust(title_width)} | {str(vals[2]).ljust(desc_width)} |")

    row_sep()
    print_row(headers)
    row_sep()
    for t in tasks:
        print_row([t.get('id', ''), t.get('title', ''), t.get('description', '')])
    row_sep()


# CLI layer

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Simple CLI Task Manager')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # add
    p_add = subparsers.add_parser('add', help='Add a new task')
    p_add.add_argument('--title', required=True, help='Title of the task')
    p_add.add_argument('--desc', required=True, help='Short description of the task')

    # list
    p_list = subparsers.add_parser('list', help='List tasks')
    p_list.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')

    # delete
    p_del = subparsers.add_parser('delete', help='Delete a task by ID')
    p_del.add_argument('id', type=int, help='ID of the task to delete')

    # search
    p_search = subparsers.add_parser('search', help='Search tasks by query')
    p_search.add_argument('query', help='Search term to match in title or description')
    p_search.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == 'add':
            task_id = add_task(args.title, args.desc)
            print(f'Task created: {task_id}')
            return 0
        elif args.command == 'list':
            tasks = list_tasks()
            if args.format == 'json':
                print(json.dumps(tasks, ensure_ascii=False, indent=2))
            else:
                print_table(tasks)
            return 0
        elif args.command == 'delete':
            deleted = delete_task(args.id)
            if deleted:
                print(f'Task deleted: {args.id}')
                return 0
            else:
                print(f'No task found with ID: {args.id}', file=sys.stderr)
                return 1
        elif args.command == 'search':
            tasks = search_tasks(args.query)
            if args.format == 'json':
                print(json.dumps(tasks, ensure_ascii=False, indent=2))
            else:
                print_table(tasks)
            return 0
        else:
            parser.print_help()
            return 2
    except ValueError as ve:
        print(f'Error: {ve}', file=sys.stderr)
        return 1
    except OSError as oe:
        print(f'I/O Error: {oe}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
