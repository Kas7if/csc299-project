#!/bin/bash
# KnowledgeFlow Demo Script
# Run this to demonstrate all features

set -e  # Exit on error

echo "🎬 KnowledgeFlow Demo Script"
echo "============================"
echo ""

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY not set!"
    echo "AI features will not work without the API key."
    echo ""
    echo "To set it, run:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Navigate to knowledgeflow directory
cd "$(dirname "$0")/knowledgeflow"

echo "📍 Current directory: $(pwd)"
echo ""

# Function to pause and wait for user
pause() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# Demo 1: Run automated demo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 1: Automated Demo (with AI)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "This will create sample notes/tasks and show AI summarization"
pause

uv run python demo_v2.py

pause

# Demo 2: Show test suite
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 2: Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Running all 16 tests..."
pause

uv run pytest tests/test_json_storage.py -v

pause

# Demo 3: Show JSON files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 3: JSON Data Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "These are the data files created:"
pause

ls -lh data/
echo ""
echo "Sample note from notes.json:"
cat data/notes.json | python3 -m json.tool | head -20

pause

echo "Sample task from tasks.json:"
cat data/tasks.json | python3 -m json.tool | head -20

pause

# Demo 4: Interactive CLI
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 4: Interactive CLI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Launching interactive CLI..."
echo ""
echo "Try these options:"
echo "  2 - List all notes"
echo "  6 - List all tasks"
echo "  3 - Search notes"
echo "  9 - AI summarize (if API key is set)"
echo "  0 - Exit"
echo ""
pause

uv run python cli_v2.py

# Final summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Demo Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "What you just saw:"
echo "  ✓ Automated demo with AI summarization"
echo "  ✓ 16 passing tests (100% success rate)"
echo "  ✓ JSON data files (human-readable)"
echo "  ✓ Interactive CLI with rich UI"
echo ""
echo "Key features:"
echo "  📝 Notes with tags and search"
echo "  ✅ Tasks with priorities and status"
echo "  🔗 Links between notes and tasks"
echo "  🤖 AI-powered summarization (GPT-4o)"
echo "  🎨 Beautiful terminal UI"
echo ""
echo "For more info, see README.md and SUMMARY.md"
echo ""
