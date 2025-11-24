# KnowledgeFlow - Video Demo Script

**Target Length:** 6-8 minutes  
**Date:** November 24, 2025  
**Author:** Kashif Mohammed

---

## 🎬 RECORDING SETUP

### Before You Start:
1. Clean your desktop/minimize windows
2. Set terminal to comfortable font size (14-16pt)
3. Have these terminals ready:
   - Terminal 1: For running commands
   - Terminal 2: For showing files (optional)
4. Set API key in environment (BEFORE recording - don't show this on screen!):
   ```bash
   # DO NOT RECORD THIS PART!
   export OPENAI_API_KEY="your-api-key-here"
   ```
5. Navigate to project:
   ```bash
   cd "/Users/kashifyaboi/299 final project"
   ```

**⚠️ IMPORTANT:** Set the API key BEFORE you start recording. Don't show the key in the video!

---

## 📝 SCRIPT

### SEGMENT 1: INTRODUCTION (1 minute)

**[Screen: Show project folder in VS Code or Finder]**

> "Hi, I'm Kashif, and this is my CSC299 final project: KnowledgeFlow, a personal knowledge management system with AI capabilities.

> This project evolved through seven iterations over the past few weeks, starting from simple task manager prototypes and culminating in a production-ready system with AI-powered features.

**[Screen: Show folder structure]**

> Let me show you the structure. We have tasks 1 through 5, which were experimental prototypes where I learned different technologies. Then the final knowledgeflow directory contains both version 1 with SQLite and version 2 with JSON storage plus AI agents.

**[Screen: Open README.md briefly]**

> The project includes comprehensive documentation, 16 passing tests, and real OpenAI GPT-4o integration for summarization. Let's dive into the demo."

---

### SEGMENT 2: LIVE DEMO (4 minutes)

#### Part A: Automated Demo (1.5 min)

**[Screen: Terminal, navigate to knowledgeflow]**

```bash
cd knowledgeflow
```

> "First, let me run the automated demo to show all features in action."

```bash
uv run python demo_v2.py
```

**[Wait for output, point out key parts as they appear]**

> "Watch as it initializes JSON storage, creates sample notes and tasks, creates links between them, and performs searches. 

> Now here's the exciting part - AI summarization using OpenAI's GPT-4o model."

**[Point to AI summary output]**

> "Look at this - it took a long note about Python best practices and condensed it into a concise 30-word summary. Same for tasks. And it even generated a title from content.

> The demo shows we have 12 notes, 12 tasks, 1 link between them, all stored in simple JSON files."

#### Part B: Interactive CLI (1.5 min)

**[Screen: Launch CLI]**

```bash
uv run python cli_v2.py
```

> "Now let's try the interactive CLI. This uses the Rich library for beautiful terminal output."

**[Show menu, select option 2 - List notes]**

```
2
[Enter]
[Leave tag filter blank]
```

> "Here's a table of all our notes with IDs, titles, tags, and creation dates. Very clean and organized.

**[Back to menu, select option 6 - List tasks]**

```
6
[Enter]
[Leave status filter blank]
```

> "And here are our tasks with emoji indicators - hourglass for pending, checkmark for completed - along with priority levels color-coded."

**[Back to menu, select option 3 - Search notes]**

```
3
python
```

> "Let's search for 'python' - and it instantly finds all notes containing that keyword, showing them in nice panels."

**[Back to menu, select option 9 - Summarize]**

```
9
note
[Use first 8 chars of any note ID from previous list]
```

> "Now for the AI magic - I'm asking it to summarize one of my notes. Watch this..."

**[Wait for AI response]**

> "Boom! GPT-4o just condensed my note into a perfect summary. This is real AI integration, not mocked responses."

**[Exit CLI]**

```
0
```

#### Part C: JSON Files (1 min)

**[Screen: Show data directory]**

```bash
ls -lh data/
cat data/notes.json | head -20
```

> "All data is stored in simple JSON files. Look how readable this is - you can see the note structure with ID, title, content, tags, and timestamps.

```bash
cat data/tasks.json | head -20
```

> This is the tasks file with status, priority, and descriptions. Everything is human-readable and git-friendly. No database setup required."

---

### SEGMENT 3: CODE WALKTHROUGH (2 minutes)

#### Part A: JSON Storage (45 sec)

**[Screen: Open core/json_storage.py in editor]**

> "Let me show you the architecture. This is the JSON storage layer - completely separated from the UI.

**[Scroll through file, highlight key methods]**

> It has clean methods for CRUD operations: create_note, get_note, update_note, delete_note, and the same for tasks. 

> Notice this atomic write pattern here - we write to a temp file first, then rename it. This prevents data corruption if the program crashes.

> Down here we have link management - connecting notes and tasks together with automatic cleanup when items are deleted.

> The whole storage layer is about 250 lines and handles everything - notes, tasks, links, and unified search."

#### Part B: AI Agent (45 sec)

**[Screen: Open agents/summarizer.py]**

> "Here's the AI agent. It's a wrapper around OpenAI's API.

**[Scroll through, highlight key parts]**

> We initialize with the API key, use the GPT-4o model, and have methods for summarizing notes, summarizing tasks, and generating titles.

> The key is this chat completions API call - we set the role as 'developer' for consistent output, use temperature 0.7 for some creativity, and limit tokens to 150.

> It can handle batch processing and has configurable word limits. The agent is self-contained - about 150 lines total."

#### Part C: Tests (30 sec)

**[Screen: Run tests]**

```bash
cd /Users/kashifyaboi/299\ final\ project/knowledgeflow
uv run pytest tests/test_json_storage.py -v
```

> "And here's proof it all works - 16 comprehensive tests covering every operation.

**[Wait for tests to run]**

> Look at that - 16 passed in 0.08 seconds. 100% success rate. Tests cover creating, reading, updating, deleting, searching, linking - everything."

---

### SEGMENT 4: WRAP-UP (1 minute)

**[Screen: Show SUMMARY.md or README briefly]**

> "This project taught me so much. I documented everything in a 2,847-word development narrative.

**[Show checklist or final stats]**

> Key lessons: Start simple and iterate. UV package manager is amazing. JSON can beat SQL for the right use case. AI integration is more accessible than I thought. And test-driven development really works.

**[Screen: Back to terminal with project structure]**

> The final system has:
> - 1,500+ lines of code
> - 16 passing tests
> - Real GPT-4o AI integration
> - Beautiful terminal UI with the Rich library
> - Complete documentation
> - And it actually works!

**[Screen: Show GitHub repo or final folder]**

> Everything is on GitHub at Kas7if/csc299-project. Thanks for watching, and thanks to Copilot for being an excellent development partner throughout this journey!"

---

## 🎯 POST-RECORDING CHECKLIST

### After Recording:
- [ ] Review video - check audio quality
- [ ] Trim any dead air or mistakes
- [ ] Add title card with your name and project
- [ ] Export video (1080p, MP4)
- [ ] Upload to YouTube
- [ ] Set as Unlisted (not Private, not Public)
- [ ] Copy YouTube URL
- [ ] Update video.txt with URL
- [ ] Commit and push video.txt

### Upload Details:
- **Title:** "KnowledgeFlow - Personal Knowledge Management System with AI (CSC299 Final Project)"
- **Description:**
  ```
  CSC299 Final Project - Fall 2025
  By: Kashif 
  
  A personal knowledge management system combining note-taking, task management, 
  and AI-powered features using OpenAI GPT-4o.
  
  Technologies: Python, UV, pytest, OpenAI API, Rich library
  Features: JSON storage, AI summarization, terminal UI, comprehensive tests
  
  GitHub: https://github.com/Kas7if/csc299-project
  ```
- **Visibility:** Unlisted
- **Category:** Science & Technology

---

## ⏱️ TIMING BREAKDOWN

| Segment | Content | Target Time |
|---------|---------|-------------|
| 1. Intro | Project overview | 1:00 |
| 2A. Auto Demo | demo_v2.py | 1:30 |
| 2B. Interactive | CLI walkthrough | 1:30 |
| 2C. JSON Files | Show data files | 1:00 |
| 3A. Storage Code | json_storage.py | 0:45 |
| 3B. AI Code | summarizer.py | 0:45 |
| 3C. Tests | Run pytest | 0:30 |
| 4. Wrap-up | Summary & stats | 1:00 |
| **TOTAL** | | **8:00** |

---

## 💡 RECORDING TIPS

1. **Speak clearly** - Don't rush, pause between segments
2. **Show, don't just tell** - Let the code/output be visible
3. **Highlight important parts** - Use cursor to point at key lines
4. **If you mess up** - Just pause and restart that sentence
5. **Energy** - Sound enthusiastic! You built something cool!
6. **Pacing** - Slow down for complex parts, speed up for familiar parts
7. **Ending** - End on a high note with your key achievements

---

## 🚀 QUICK COMMAND REFERENCE

```bash
# Setup (DO THIS BEFORE RECORDING - DON'T SHOW ON SCREEN!)
cd "/Users/kashifyaboi/299 final project"
export OPENAI_API_KEY="your-api-key-here"  # Use your actual key
cd knowledgeflow

# Demo (START RECORDING HERE)
uv run python demo_v2.py

# CLI
uv run python cli_v2.py
# Options: 2 (list notes), 6 (list tasks), 3 (search), 9 (AI summary), 0 (exit)

# Show JSON
ls -lh data/
cat data/notes.json | head -20
cat data/tasks.json | head -20

# Tests
uv run pytest tests/test_json_storage.py -v

# Show files in editor
code core/json_storage.py
code agents/summarizer.py
```

---

**Ready to record? Follow the script, have fun, and show off what you built! 🎬**