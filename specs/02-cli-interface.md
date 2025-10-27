# Specification: Enhanced CLI Interface

**Version:** 1.0  
**Date:** October 27, 2025  
**Phase:** 1.3

## Overview
Upgrade the basic CLI to use the Rich library for beautiful, colorful terminal output with better command parsing and user experience.

## Goals
1. Beautiful terminal UI with colors and formatting
2. Better command parsing (support flags and options)
3. Command history and auto-completion hints
4. Improved error messages
5. Progress indicators for long operations

## Dependencies
```
rich>=13.7.0
```

## Features to Implement

### 1. Rich Console Output

**Before:**
```
📝 Your Notes:
------------------------------------------------------------
  #1 - Python Tutorial [python, database]
      Created: 2025-10-27
------------------------------------------------------------
```

**After (with Rich):**
```
╭─────────────────────── Your Notes ───────────────────────╮
│ ID │ Title            │ Tags              │ Created      │
├────┼──────────────────┼───────────────────┼──────────────┤
│ 1  │ Python Tutorial  │ python, database  │ Oct 27, 2025 │
│ 2  │ Project Ideas    │ ideas, project    │ Oct 27, 2025 │
╰──────────────────────────────────────────────────────────╯
```

### 2. Command Structure

Support both simple and advanced syntax:

```bash
# Simple commands (keep backward compatible)
note My Note Title
task Buy groceries
search python

# Advanced commands with flags
note --title "My Note" --tags python,tutorial --category coding
task --title "Buy groceries" --priority high --due 2025-10-30
search --query python --tags tutorial --after 2025-10-01
```

### 3. Interactive Prompts

Use Rich's `Prompt` for better input:

```python
from rich.prompt import Prompt, Confirm

title = Prompt.ask("Note title")
add_tags = Confirm.ask("Add tags?")
if add_tags:
    tags = Prompt.ask("Tags (comma-separated)")
```

### 4. Status Indicators

Show progress for operations:

```python
from rich.progress import track

for item in track(items, description="Processing..."):
    # Do work
```

### 5. Syntax Highlighting

Color code different elements:
- **Commands** - bold cyan
- **Arguments** - green
- **Errors** - bold red
- **Success** - bold green
- **Info** - blue

### 6. Help System

Rich formatted help:

```python
from rich.table import Table
from rich.panel import Panel

# Show available commands in a table
# Show examples in panels
# Syntax highlighting for command examples
```

## API Requirements

### Console Manager (`ui/console.py`)

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class ConsoleManager:
    def __init__(self):
        self.console = Console()
    
    def print_notes(self, notes):
        """Display notes in a formatted table"""
        
    def print_tasks(self, tasks):
        """Display tasks with status icons"""
        
    def print_error(self, message):
        """Display error message"""
        
    def print_success(self, message):
        """Display success message"""
        
    def show_help(self):
        """Display help information"""
```

### Command Parser (`ui/parser.py`)

```python
import argparse

class CommandParser:
    def parse(self, user_input):
        """Parse user input into command and arguments"""
        # Support both:
        # - Simple: "note My Title"
        # - Advanced: "note --title 'My Title' --tags python"
        
    def get_command(self):
        """Get the main command"""
        
    def get_args(self):
        """Get command arguments"""
```

### Enhanced Chat Interface (`ui/chat.py`)

```python
from rich.console import Console
from rich.prompt import Prompt
from ui.console import ConsoleManager
from ui.parser import CommandParser

class ChatInterface:
    def __init__(self):
        self.console_manager = ConsoleManager()
        self.parser = CommandParser()
        
    def run(self):
        """Main chat loop with Rich UI"""
        
    def handle_command(self, command, args):
        """Execute parsed commands"""
```

## Implementation Details

### File Structure
```
knowledgeflow/
├── ui/
│   ├── __init__.py
│   ├── console.py      # Rich console management
│   ├── parser.py       # Command parsing
│   └── chat.py         # Enhanced chat interface
└── main.py             # Entry point (updated)
```

### Color Scheme
- **Primary:** Cyan (#00FFFF)
- **Success:** Green (#00FF00)
- **Warning:** Yellow (#FFFF00)
- **Error:** Red (#FF0000)
- **Info:** Blue (#0000FF)
- **Muted:** Gray (#808080)

### Command Examples

```bash
# Notes
note Create a new note
note --title "My Note" --tags python,ai --category learning
notes
notes --tags python
notes --category learning --after 2025-10-01
view 1
edit 1
delete 1

# Tasks
task Complete homework
task --title "Complete homework" --priority high --due 2025-10-30
tasks
tasks --status pending --priority high
tasks --overdue
done 1

# Search
search python
search --query "machine learning" --type note
search --tags ai,python

# Links (Phase 1.2 feature)
link 1 2
links 1
graph

# Categories (Phase 1.2 feature)
category add Learning
categories
move note 1 Learning

# General
help
help note
clear
quit
```

## Testing Requirements

### Unit Tests
- [ ] Test command parsing (simple and advanced)
- [ ] Test table formatting
- [ ] Test color output
- [ ] Test error handling
- [ ] Test help display

### Integration Tests
- [ ] Test full command flow
- [ ] Test backward compatibility
- [ ] Test edge cases (empty input, invalid commands)

## User Experience Improvements

1. **Command suggestions** - "Did you mean 'notes'?" for typos
2. **Tab completion** - Auto-complete commands
3. **Command history** - Up/down arrows for history
4. **Confirmation prompts** - Confirm before deleting
5. **Loading indicators** - Show progress for slow operations

## Backward Compatibility

- Keep simple command syntax working
- Existing database remains compatible
- Old scripts using simple commands still work

## Success Criteria
- ✅ All commands have Rich formatting
- ✅ Tables display properly
- ✅ Colors enhance readability
- ✅ Command parsing handles both simple and advanced syntax
- ✅ All tests pass
- ✅ Help system is comprehensive

## Implementation Order
1. Install Rich and create console manager
2. Create command parser
3. Migrate existing commands to use Rich
4. Add advanced command syntax
5. Enhance help system
6. Add interactive prompts
7. Tests

---
**Previous Spec:** `01-data-model.md`  
**Next Spec:** `03-ai-setup.md`
