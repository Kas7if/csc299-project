"""
Task Manager CLI
Command-line interface for task management.
Logically separate from storage - uses the TaskStorage API.
"""

import argparse
import sys
from datetime import datetime
from .storage import TaskStorage


# Emoji mappings for visual clarity
STATUS_EMOJI = {
    "pending": "📝",
    "in-progress": "🔄",
    "completed": "✅"
}

PRIORITY_EMOJI = {
    "low": "🟢",
    "medium": "🟡",
    "high": "🔥"
}


def format_task(task: dict, detailed: bool = False) -> str:
    """
    Format a task for display.
    
    Args:
        task: Task dictionary
        detailed: Show detailed view
        
    Returns:
        Formatted string
    """
    status_emoji = STATUS_EMOJI.get(task["status"], "❓")
    priority_emoji = PRIORITY_EMOJI.get(task["priority"], "⚪")
    
    if detailed:
        lines = [
            f"{'=' * 60}",
            f"{status_emoji} Task: {task['title']}",
            f"ID: {task['id']}",
            f"Status: {task['status']} | Priority: {priority_emoji} {task['priority']}",
        ]
        
        if task["description"]:
            lines.append(f"Description: {task['description']}")
        
        if task["due_date"]:
            lines.append(f"Due: {task['due_date']}")
        
        if task["tags"]:
            lines.append(f"Tags: {', '.join(task['tags'])}")
        
        lines.append(f"Created: {task['created_at']}")
        lines.append(f"Updated: {task['updated_at']}")
        lines.append(f"{'=' * 60}")
        
        return "\n".join(lines)
    else:
        # Compact format for lists
        title = task['title'][:40] + "..." if len(task['title']) > 40 else task['title']
        return f"{status_emoji} {priority_emoji} [{task['id'][:8]}] {title}"


def cmd_add(args, storage: TaskStorage):
    """Add a new task."""
    tags = args.tags.split(",") if args.tags else []
    
    task = storage.create_task(
        title=args.title,
        description=args.description or "",
        priority=args.priority,
        due_date=args.due,
        tags=tags
    )
    
    print(f"✨ Task created successfully!")
    print(format_task(task, detailed=True))


def cmd_list(args, storage: TaskStorage):
    """List all tasks."""
    tasks = storage.list_tasks(status=args.status, priority=args.priority)
    
    if not tasks:
        print("📭 No tasks found.")
        return
    
    print(f"\n📋 Tasks ({len(tasks)} total):")
    print("-" * 60)
    for task in tasks:
        print(format_task(task))
    print("-" * 60)


def cmd_show(args, storage: TaskStorage):
    """Show detailed task information."""
    task = storage.get_task(args.task_id)
    
    if not task:
        print(f"❌ Task not found: {args.task_id}")
        sys.exit(1)
    
    print(format_task(task, detailed=True))


def cmd_update(args, storage: TaskStorage):
    """Update a task."""
    updates = {}
    
    if args.title:
        updates["title"] = args.title
    if args.description:
        updates["description"] = args.description
    if args.status:
        updates["status"] = args.status
    if args.priority:
        updates["priority"] = args.priority
    if args.due:
        updates["due_date"] = args.due
    
    task = storage.update_task(args.task_id, **updates)
    
    if not task:
        print(f"❌ Task not found: {args.task_id}")
        sys.exit(1)
    
    print("✅ Task updated successfully!")
    print(format_task(task, detailed=True))


def cmd_delete(args, storage: TaskStorage):
    """Delete a task."""
    if storage.delete_task(args.task_id):
        print(f"🗑️  Task deleted successfully: {args.task_id}")
    else:
        print(f"❌ Task not found: {args.task_id}")
        sys.exit(1)


def cmd_search(args, storage: TaskStorage):
    """Search for tasks."""
    tasks = storage.search_tasks(args.query)
    
    if not tasks:
        print(f"🔍 No tasks found matching '{args.query}'")
        return
    
    print(f"\n🔍 Search results for '{args.query}' ({len(tasks)} found):")
    print("-" * 60)
    for task in tasks:
        print(format_task(task))
    print("-" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="📝 Tasks Manager - Manage your tasks with style!",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description")
    add_parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], 
                           default="medium", help="Task priority")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    add_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-s", "--status", 
                            choices=["pending", "in-progress", "completed"],
                            help="Filter by status")
    list_parser.add_argument("-p", "--priority",
                            choices=["low", "medium", "high"],
                            help="Filter by priority")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_id", help="Task ID")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("-d", "--description", help="New description")
    update_parser.add_argument("-s", "--status",
                              choices=["pending", "in-progress", "completed"],
                              help="New status")
    update_parser.add_argument("-p", "--priority",
                              choices=["low", "medium", "high"],
                              help="New priority")
    update_parser.add_argument("--due", help="New due date (YYYY-MM-DD)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for tasks")
    search_parser.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Initialize storage (API layer)
    storage = TaskStorage()
    
    # Route to appropriate command
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "update": cmd_update,
        "delete": cmd_delete,
        "search": cmd_search
    }
    
    commands[args.command](args, storage)


if __name__ == "__main__":
    main()
