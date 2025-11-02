# Tasks2 - PKMS & Task Management System

**Iteration on tasks1 with enhanced features**

## Overview

This is an iteration and enhancement of the task manager from `tasks1`, now including:
- ✅ **Personal Knowledge Management** - Create and manage notes
- ✅ **Note Linking** - Build a knowledge graph by linking related notes  
- ✅ **Task Management** - Enhanced task management from tasks1
- ✅ **Task-Note Integration** - Attach tasks to relevant notes
- ✅ **SQLite Storage** - Persistent database instead of JSON
- ✅ **Search** - Full-text search across notes
- ✅ **Tagging** - Tag both notes and tasks for organization

## New Features from tasks1

1. **Notes System** - Store and manage knowledge in notes
2. **Note Links** - Connect related notes together
3. **Task-Note Attachments** - Link tasks to documentation
4. **Enhanced Database** - SQLite with proper relationships
5. **Better CLI** - More commands and features

## Running the Application

```bash
cd tasks2
python3 pkms.py
```

## Available Commands

### Notes
- `note <title>` - Create a new note
- `notes` - List all notes
- `search <query>` - Search notes by title or content
- `link <id1> <id2>` - Link two notes together
- `links <id>` - Show all links from a note

### Tasks  
- `task <title>` - Create a new task
- `tasks` - List all tasks
- `tasks pending` - List only pending tasks
- `done <id>` - Mark a task as complete
- `attach <task_id> <note_id>` - Link a task to a note

### General
- `help` - Show all commands
- `quit` - Exit the application

## Example Usage

```bash
# Create some notes
> note Python Basics
Content: Introduction to Python programming
Tags: python, programming

> note Web Development  
Content: Using Django and Flask
Tags: python, web

# Link related notes
> link 2 1

# Create a task
> task Learn Django
Priority: high
Due date: 2025-11-10

# Attach task to note
> attach 1 2

# Search
> search python

# View all tasks
> tasks
```

## Database Schema

The application uses SQLite with three main tables:

- **notes** - Stores notes with title, content, and tags
- **tasks** - Stores tasks with priority, due dates, and tags
- **note_links** - Stores connections between notes

## Experiments

The `experiment_*.py` files are for testing new features before integration:
- `experiment_rich_ui.py` - Test Rich library for UI
- `experiment_openai.py` - Test AI integration
- `experiment_parsers.py` - Test command parsing approaches
