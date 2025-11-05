"""
tasks3 - PKMS with pytest integration
"""

from .pkms import PKMS


def inc(n: int) -> int:
    return n + 1


def main() -> None:
    """Main entry point for tasks3"""
    print("🚀 tasks3 - Personal Knowledge & Task Management System")
    print("=" * 60)
    
    # Create PKMS instance
    pkms = PKMS()
    
    print("\n✅ Database initialized!")
    print(f"📁 Database location: {pkms.db_path}")
    
    # Show some usage examples
    print("\n📚 PKMS Module Usage Examples:")
    print("-" * 60)
    print("from tasks3 import PKMS")
    print("")
    print("pkms = PKMS()")
    print("note_id = pkms.create_note('My Note', 'Content here', ['tag1', 'tag2'])")
    print("task_id = pkms.create_task('My Task', priority='high', due_date='2025-11-24')")
    print("pkms.link_notes(note_id_1, note_id_2)")
    print("pkms.link_task_to_note(task_id, note_id)")
    print("")
    print("Run 'uv run pytest' to see all tests pass!")
    print("=" * 60)

