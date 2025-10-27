# KnowledgeFlow

**Personal Knowledge & Task Management System with AI**

A terminal-based application that combines note-taking, task management, and AI agents to help you organize your knowledge and work.

## 🎯 Project Status

**Current Phase:** Week 1 - Foundation  
**Deadline:** November 24, 2025 @ 1:30 PM  
**On Track:** 🟢 YES

## 📁 Repository Structure

```
csc299-project/
├── knowledgeflow/          # Main application
│   ├── core/               # Database and models
│   ├── agents/             # AI agents
│   ├── ui/                 # User interface
│   ├── main.py            # Entry point
│   └── demo.py            # Demo script
├── tests/                  # Test suite
├── specs/                  # Feature specifications
├── tasks1/                 # Early task manager prototype
├── PROJECT_PLAN.md        # Development roadmap
└── README.md              # This file
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Kas7if/csc299-project.git
cd csc299-project

# Run the application
cd knowledgeflow
python3 main.py

# Run demo with sample data
python3 demo.py

# Run tests
cd ..
python3 -m pytest tests/ -v
```

## ✨ Features

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
