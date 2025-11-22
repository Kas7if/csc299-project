# KnowledgeFlow - Personal Knowledge Management System

A hybrid personal knowledge management system combining note-taking, task management, and AI-powered features.

## 🎯 Project Overview

KnowledgeFlow is a comprehensive PKMS (Personal Knowledge Management System) developed as a final project for CSC299. It evolved through multiple iterations, incorporating lessons learned from experimental tasks and prototypes.

**Key Features:**
- 📝 Note management with tags and full-text search
- ✅ Task management with status tracking and priorities
- 🔗 Linking system to connect related items
- 🤖 AI-powered summarization using OpenAI GPT-4o
- 🎨 Rich terminal UI with colors and formatting
- 💾 Dual storage: SQLite (v1) and JSON (v2)
- 🧪 Comprehensive test suite with pytest

## 🏗️ Architecture

The project uses a hybrid architecture:

### Version 1 (SQLite - Original)
- **Location:** `main.py` and `core/` directory
- **Storage:** SQLite database (`knowledgeflow.db`)
- **Status:** Functional prototype
- **Best for:** Complex queries, relationships, large datasets

### Version 2 (JSON - Current)
- **Location:** `cli_v2.py`, `core/json_storage.py`, `agents/`
- **Storage:** JSON files in `data/` directory
- **Status:** Production-ready with tests
- **Best for:** Portability, simplicity, version control

```
knowledgeflow/
├── cli_v2.py              # Enhanced CLI with rich UI
├── demo_v2.py            # Demonstration script
├── main.py               # Original SQLite version
├── core/
│   ├── json_storage.py   # JSON storage layer
│   ├── database.py       # SQLite implementation
│   ├── models.py         # Data models
│   └── categories.py     # Categorization
├── agents/
│   └── summarizer.py     # AI summarization agent
└── tests/
    ├── test_json_storage.py  # Storage tests (16 tests)
    └── conftest.py           # Test configuration
```

## 🚀 Installation

