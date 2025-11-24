#!/usr/bin/env python3
"""
Demo: KnowledgeFlow v2 with JSON Storage and AI
Shows the new features in action
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from core.json_storage import JSONStorage
from agents.summarizer import SummarizerAgent
import os

# Load environment variables from .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]KnowledgeFlow v2 Demo[/bold cyan]\n"
        "JSON Storage + AI Agents + Rich UI",
        border_style="cyan"
    ))
    
    # Initialize storage
    console.print("\n[yellow]1. Initializing JSON storage...[/yellow]")
    storage = JSONStorage()
    console.print("[green]✓ Storage ready[/green]")
    
    # Create some notes
    console.print("\n[yellow]2. Creating sample notes...[/yellow]")
    note1 = storage.create_note(
        title="Python Best Practices",
        content="Use type hints, write docstrings, follow PEP 8, use virtual environments, write tests.",
        tags=["python", "programming"]
    )
    note2 = storage.create_note(
        title="Project Architecture",
        content="Separate concerns, use layers (UI, business logic, data), keep dependencies minimal.",
        tags=["architecture", "design"]
    )
    console.print(f"[green]✓ Created {len(storage.list_notes())} notes[/green]")
    
    # Create some tasks
    console.print("\n[yellow]3. Creating sample tasks...[/yellow]")
    task1 = storage.create_task(
        title="Write unit tests",
        description="Add pytest tests for all core modules including storage and agents",
        status="completed",
        priority="high",
        tags=["testing"]
    )
    task2 = storage.create_task(
        title="Document API",
        description="Create comprehensive documentation for all public APIs and CLI usage",
        status="pending",
        priority="medium",
        tags=["documentation"]
    )
    console.print(f"[green]✓ Created {len(storage.list_tasks())} tasks[/green]")
    
    # Create links
    console.print("\n[yellow]4. Creating links between items...[/yellow]")
    link = storage.create_link(note1['id'], task1['id'], link_type="supports")
    console.print(f"[green]✓ Linked note to task[/green]")
    
    # Search functionality
    console.print("\n[yellow]5. Testing search...[/yellow]")
    results = storage.search_all("python")
    console.print(f"[green]✓ Found {len(results['notes'])} notes and {len(results['tasks'])} tasks[/green]")
    
    # AI Summarization
    if os.getenv("OPENAI_API_KEY"):
        console.print("\n[yellow]6. Testing AI summarization...[/yellow]")
        try:
            summarizer = SummarizerAgent()
            
            summary1 = summarizer.summarize_note(note1, max_words=20)
            console.print(f"\n[cyan]Note Summary:[/cyan] {summary1}")
            
            summary2 = summarizer.summarize_task(task1, max_words=20)
            console.print(f"[cyan]Task Summary:[/cyan] {summary2}")
            
            title = summarizer.generate_title(note2['content'], max_words=5)
            console.print(f"[cyan]Generated Title:[/cyan] {title}")
            
            console.print("\n[green]✓ AI features working![/green]")
        except Exception as e:
            console.print(f"[red]✗ AI error: {e}[/red]")
    else:
        console.print("\n[yellow]6. AI features skipped (set OPENAI_API_KEY to enable)[/yellow]")
    
    # Display stats
    console.print("\n" + "="*50)
    console.print("[bold cyan]Final Statistics:[/bold cyan]")
    console.print(f"  📝 Notes: {len(storage.list_notes())}")
    console.print(f"  ✅ Tasks: {len(storage.list_tasks())}")
    console.print(f"  🔗 Links: {len(storage.get_links(note1['id']))}")
    console.print(f"  📁 Storage: JSON files in data/")
    console.print("="*50)
    
    console.print("\n[bold green]✓ Demo complete![/bold green]")
    console.print("\nRun [cyan]uv run python cli_v2.py[/cyan] to try the interactive CLI")

if __name__ == "__main__":
    main()
