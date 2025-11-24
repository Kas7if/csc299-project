# KnowledgeFlow - Personal Knowledge Management System

**CSC299 Final Project - Fall 2025**

A hybrid personal knowledge management system combining note-taking, task management, and AI-powered features. Built through iterative development from experimental prototypes to production-ready system.

---

## 🎯 Project Overview

KnowledgeFlow evolved from a series of experiments (tasks1-5) into a comprehensive PKMS with:
- 📝 **Note Management** - Create, organize, and search notes with tags
- ✅ **Task Tracking** - Manage tasks with priorities and status
- 🔗 **Linking System** - Connect related notes and tasks
- 🤖 **AI Agents** - GPT-4o powered summarization and title generation
- 🎨 **Rich Terminal UI** - Beautiful, interactive command-line interface
- 💾 **Dual Storage** - SQLite (v1) and JSON (v2) implementations
- 🧪 **Test Suite** - 16 comprehensive tests with 100% pass rate

**Final Deliverable Status:** ✅ Complete  
**Submission Deadline:** November 24, 2025 @ 1:30 PM

---

## 📁 Repository Structure

```
csc299-project/
├── knowledgeflow/              # 🎯 MAIN APPLICATION
│   ├── cli_v2.py              # Enhanced CLI with rich UI
│   ├── demo_v2.py             # Demo script
│   ├── main.py                # SQLite version (v1)
│   ├── core/
│   │   ├── json_storage.py    # JSON storage layer (v2) ⭐
│   │   ├── database.py        # SQLite implementation
│   │   ├── models.py          # Data models
│   │   └── categories.py      # Categorization
│   ├── agents/
│   │   └── summarizer.py      # AI summarization agent ⭐
│   ├── tests/
│   │   ├── test_json_storage.py  # 16 passing tests ⭐
│   │   └── conftest.py
│   ├── pyproject.toml         # UV project config
│   ├── README_v2.md           # Detailed documentation
│   └── STATUS.md              # Progress tracking
│
├── tasks1/                     # Prototype: CLI task manager
├── tasks2/                     # Experiments: PKMS iterations
├── tasks3/                     # Prototype: UV + pytest
├── tasks4/                     # Experiment: OpenAI integration
├── tasks5/                     # Experiment: Spec-kit workflow
│
├── specs/                      # Feature specifications
├── tests/                      # Legacy tests
├── SUMMARY.md                  # Development narrative (500+ words)
├── video.txt                   # YouTube demo URL
└── README.md                   # This file
```

