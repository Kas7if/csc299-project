# 🎬 Video Recording Guide - Simple Breakdown

## ⚡ SUPER QUICK VERSION

**Total Time:** 6-8 minutes

1. **Intro** (1 min) - Show folder, explain project
2. **Run `./run_demo.sh`** (5 min) - Let it guide you through everything
3. **Wrap-up** (1 min) - Show stats, say thanks

Done! 🎉

---

## 🎯 DETAILED BREAKDOWN

### Before You Start (DON'T RECORD THIS!)

```bash
# 1. Set API key (do this BEFORE recording!)
export OPENAI_API_KEY="your-actual-api-key-here"

# 2. Navigate to project
cd "/Users/kashifyaboi/299 final project"

# 3. Test that everything works
./run_demo.sh
```

Once you've tested, you're ready to record!

---

## 🎬 RECORDING SEGMENTS

### SEGMENT 1: Introduction (1 minute)

**What to show:**
- Project folder structure
- README.md briefly
- Explain: "evolved through 7 iterations, has AI, tests, docs"

**What to say:**
> "Hi, I'm Kashif. This is KnowledgeFlow, my CSC299 final project. It's a personal knowledge management system with AI capabilities using OpenAI GPT-4o. It evolved through seven iterations - tasks 1 through 5 were prototypes, and the final knowledgeflow directory has the production system with both SQLite and JSON versions, plus AI agents."

---

### SEGMENT 2: Automated Demo (2 minutes)

**What to show:**
```bash
cd knowledgeflow
uv run python demo_v2.py
```

**What to say while it runs:**
> "Let me run the automated demo. Watch as it creates notes and tasks, performs searches, and here comes the AI part - it's using GPT-4o to summarize this note about Python best practices. See how it condensed it into just 30 words? That's real AI, not mocked. Same for tasks and title generation."

**Highlight:**
- Point to AI summaries when they appear
- Point to final statistics

---

### SEGMENT 3: Interactive CLI (2 minutes)

**What to show:**
```bash
uv run python cli_v2.py
```

**Menu flow:**
1. Type `2` - List notes (show table)
2. Type `6` - List tasks (show emoji indicators)
3. Type `3` - Search for "python"
4. Type `9` - AI summarize a note (copy a note ID from list)
5. Type `0` - Exit

**What to say:**
> "Now the interactive CLI. Option 2 lists all notes in a nice table. Option 6 shows tasks with emoji indicators and color-coded priorities. Let's search for 'python' - instant results. Now for AI - option 9 - I'll summarize this note... and boom, GPT-4o just gave us a perfect summary."

---

### SEGMENT 4: Show Data Files (1 minute)

**What to show:**
```bash
ls -lh data/
cat data/notes.json | head -20
cat data/tasks.json | head -15
```

**What to say:**
> "All data is stored in simple JSON files. Look how readable this is - you can see the structure with IDs, titles, content, tags, timestamps. No database setup needed. Everything is git-friendly and human-readable."

---

### SEGMENT 5: Code Walkthrough (1.5 minutes)

**What to show:**
```bash
# Open in your editor
code core/json_storage.py
# Scroll through, highlight key methods
# Then
code agents/summarizer.py
# Show the GPT-4o integration
```

**What to say:**
> "Quick code walkthrough. Here's the storage layer - clean separation of concerns. Create, read, update, delete for notes and tasks. This atomic write pattern prevents data corruption. And here's the AI agent - wraps OpenAI's API, uses GPT-4o, temperature 0.7, customizable word limits. About 150 lines total."

---

### SEGMENT 6: Tests (30 seconds)

**What to show:**
```bash
uv run pytest tests/test_json_storage.py -v
```

**What to say:**
> "And proof it all works - 16 comprehensive tests. Watch... 16 passed in 0.08 seconds. 100% success rate. Tests cover everything - CRUD operations, search, links, the whole system."

---

### SEGMENT 7: Wrap-up (1 minute)

**What to say:**
> "So to summarize: This is KnowledgeFlow, a fully functional knowledge management system. Key achievements - 1500 plus lines of code, 16 passing tests, real GPT-4o integration, beautiful terminal UI with the Rich library, complete documentation including a 2,847-word development narrative. The biggest lesson? Iterate fast, test early, and simple solutions often beat complex ones. JSON storage won over SQLite because it matched the problem better. Everything is on GitHub at Kas7if slash csc299-project. Thanks for watching!"

---

## 🎥 RECORDING TIPS

### Screen Setup:
1. **Clean desktop** - close unnecessary windows
2. **Terminal font size** - 14-16pt so it's readable
3. **Full screen terminal** - or at least 80% of screen
4. **Dark/Light theme** - whatever looks better on camera

### Recording Tools:
- **Mac:** QuickTime (built-in) - `Cmd+Shift+5`
- **Windows:** Xbox Game Bar - `Win+G`
- **Cross-platform:** OBS Studio (free)

### Do's:
- ✅ Speak clearly and with energy
- ✅ Pause between segments
- ✅ Point with cursor to highlight things
- ✅ Let commands run fully on screen
- ✅ Show your enthusiasm!

### Don'ts:
- ❌ Rush through sections
- ❌ Apologize or say "um" too much
- ❌ Show your API key!
- ❌ Record in a noisy environment
- ❌ Use tiny font

---

## 📝 EASY SCRIPT TO FOLLOW

Just read this while recording:

```
[Show folder]
"Hi, I'm Kashif, and this is KnowledgeFlow, my CSC299 final project. 
It's a knowledge management system with AI using OpenAI GPT-4o."

[cd knowledgeflow]
"Let me run the demo..."

[uv run python demo_v2.py]
"Creating notes and tasks... and here's the AI summarization using 
GPT-4o. See how it condensed that note? That's real AI."

[Wait for demo to finish]
"Now the interactive CLI..."

[uv run python cli_v2.py]
"Option 2 shows all notes in a table. Option 6 shows tasks. 
Let's search... and AI summarize..."

[Type: 2, Enter, 6, Enter, 3, python, Enter, 9, note, <note-id>, Enter, 0]

"The data is stored in JSON files..."
[ls -lh data/]
[cat data/notes.json | head -20]

"Quick code walkthrough..."
[Show json_storage.py and summarizer.py in editor]

"And proof with tests..."
[uv run pytest tests/ -v]
"16 passed, 100% success rate."

"To wrap up: 1500+ lines of code, 16 tests, real AI, beautiful UI, 
complete docs. Biggest lesson: iterate fast and keep it simple. 
Everything's on GitHub. Thanks!"
```

---

## ⏱️ TIME MANAGEMENT

If you're running long:
- Skip showing `tasks.json` (just show `notes.json`)
- Make code walkthrough faster (just scroll, don't explain every line)
- Combine segments 4 and 5

If you're running short:
- Add more detail in code walkthrough
- Show more CLI features
- Mention specific challenges you faced

---

## 🚀 READY TO RECORD?

1. ✅ Set API key (before recording!)
2. ✅ Test `./run_demo.sh` works
3. ✅ Open screen recorder
4. ✅ Follow this guide
5. ✅ Be yourself and have fun!

**You got this!** 🎬
