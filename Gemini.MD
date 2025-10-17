Prompt : What can I do for my vibe coding lab class final project? *Final Project Details* 

Of course! Based on your project requirements, you can build an integrated "Cognitive Command Center"—a personal AI-powered second brain that runs entirely in your terminal.

The core idea is to create a seamless environment where your notes (knowledge) and your to-do list (tasks) are interconnected. An AI agent acts as your assistant, helping you connect ideas, plan projects, and retrieve information from your own data.

---

### ## Core Project Concept: The "Cognitive Command Center" 🧠

Think of this as your personal, text-based JARVIS. It's a single interface where you manage what you know and what you need to do.

* **Knowledge Base (PKMS):** A collection of Markdown notes. You can dump thoughts, meeting notes, code snippets, or web clippings here.
* **Action Center (Tasks):** Your to-do list. Tasks can be simple or part of larger projects.
* **The Bridge (Chat & AI):** Your terminal interface is how you talk to your system. You can give it simple commands (`task add "Finish project proposal"`) or ask it complex questions (`"What were my main ideas about the new database design?"`). The AI agents work in the background to make the system smarter.



---

### ## Feature Ideas by Component

Here are some specific features you could implement for each part of the project.

#### Personal Knowledge Management System (PKMS)

* **Core:** Create, edit, and view notes in Markdown. All notes should be searchable.
* **Linking:** Implement a wiki-style linking system using `[[Note Title]]` syntax. When you view a note, it could show "backlinks"—other notes that link *to* it.
* **Tagging:** Add tags to notes (e.g., `#python`, `#project-ideas`) to categorize and easily find related information.
* **Unique Feature:** A **"Daily Note"** command (`note today`) that creates or opens a journal entry for the current date, making it easy to log thoughts chronologically.

#### Task Management System

* **Core:** Create tasks with descriptions, deadlines, and priorities (e.g., low, medium, high). Ability to mark tasks as complete.
* **Projects:** Group tasks under named projects. A command like `task list --project "Final Project"` would show all related tasks.
* **Dependencies:** Allow a task to depend on another. You can't start designing the UI until you've finished the user research.
* **Unique Feature:** **Knowledge Integration**. A command like `task link <task_id> --note <note_id>` could associate a task with a knowledge note. When you view the task, it could automatically show a summary of the linked note.

#### Terminal Chat Interface

Your interface is the heart of the project. Make it feel powerful and intuitive.

* **Simple Command Parser:** Start with a `verb + noun` structure.
    * `note create "My thoughts on AI agents"`
    * `task list --priority high`
    * `find "database schemas"` (searches both notes and tasks)
* **Natural Language Commands:** Use an LLM to interpret more flexible commands.
    * User types: `"remind me to email prof. smith tomorrow at 10am about the deadline"`
    * Your system parses this into: `task add "Email Prof. Smith about the deadline" --due 2025-10-09T10:00:00`
* **Context-Aware Prompt:** The prompt could show useful info, like the number of pending tasks: `(5 tasks due) >`

#### AI Agents 🤖

This is where you can get really creative. The agents should feel like they're augmenting your own intelligence.

1.  **The Connector Agent:** When you create a new note, this agent could scan it for keywords and suggest linking it to 3 other relevant notes that already exist in your PKMS.
2.  **The Planner Agent:** You give it a high-level goal, and it breaks it down into a list of actionable tasks.
    * User: `agent plan "Write a blog post about my final project"`
    * Agent creates tasks: "Outline blog post structure," "Write first draft," "Find relevant screenshots," "Edit and proofread," "Publish post."
3.  **The Summarizer Agent:** An agent that can generate a summary of your knowledge on a specific topic.
    * User: `agent summarize --tag "python"`
    * Agent responds: "You have 15 notes tagged with #python. Key themes include database interaction with SQLite, creating terminal interfaces, and using LLM APIs. You seem to be focused on practical application over theoretical concepts."

---

### ## Choosing Your Database

Your choice of data storage has a big impact on the project.

* **SQLite (Recommended):** This is the best of both worlds. It's a file-based database (so it's portable), but it gives you the power of SQL for complex queries. It's perfect for managing structured data like tasks and the relationships between notes.
* **JSON Documents:** Easiest to start with and great for prototyping. You can have a `notes` directory with `.json` files. However, searching and establishing complex relationships can become slow and complicated as your data grows.
* **Neo4j (Ambitious):** If you are passionate about the "linked" nature of your knowledge, a graph database is the ultimate choice. It's designed to manage complex relationships, making features like backlink analysis incredibly fast. This has a steeper learning curve but would be very impressive.

---

### ## A Possible Development Roadmap

Here’s a plan to get you from now until the deadline.

* **Weeks 1-2 (Now - Oct 20): Foundation.**
    * Set up your GitHub repo (`csc299-project`).
    * Choose your database (start with SQLite).
    * Define your data models for notes (ID, title, content, tags) and tasks (ID, description, due date, priority, status).
    * Build the basic Python functions to create, read, update, and delete notes and tasks from the database. **Forget the UI for now.**
* **Weeks 3-4 (Oct 21 - Nov 3): The Interface.**
    * Build the main terminal application loop that waits for user input.
    * Implement the simple command parser for your core CRUD functions (`note create`, `task list`, etc.).
* **Weeks 5-6 (Nov 4 - Nov 17): Integration & AI.**
    * Implement the linking features between notes and between tasks and notes.
    * Integrate with an LLM API (e.g., Google's Gemini API or OpenAI's API).
    * Create your first simple AI feature, like the **Summarizer Agent**.
* **Week 7 (Nov 18 - Nov 24): Polish and Demo.**
    * Build out another AI agent, like the **Planner Agent**.
    * Refine the user interface, add help commands, and fix bugs.
    * Record your 6-8 minute video demonstration and upload it to YouTube.
    * Finalize your `video.txt` and push all code to GitHub.
