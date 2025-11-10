# Tasks4: OpenAI Task Summarizer

A standalone experiment using the OpenAI Chat Completions API to summarize paragraph-length task descriptions into short phrases.

## Features

- 🤖 Uses GPT-4o-mini model for task summarization
- 🔄 Processes multiple task descriptions in a loop
- 📝 Includes 3 sample paragraph-length descriptions
- ✨ Summarizes each task into a concise 5-10 word phrase

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

Run the summarizer:
```bash
uv run tasks4
```

This will:
1. Initialize the OpenAI client
2. Process each sample task description
3. Display the original text (truncated) and its summary
4. Print all summaries at the end

## Sample Output

```
================================================================================
🤖 Tasks4: OpenAI Task Summarizer
================================================================================

✅ OpenAI client initialized
📝 Processing 3 task descriptions...

────────────────────────────────────────────────────────────────────────────────
Task #1:
────────────────────────────────────────────────────────────────────────────────

📄 Original (567 characters):
   I need to complete my CSC299 final project which includes finishing all the remaining tasks...

🔄 Summarizing with GPT-4o-mini...
✨ Summary: Complete CSC299 project with all tasks by Nov 24th

...
```

## Requirements

- Python 3.13+
- OpenAI API key
- `openai` package (installed via uv)