**⭐ = Core v2 components (JSON Edition)**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- [UV package manager](https://docs.astral.sh/uv/) (recommended)
- OpenAI API key (optional, for AI features)

### Installation

```bash
# Clone the repository
git clone https://github.com/Kas7if/csc299-project.git
cd csc299-project/knowledgeflow

# Install dependencies with UV (recommended)
uv sync

# OR with pip
pip install openai rich pytest
```

### Running KnowledgeFlow v2

```bash
# Interactive CLI (recommended)
uv run python cli_v2.py

# Demo with AI features
export OPENAI_API_KEY="your-key-here"
uv run python demo_v2.py

# Run tests
uv run pytest tests/test_json_storage.py -v
```

### Running KnowledgeFlow v1 (SQLite)

```bash
# SQLite version
python main.py

# Original demo
python demo.py
```

---

## ✨ Features

### Core Functionality (v2)

**Notes Management:**
- Create notes with title, content, and tags
- Full-text search across all notes
- Tag-based filtering
- View individual notes with markdown rendering

**Task Management:**
- Create tasks with priorities (low/medium/high)
- Status tracking (pending/in_progress/completed)
- Filter by status and priority
- Search tasks by keywords

**Linking System:**
- Connect related notes and tasks
- Track relationships between items
- Automatic cleanup when items deleted

**AI Features (requires API key):**
- 🤖 Summarize notes and tasks (GPT-4o)
- 🤖 Generate titles from content
- 🤖 Batch processing capabilities
- 🤖 Configurable word limits

**Terminal UI:**
- 🎨 Colored output with rich library
- 📊 Beautiful tables for lists
- 📦 Panels for content display
- ✨ Status spinners for operations
- 🔄 Emoji indicators (⏳ pending, 🔄 in progress, ✅ completed)

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/test_json_storage.py -v

# Run with coverage
uv run pytest tests/ --cov=core --cov=agents

# Quick test
uv run pytest tests/test_json_storage.py -q
```

**Test Results:**
- ✅ 16/16 tests passing (100%)
- ✅ Notes: Create, read, update, delete, search
- ✅ Tasks: Create, read, update, delete, search, filter
- ✅ Links: Create, retrieve, auto-cleanup
- ✅ Unified search across notes and tasks

---

## 📖 Documentation

- **[README_v2.md](knowledgeflow/README_v2.md)** - Complete usage guide for v2
- **[STATUS.md](knowledgeflow/STATUS.md)** - Current progress and achievements
- **[SUMMARY.md](SUMMARY.md)** - Development narrative and lessons learned
- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** - Original project roadmap
- **Individual task READMEs** - See tasks1-5 directories

---

## 🎓 Project Evolution

This project evolved through iterative development:

1. **tasks1** - Basic CLI task manager with JSON storage
2. **tasks2** - PKMS experiments and UI iterations
3. **tasks3** - UV package manager + pytest integration
4. **tasks4** - OpenAI GPT-4o Chat Completions API
5. **tasks5** - Spec-kit workflow and task manager
6. **knowledgeflow v1** - SQLite-based PKMS prototype
7. **knowledgeflow v2** - JSON storage + AI agents + rich UI ⭐

Each iteration built upon lessons learned, leading to the final production-ready system.

---

## 🛠️ Technology Stack

**Core:**
- Python 3.13
- UV package manager
- SQLite (v1) / JSON (v2)

**Libraries:**
- `openai` (2.8.1) - AI integration
- `rich` (14.2.0) - Terminal UI
- `pytest` (9.0.1) - Testing framework

**AI:**
- OpenAI GPT-4o model
- Chat Completions API
- Temperature: 0.7, Max tokens: 150

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Lines of Code | ~1,500+ |
| Test Coverage | 100% of storage layer |
| Tests Written | 16 tests |
| Tests Passing | 16/16 (100%) |
| AI Agent | 1 (Summarizer) |
| Development Time | ~3 weeks |
| Iterations | 7 (tasks1-5 + v1 + v2) |

---

## 🎬 Demo Video

See the system in action: [video.txt](video.txt)

**Video Contents:**
- Project overview and evolution
- Live demo of CLI features
- AI summarization in action
- Code walkthrough
- Testing demonstration

---

## 👤 Author

**Kashif Yaboi**  
CSC299 - Fall 2025  
GitHub: [@Kas7if](https://github.com/Kas7if)

---

## 🙏 Acknowledgments

- **ChatGPT** - Planning, architecture discussions, and development guidance
- **GitHub Copilot** - Code assistance and completions
- **UV Team** - Excellent Python package management tooling
- **Rich Library** - Beautiful terminal UI capabilities
- **OpenAI** - GPT-4o API for AI features

---

## 📄 License

Educational project for CSC299 - Fall 2025

---

## 🔗 Quick Links

- **Main Application:** [knowledgeflow/cli_v2.py](knowledgeflow/cli_v2.py)
- **Documentation:** [knowledgeflow/README_v2.md](knowledgeflow/README_v2.md)
- **Tests:** [knowledgeflow/tests/](knowledgeflow/tests/)
- **Development Summary:** [SUMMARY.md](SUMMARY.md)

**Status:** ✅ Production Ready | **Version:** 2.0 | **Last Updated:** November 23, 2025

### Current (v0.1.0)
- ✅ Note management with tags and search
- ✅ Task management with priorities and deadlines
- ✅ SQLite database for portable storage
- ✅ Terminal chat interface
- ✅ Cross-platform support

### Planned
- 📎 Bidirectional note linking
- 🗂️ Hierarchical categories
- 🤖 AI agents (auto-tagging, link suggestions, task analysis)
- 🔍 Semantic search with embeddings
- 📊 Knowledge graph visualization
- 🌐 Natural language interface

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Database:** SQLite3
- **UI:** Rich (coming soon)
- **AI:** OpenAI/Anthropic (coming soon)
- **Testing:** pytest

## 📚 Documentation

- [Project Plan](PROJECT_PLAN.md) - Detailed 4-week development plan
- [Specifications](specs/) - Feature specifications
- [Tasks1 Prototype](tasks1/) - Early exploration

## 🎓 Course Project

This is a final project for CSC299 - Vibecoding, demonstrating:
- AI-assisted software development
- Iterative prototyping
- Test-driven development
- Specification-driven design

## 👨‍💻 Author

**Kashif** - [@Kas7if](https://github.com/Kas7if)

## 📄 License

Educational project - CSC299 Fall 2025