### Prerequisites
- Python 3.13+
- UV package manager ([install instructions](https://docs.astral.sh/uv/))
- OpenAI API key (optional, for AI features)

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd "299 final project/knowledgeflow"
```

2. **Install dependencies:**
```bash
uv sync
```

This installs:
- `openai` - AI agent integration
- `rich` - Terminal UI enhancements
- `pytest` - Testing framework

3. **Set up OpenAI API key (optional):**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📖 Usage

### Interactive CLI (Recommended)

Run the enhanced CLI with rich formatting:

```bash
uv run python cli_v2.py
```

Features:
- Create and manage notes with tags
- Create and track tasks with priorities
- Search across all items
- AI-powered summarization (requires API key)
- Generate titles from content
- Rich terminal UI with colors and tables

### Demo Script

See the system in action:

```bash
uv run python demo_v2.py
```

### Original SQLite Version

Run the v1 implementation:

```bash
uv run python main.py
```

### Python API

Use the storage layer programmatically:

```python
from core.json_storage import JSONStorage

# Initialize storage
storage = JSONStorage()

# Create a note
note = storage.create_note(
    title="My Note",
    content="Note content here",
    tags=["important", "work"]
)

# Create a task
task = storage.create_task(
    title="Complete project",
    description="Finish the final project",
    priority="high",
    status="pending"
)

# Search
results = storage.search_all("project")
print(f"Found {len(results['notes'])} notes")
print(f"Found {len(results['tasks'])} tasks")
```

### AI Agents

Use the summarizer agent:

```python
from agents.summarizer import SummarizerAgent
import os

# Initialize (requires OPENAI_API_KEY)
summarizer = SummarizerAgent()

# Summarize text
summary = summarizer.summarize_text(
    "Long text to summarize...",
    max_words=30
)

# Generate title
title = summarizer.generate_title(
    "Content here...",
    max_words=5
)
```

## 🧪 Testing

Run the complete test suite:

```bash
uv run pytest tests/ -v
```

Run specific tests:

```bash
# Test JSON storage
uv run pytest tests/test_json_storage.py -v

# Test with coverage
uv run pytest tests/ --cov=core --cov=agents
```

**Test Coverage:**
- ✅ 16 tests for JSON storage (notes, tasks, links)
- ✅ CRUD operations
- ✅ Search functionality
- ✅ Link management
- ✅ Data persistence

## 📊 Project Evolution

This project evolved through several iterations:

### tasks1 → tasks2 → tasks3
- Explored different PKMS approaches
- Experimented with JSON storage
- Added pytest testing framework
- Learned UV package management

### tasks4
- Integrated OpenAI Chat Completions API
- Experimented with GPT-4o model
- Developed summarization capabilities
- Temperature and token tuning

### tasks5
- Used GitHub spec-kit for spec-driven development
- Created constitution and specifications
- Built tasks manager with CLI
- Learned structured development approach

### knowledgeflow (Final)
- Combined best ideas from all experiments
- Hybrid SQLite + JSON architecture
- AI agent integration
- Rich terminal UI
- Comprehensive testing

## 🤖 AI Integration

### Summarization Agent

The `SummarizerAgent` uses OpenAI's GPT-4o model to:
- Summarize long notes into concise summaries
- Generate titles from content
- Batch process multiple items
- Configurable word limits

**Configuration:**
- Model: `gpt-4o`
- Temperature: `0.7`
- Max tokens: `150` (summaries), `50` (titles)
- Role: `developer` (for consistent output)

### Future Agent Ideas (Not Implemented)

**Q&A Agent:** Answer questions based on your knowledge base
- Search relevant notes/tasks
- Provide contextual answers
- Cross-reference related items

**Planning Agent:** Help prioritize and plan tasks
- Analyze task dependencies
- Suggest priorities
- Generate schedules

## 🎨 UI Features

The CLI uses the `rich` library for:
- 🎨 Colored output and syntax highlighting
- 📊 Beautiful tables for lists
- 📦 Panels for content display
- ✨ Status spinners for AI operations
- 📝 Markdown rendering for notes
- 🔄 Progress indicators

## 📁 Data Storage

### JSON Format (v2)

Data is stored in three JSON files:

**notes.json:**
```json
{
  "id": "uuid",
  "title": "Note Title",
  "content": "Note content...",
  "tags": ["tag1", "tag2"],
  "created_at": "2025-11-22T10:00:00",
  "updated_at": "2025-11-22T10:00:00"
}
```

**tasks.json:**
```json
{
  "id": "uuid",
  "title": "Task Title",
  "description": "Task description...",
  "status": "pending",
  "priority": "high",
  "tags": ["work"],
  "created_at": "2025-11-22T10:00:00",
  "updated_at": "2025-11-22T10:00:00"
}
```

**links.json:**
```json
{
  "id": "uuid",
  "from_id": "item-uuid",
  "to_id": "item-uuid",
  "link_type": "relates_to",
  "created_at": "2025-11-22T10:00:00"
}
```

### SQLite Format (v1)

Relational database with tables:
- `notes` - Note storage
- `tasks` - Task storage
- `categories` - Category management
- `links` - Relationship tracking

## 🔧 Development

### Project Structure

```
knowledgeflow/
├── pyproject.toml       # UV project configuration
├── .venv/              # Virtual environment
├── data/               # JSON storage (created at runtime)
├── core/               # Core modules
├── agents/             # AI agents
├── ui/                 # UI components (future)
└── tests/              # Test suite
```

### Dependencies

**Core:**
- `openai>=2.8.1` - AI integration
- `rich>=14.2.0` - Terminal UI

**Development:**
- `pytest>=9.0.1` - Testing framework

### Adding New Features

1. Implement in appropriate module (`core/` or `agents/`)
2. Add tests in `tests/`
3. Update CLI in `cli_v2.py`
4. Run tests to verify
5. Update documentation

## 🎓 Lessons Learned

**What Worked:**
- ✅ UV package manager - fast, reliable, simple
- ✅ JSON storage - portable, version-controllable
- ✅ pytest - comprehensive testing
- ✅ Rich library - beautiful UIs easily
- ✅ Iterative development - tasks1-5 → final
- ✅ OpenAI API - powerful summarization

**What Didn't Work:**
- ❌ GPT-5-mini - empty responses with API key
- ❌ Complex SQLite schema - overkill for MVP
- ❌ Over-engineering early - simpler is better
- ❌ No tests initially - added technical debt

**Key Insights:**
1. **Start simple, iterate:** JSON before SQL
2. **Test early:** pytest from the start
3. **Use AI wisely:** Summarization >> full generation
4. **Spec-driven helps:** tasks5 showed the value
5. **UV is amazing:** Better than pip/venv

## 📝 Future Enhancements

- [ ] Web UI with Flask/FastAPI
- [ ] Q&A agent implementation
- [ ] Planning agent implementation
- [ ] Spaced repetition for notes
- [ ] Export to Markdown/PDF
- [ ] Cloud sync capabilities
- [ ] Mobile app
- [ ] Graph visualization of links

## 📄 License

Educational project for CSC299 - Fall 2025

## 👤 Author

Kashif Yaboi
- Course: CSC299
- Term: Fall 2025
- Deadline: November 24, 2025

## 🙏 Acknowledgments

- ChatGPT for planning and architecture discussions
- GitHub Copilot for code assistance
- UV team for excellent tooling
- Rich library for beautiful terminal UIs
- OpenAI for GPT-4o API

---

**Status:** ✅ Production-ready
**Version:** 2.0 (JSON Edition)
**Last Updated:** November 22, 2025
