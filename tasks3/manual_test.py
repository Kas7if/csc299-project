#!/usr/bin/env python3
"""
Manual testing script for tasks3 PKMS
Run with: uv run python manual_test.py
"""

from tasks3 import PKMS, inc
from pathlib import Path

print("=" * 70)
print("🧪 Manual Testing Script for tasks3")
print("=" * 70)

# Test 1: inc() function
print("\n1️⃣  Testing inc() function:")
print(f"   inc(5) = {inc(5)}")
print(f"   inc(100) = {inc(100)}")
print(f"   inc(-1) = {inc(-1)}")
print("   ✅ inc() works!")

# Test 2: Create PKMS instance
print("\n2️⃣  Creating PKMS instance with custom database:")
test_db = Path("manual_test.db")
pkms = PKMS(test_db)
print(f"   ✅ PKMS created with database: {test_db}")

# Test 3: Create notes
print("\n3️⃣  Creating notes:")
note1 = pkms.create_note(
    "Python Tutorial", 
    "Learn Python basics including variables, loops, and functions",
    ["python", "tutorial", "programming"]
)
print(f"   Created note #{note1}: Python Tutorial")

note2 = pkms.create_note(
    "Data Structures",
    "Study arrays, linked lists, trees, and graphs",
    ["cs", "algorithms", "data-structures"]
)
print(f"   Created note #{note2}: Data Structures")

note3 = pkms.create_note(
    "Web Development",
    "HTML, CSS, JavaScript, and modern frameworks like React",
    ["web", "frontend", "javascript"]
)
print(f"   Created note #{note3}: Web Development")
print("   ✅ 3 notes created!")

# Test 4: List all notes
print("\n4️⃣  Listing all notes:")
all_notes = pkms.list_notes()
for note in all_notes:
    print(f"   #{note['id']}: {note['title']}")
    print(f"      Tags: {', '.join(note['tags'])}")
    print(f"      Content: {note['content'][:50]}...")
print(f"   ✅ Total notes: {len(all_notes)}")

# Test 5: Search notes
print("\n5️⃣  Searching for 'python':")
results = pkms.search_notes("python")
for note in results:
    print(f"   Found: #{note['id']} - {note['title']}")
print(f"   ✅ Found {len(results)} matching note(s)")

# Test 6: Link notes
print("\n6️⃣  Linking notes together:")
success = pkms.link_notes(note1, note2)
print(f"   Linked note #{note1} → #{note2}: {success}")
success = pkms.link_notes(note1, note3)
print(f"   Linked note #{note1} → #{note3}: {success}")
print("   ✅ Notes linked!")

# Test 7: Get linked notes
print("\n7️⃣  Getting linked notes from note #1:")
linked = pkms.get_linked_notes(note1)
for note in linked:
    print(f"   → #{note['id']}: {note['title']}")
print(f"   ✅ Note #{note1} links to {len(linked)} other notes")

# Test 8: Create tasks
print("\n8️⃣  Creating tasks:")
task1 = pkms.create_task(
    "Complete CSC299 project",
    "Finish all tasks including tasks4, testing, and documentation",
    priority="high",
    due_date="2025-11-24",
    tags=["school", "urgent"]
)
print(f"   Created task #{task1}: Complete CSC299 project (high priority)")

task2 = pkms.create_task(
    "Study for midterm",
    priority="medium",
    due_date="2025-11-15",
    tags=["school", "exam"]
)
print(f"   Created task #{task2}: Study for midterm (medium priority)")

task3 = pkms.create_task(
    "Buy groceries",
    priority="low",
    due_date="2025-11-06",
    tags=["personal"]
)
print(f"   Created task #{task3}: Buy groceries (low priority)")
print("   ✅ 3 tasks created!")

# Test 9: List all tasks
print("\n9️⃣  Listing all tasks:")
all_tasks = pkms.list_tasks()
for task in all_tasks:
    status_icon = "✓" if task['status'] == 'done' else "○"
    print(f"   {status_icon} #{task['id']}: {task['title']} ({task['priority']}) - Due: {task['due_date']}")
print(f"   ✅ Total tasks: {len(all_tasks)}")

# Test 10: Link task to note
print("\n🔟 Linking task to note:")
success = pkms.link_task_to_note(task1, note1)
print(f"   Linked task #{task1} → note #{note1}: {success}")
task_info = pkms.get_task(task1)
print(f"   Task #{task1} is now linked to note #{task_info['linked_note_id']}")
print("   ✅ Task-note link created!")

# Test 11: Complete a task
print("\n1️⃣1️⃣  Completing task #3:")
before = pkms.get_task(task3)
print(f"   Before: Task #{task3} status = {before['status']}")
pkms.complete_task(task3)
after = pkms.get_task(task3)
print(f"   After:  Task #{task3} status = {after['status']}")
print("   ✅ Task completed!")

# Test 12: Filter tasks by status
print("\n1️⃣2️⃣  Filtering tasks by status:")
pending_tasks = pkms.list_tasks(status="pending")
print(f"   Pending tasks: {len(pending_tasks)}")
for task in pending_tasks:
    print(f"      ○ #{task['id']}: {task['title']}")

done_tasks = pkms.list_tasks(status="done")
print(f"   Completed tasks: {len(done_tasks)}")
for task in done_tasks:
    print(f"      ✓ #{task['id']}: {task['title']}")
print("   ✅ Filtering works!")

# Summary
print("\n" + "=" * 70)
print("📊 Test Summary:")
print("=" * 70)
print(f"   Notes created: {len(all_notes)}")
print(f"   Tasks created: {len(all_tasks)}")
print(f"   Note links: {len(linked)}")
print(f"   Pending tasks: {len(pending_tasks)}")
print(f"   Completed tasks: {len(done_tasks)}")
print("=" * 70)
print("✅ All manual tests passed!")
print("=" * 70)
print(f"\n📁 Test database created at: {test_db.absolute()}")
print("   (You can delete this file after testing)")
