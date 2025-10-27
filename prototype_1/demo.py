#!/usr/bin/env python3
"""
Quick demo of Prototype 1 functionality
"""

from main import init_db, create_note, create_task, list_notes, list_tasks

print("🌊 KnowledgeFlow Prototype 1 - Quick Demo\n")

# Initialize
init_db()

# Create some sample notes
print("\n📝 Creating sample notes...")
create_note(
    "Python SQLite Tutorial",
    "SQLite is a lightweight database that's perfect for Python applications. No server needed!",
    ["python", "database", "tutorial"]
)

create_note(
    "Project Ideas",
    "1. Build a PKMS\n2. Add AI agents\n3. Create chat interface",
    ["project", "ideas"]
)

create_note(
    "Learning Goals",
    "Master Python, understand databases, build useful tools",
    ["goals", "learning"]
)

# Create some sample tasks
print("\n✅ Creating sample tasks...")
create_task("Finish prototype 1", priority="high", due_date="2025-10-28")
create_task("Design final architecture", priority="medium", due_date="2025-10-30")
create_task("Research AI integration", priority="high", due_date="2025-10-29")

# Display everything
print("\n" + "="*60)
list_notes()
print()
list_tasks()
print("\n" + "="*60)
print("\n💡 Now try running: python3 main.py")
print("   Then try commands like:")
print("   - search python")
print("   - view 1")
print("   - done 1")
print("   - note My New Note")
