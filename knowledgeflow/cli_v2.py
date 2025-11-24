#!/usr/bin/env python3
"""
KnowledgeFlow CLI v2 - JSON-based Personal Knowledge Management System
Enhanced with AI agents and rich terminal UI
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from rich.markdown import Markdown

from core.json_storage import JSONStorage
from agents.summarizer import SummarizerAgent


class KnowledgeFlowCLI:
    """CLI interface for KnowledgeFlow"""
    
    def __init__(self):
        self.console = Console()
        self.storage = JSONStorage()
        
        # Initialize AI agent if API key is available
        self.summarizer = None
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.summarizer = SummarizerAgent()
                self.console.print("[green]✓[/green] AI Summarizer initialized")
            except Exception as e:
                self.console.print(f"[yellow]⚠[/yellow] AI Summarizer unavailable: {e}")
        else:
            self.console.print("[yellow]⚠[/yellow] Set OPENAI_API_KEY to enable AI features")
    
    def show_banner(self):
        """Display welcome banner"""
        banner = """
╔═══════════════════════════════════════════╗
║     📚 KnowledgeFlow v2 - JSON Edition    ║
║   Personal Knowledge & Task Management    ║
╚═══════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="cyan"))
    
    def show_menu(self):
        """Display main menu"""
        self.console.print("\n[bold cyan]Main Menu[/bold cyan]")
        menu = """
[bold]Notes:[/bold]
  1. Create note
  2. List notes
  3. Search notes
  4. View note

[bold]Tasks:[/bold]
  5. Create task
  6. List tasks
  7. Search tasks
  8. Update task status

[bold]AI Features:[/bold]
  9. Summarize note/task
  10. Generate title from content

[bold]Other:[/bold]
  0. Exit
        """
        self.console.print(menu)
    
    # ===== NOTE OPERATIONS =====
    
    def create_note(self):
        """Create a new note"""
        self.console.print("\n[bold cyan]Create New Note[/bold cyan]")
        
        title = Prompt.ask("Title")
        content = Prompt.ask("Content (optional)", default="")
        tags_input = Prompt.ask("Tags (comma-separated, optional)", default="")
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        
        note = self.storage.create_note(title=title, content=content, tags=tags)
        
        self.console.print(f"\n[green]✓[/green] Note created with ID: {note['id']}")
        
        # Offer AI summary
        if self.summarizer and content:
            if Confirm.ask("Generate AI summary?", default=False):
                summary = self.summarizer.summarize_note(note)
                self.console.print(f"\n[cyan]AI Summary:[/cyan] {summary}")
    
    def list_notes(self):
        """List all notes"""
        tag_filter = Prompt.ask("Filter by tag (optional)", default="")
        
        notes = self.storage.list_notes(tag=tag_filter if tag_filter else None)
        
        if not notes:
            self.console.print("[yellow]No notes found[/yellow]")
            return
        
        table = Table(title=f"Notes ({len(notes)} total)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Tags", style="green")
        table.add_column("Created", style="yellow")
        
        for note in notes:
            table.add_row(
                note['id'][:8] + "...",
                note['title'][:40],
                ", ".join(note.get('tags', [])),
                note['created_at'][:10]
            )
        
        self.console.print(table)
    
    def search_notes(self):
        """Search notes"""
        query = Prompt.ask("Search query")
        
        results = self.storage.search_notes(query)
        
        if not results:
            self.console.print("[yellow]No matches found[/yellow]")
            return
        
        self.console.print(f"\n[green]Found {len(results)} note(s)[/green]\n")
        
        for note in results:
            panel = Panel(
                f"[bold]{note['title']}[/bold]\n\n{note.get('content', '')[:200]}...",
                title=f"ID: {note['id'][:8]}",
                subtitle=f"Tags: {', '.join(note.get('tags', []))}",
                border_style="cyan"
            )
            self.console.print(panel)
    
    def view_note(self):
        """View a specific note"""
        note_id = Prompt.ask("Note ID (full or first 8 chars)")
        
        # Try to find by partial ID
        notes = self.storage.list_notes()
        note = None
        for n in notes:
            if n['id'].startswith(note_id):
                note = n
                break
        
        if not note:
            self.console.print("[red]Note not found[/red]")
            return
        
        # Display note
        md_content = f"""# {note['title']}

**ID:** {note['id']}
**Created:** {note['created_at']}
**Updated:** {note['updated_at']}
**Tags:** {', '.join(note.get('tags', []))}

---

{note.get('content', '')}
"""
        md = Markdown(md_content)
        self.console.print(Panel(md, border_style="cyan"))
    
    # ===== TASK OPERATIONS =====
    
    def create_task(self):
        """Create a new task"""
        self.console.print("\n[bold cyan]Create New Task[/bold cyan]")
        
        title = Prompt.ask("Title")
        description = Prompt.ask("Description (optional)", default="")
        priority = Prompt.ask("Priority", choices=["low", "medium", "high"], default="medium")
        tags_input = Prompt.ask("Tags (comma-separated, optional)", default="")
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        
        task = self.storage.create_task(
            title=title,
            description=description,
            priority=priority,
            tags=tags
        )
        
        self.console.print(f"\n[green]✓[/green] Task created with ID: {task['id']}")
        
        # Offer AI summary
        if self.summarizer and description:
            if Confirm.ask("Generate AI summary?", default=False):
                summary = self.summarizer.summarize_task(task)
                self.console.print(f"\n[cyan]AI Summary:[/cyan] {summary}")
    
    def list_tasks(self):
        """List all tasks"""
        status_filter = Prompt.ask(
            "Filter by status (optional)",
            choices=["", "pending", "in_progress", "completed"],
            default=""
        )
        
        tasks = self.storage.list_tasks(
            status=status_filter if status_filter else None
        )
        
        if not tasks:
            self.console.print("[yellow]No tasks found[/yellow]")
            return
        
        table = Table(title=f"Tasks ({len(tasks)} total)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Created", style="green")
        
        for task in tasks:
            status_emoji = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅"
            }.get(task['status'], "❓")
            
            priority_color = {
                "low": "green",
                "medium": "yellow",
                "high": "red"
            }.get(task['priority'], "white")
            
            table.add_row(
                task['id'][:8] + "...",
                task['title'][:40],
                f"{status_emoji} {task['status']}",
                f"[{priority_color}]{task['priority']}[/{priority_color}]",
                task['created_at'][:10]
            )
        
        self.console.print(table)
    
    def search_tasks(self):
        """Search tasks"""
        query = Prompt.ask("Search query")
        
        results = self.storage.search_tasks(query)
        
        if not results:
            self.console.print("[yellow]No matches found[/yellow]")
            return
        
        self.console.print(f"\n[green]Found {len(results)} task(s)[/green]\n")
        
        for task in results:
            status_emoji = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅"
            }.get(task['status'], "❓")
            
            panel = Panel(
                f"[bold]{task['title']}[/bold]\n\n{task.get('description', '')[:200]}...",
                title=f"{status_emoji} {task['id'][:8]} | Priority: {task['priority']}",
                border_style="yellow"
            )
            self.console.print(panel)
    
    def update_task_status(self):
        """Update task status"""
        task_id = Prompt.ask("Task ID (full or first 8 chars)")
        
        # Find task
        tasks = self.storage.list_tasks()
        task = None
        for t in tasks:
            if t['id'].startswith(task_id):
                task = t
                break
        
        if not task:
            self.console.print("[red]Task not found[/red]")
            return
        
        new_status = Prompt.ask(
            "New status",
            choices=["pending", "in_progress", "completed"],
            default=task['status']
        )
        
        updated = self.storage.update_task(task['id'], status=new_status)
        self.console.print(f"[green]✓[/green] Task status updated to: {new_status}")
    
    # ===== AI OPERATIONS =====
    
    def summarize_item(self):
        """Summarize a note or task"""
        if not self.summarizer:
            self.console.print("[red]AI features not available. Set OPENAI_API_KEY.[/red]")
            return
        
        item_type = Prompt.ask("Item type", choices=["note", "task"])
        item_id = Prompt.ask(f"{item_type.title()} ID (full or first 8 chars)")
        
        # Find item
        if item_type == "note":
            items = self.storage.list_notes()
        else:
            items = self.storage.list_tasks()
        
        item = None
        for i in items:
            if i['id'].startswith(item_id):
                item = i
                break
        
        if not item:
            self.console.print(f"[red]{item_type.title()} not found[/red]")
            return
        
        with self.console.status("[cyan]Generating summary..."):
            if item_type == "note":
                summary = self.summarizer.summarize_note(item)
            else:
                summary = self.summarizer.summarize_task(item)
        
        self.console.print(f"\n[bold cyan]AI Summary:[/bold cyan]\n{summary}")
    
    def generate_title(self):
        """Generate a title from content"""
        if not self.summarizer:
            self.console.print("[red]AI features not available. Set OPENAI_API_KEY.[/red]")
            return
        
        content = Prompt.ask("Enter content")
        
        with self.console.status("[cyan]Generating title..."):
            title = self.summarizer.generate_title(content)
        
        self.console.print(f"\n[bold cyan]Suggested Title:[/bold cyan]\n{title}")
    
    # ===== MAIN LOOP =====
    
    def run(self):
        """Main CLI loop"""
        self.show_banner()
        
        while True:
            self.show_menu()
            choice = Prompt.ask("\nChoice", default="0")
            
            try:
                if choice == "1":
                    self.create_note()
                elif choice == "2":
                    self.list_notes()
                elif choice == "3":
                    self.search_notes()
                elif choice == "4":
                    self.view_note()
                elif choice == "5":
                    self.create_task()
                elif choice == "6":
                    self.list_tasks()
                elif choice == "7":
                    self.search_tasks()
                elif choice == "8":
                    self.update_task_status()
                elif choice == "9":
                    self.summarize_item()
                elif choice == "10":
                    self.generate_title()
                elif choice == "0":
                    self.console.print("\n[cyan]Goodbye! 👋[/cyan]")
                    break
                else:
                    self.console.print("[red]Invalid choice[/red]")
            
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Operation cancelled[/yellow]")
                continue
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    cli = KnowledgeFlowCLI()
    cli.run()
