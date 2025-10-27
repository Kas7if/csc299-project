#!/usr/bin/env python3
"""
Experiment 1: Rich Terminal UI
Test out the Rich library for beautiful terminal output
"""

# First, let's see if Rich is installed
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.progress import track
    from rich.tree import Tree
    from rich import print as rprint
    import time
    
    print("✅ Rich library is installed!")
except ImportError:
    print("❌ Rich library not installed.")
    print("Install it with: pip3 install rich")
    exit(1)

console = Console()

def demo_basic_formatting():
    """Demo basic Rich formatting"""
    console.print("\n[bold cyan]1. Basic Formatting[/bold cyan]")
    console.print("This is [bold]bold[/bold] text")
    console.print("This is [italic]italic[/italic] text")
    console.print("This is [bold red]bold red[/bold red] text")
    console.print("This is [link=https://github.com]a link[/link]")

def demo_panels():
    """Demo Rich panels"""
    console.print("\n[bold cyan]2. Panels[/bold cyan]")
    
    panel = Panel(
        "[bold green]This is a panel![/bold green]\nPanels are great for highlighting content.",
        title="Welcome",
        border_style="cyan"
    )
    console.print(panel)

def demo_tables():
    """Demo Rich tables"""
    console.print("\n[bold cyan]3. Tables[/bold cyan]")
    
    table = Table(title="Sample Notes", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Title", style="green")
    table.add_column("Tags", style="yellow")
    table.add_column("Created", style="blue")
    
    table.add_row("1", "Python Tutorial", "python, coding", "2025-10-27")
    table.add_row("2", "Project Ideas", "ideas, planning", "2025-10-27")
    table.add_row("3", "Meeting Notes", "work, meetings", "2025-10-26")
    
    console.print(table)

def demo_markdown():
    """Demo Rich Markdown rendering"""
    console.print("\n[bold cyan]4. Markdown Rendering[/bold cyan]")
    
    markdown_text = """
# Sample Note

This is a **rich markdown** note with:

- Bullet points
- *Emphasis*
- `code blocks`

## Code Example

```python
def hello():
    print("Hello, World!")
```
"""
    
    md = Markdown(markdown_text)
    console.print(md)

def demo_tree():
    """Demo Rich tree structure"""
    console.print("\n[bold cyan]5. Tree Structure (for Categories)[/bold cyan]")
    
    tree = Tree("📁 Categories")
    
    coding = tree.add("💻 Coding")
    coding.add("🐍 Python")
    coding.add("🌐 JavaScript")
    
    work = tree.add("💼 Work")
    work.add("📊 Projects")
    work.add("📝 Meeting Notes")
    
    personal = tree.add("👤 Personal")
    personal.add("📚 Learning")
    personal.add("💭 Ideas")
    
    console.print(tree)

def demo_progress():
    """Demo Rich progress bars"""
    console.print("\n[bold cyan]6. Progress Bars[/bold cyan]")
    
    items = range(20)
    for _ in track(items, description="Processing notes..."):
        time.sleep(0.05)
    
    console.print("[green]✓ Processing complete![/green]")

def demo_interactive():
    """Demo Rich interactive prompts"""
    console.print("\n[bold cyan]7. Interactive Prompts[/bold cyan]")
    
    name = Prompt.ask("What's your name?", default="User")
    console.print(f"Hello, [bold green]{name}[/bold green]!")
    
    likes_rich = Confirm.ask("Do you like Rich library?")
    if likes_rich:
        console.print("[bold green]Awesome! 🎉[/bold green]")
    else:
        console.print("[yellow]That's okay! 😊[/yellow]")

def demo_status():
    """Demo Rich status indicators"""
    console.print("\n[bold cyan]8. Status Indicators[/bold cyan]")
    
    with console.status("[bold green]Creating note...", spinner="dots"):
        time.sleep(1)
    console.print("✓ Note created!")
    
    with console.status("[bold yellow]Building knowledge graph...", spinner="dots"):
        time.sleep(1)
    console.print("✓ Graph built!")

def main():
    """Run all demos"""
    console.print("\n" + "="*60)
    console.print("[bold magenta]Rich Library Demo - Terminal UI Experiments[/bold magenta]")
    console.print("="*60)
    
    demo_basic_formatting()
    demo_panels()
    demo_tables()
    demo_markdown()
    demo_tree()
    demo_progress()
    demo_interactive()
    demo_status()
    
    console.print("\n" + "="*60)
    console.print("[bold green]✨ Demo Complete![/bold green]")
    console.print("="*60)
    console.print("\n💡 This is what we can integrate into KnowledgeFlow!")

if __name__ == "__main__":
    main()
