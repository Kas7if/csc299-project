# Tasks2 Experiments - Quick Setup

## Install Dependencies (Optional)

For full experimentation, install these:

```bash
# Rich for beautiful terminal UI
pip3 install rich

# OpenAI for AI features
pip3 install openai python-dotenv

# NumPy for embeddings/similarity
pip3 install numpy
```

## Experiments Available

### 1. Rich UI (`experiment_rich_ui.py`)
Test beautiful terminal formatting:
```bash
python3 experiment_rich_ui.py
```

Shows:
- Tables for notes/tasks
- Panels for highlights
- Markdown rendering
- Tree structures for categories
- Progress bars
- Interactive prompts

### 2. OpenAI Integration (`experiment_openai.py`)
Test AI features (requires API key):
```bash
# Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-key" > .env

python3 experiment_openai.py
```

Tests:
- Auto-tagging notes
- Breaking down tasks
- Semantic search with embeddings
- Cost estimation

### 3. Command Parsing (`experiment_parsers.py`)
Test different command parsing approaches:
```bash
python3 experiment_parsers.py
```

Shows:
- Simple parsing (current approach)
- Advanced flag-based parsing
- Natural language hints

## Quick Start - Try Rich First!

```bash
cd tasks2
pip3 install rich
python3 experiment_rich_ui.py
```

This is the easiest to try and will show you what the enhanced UI could look like!

## Your Experiments

Add your own experiments here:
- `experiment_xyz.py` - Try something new!
- Test ideas quickly
- Break things
- Have fun!
