# Specification: AI Agents

**Version:** 1.0  
**Date:** October 27, 2025  
**Phase:** 2.2 - 3.1

## Overview
Implement autonomous AI agents that analyze and enhance your knowledge base and tasks automatically.

## Goals
1. Create at least 3 functional AI agents
2. Agents run automatically or on-demand
3. Improve user productivity
4. Learn from user behavior
5. Provide actionable insights

## Agent Architecture

### Base Agent Class (`agents/base_agent.py`)

```python
from abc import ABC, abstractmethod
from core.ai_client import ai_client
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True
    
    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent with given context"""
        pass
    
    def is_available(self) -> bool:
        """Check if agent can run"""
        return self.enabled and ai_client.is_available()
    
    def log_action(self, action: str, details: str):
        """Log agent actions"""
        # Store in database for audit trail
        pass
```

## Agent 1: Smart Tagger

**Purpose:** Automatically suggest tags for notes based on content

### Implementation (`agents/tagger_agent.py`)

```python
from agents.base_agent import BaseAgent
from core.ai_client import ai_client

class TaggerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Smart Tagger",
            description="Suggests relevant tags for your notes"
        )
    
    def run(self, context):
        """
        context: {
            'note_id': int,
            'title': str,
            'content': str,
            'existing_tags': List[str]
        }
        """
        note_id = context['note_id']
        title = context['title']
        content = context['content']
        existing_tags = context.get('existing_tags', [])
        
        # Get all existing tags in the system for context
        all_tags = self._get_all_tags()
        
        prompt = f"""
        Analyze this note and suggest 3-5 relevant tags.
        
        Title: {title}
        Content: {content[:500]}
        
        Existing tags in system: {', '.join(all_tags[:20])}
        Current tags: {', '.join(existing_tags)}
        
        Suggest new tags that:
        1. Are concise (1-2 words)
        2. Are lowercase
        3. Match existing tag style if possible
        4. Are relevant to content
        
        Return ONLY comma-separated tags, nothing else.
        """
        
        response = ai_client.complete(
            prompt=prompt,
            system="You are a helpful tagging assistant. Be concise."
        )
        
        if response:
            suggested_tags = [tag.strip().lower() for tag in response.split(',')]
            # Filter out existing tags
            new_tags = [tag for tag in suggested_tags if tag not in existing_tags]
            
            self.log_action("suggest_tags", f"Note {note_id}: {', '.join(new_tags)}")
            
            return {
                'success': True,
                'suggested_tags': new_tags[:5],
                'note_id': note_id
            }
        
        return {'success': False, 'error': 'AI unavailable'}
    
    def _get_all_tags(self):
        """Get all tags from database"""
        # Query database for existing tags
        pass
```

### Usage

```python
# Automatic when creating notes
tagger = TaggerAgent()
result = tagger.run({
    'note_id': 1,
    'title': 'Machine Learning Basics',
    'content': 'Introduction to neural networks...',
    'existing_tags': []
})

if result['success']:
    print(f"Suggested tags: {', '.join(result['suggested_tags'])}")
    # Ask user if they want to apply tags
```

## Agent 2: Link Suggester

**Purpose:** Suggest connections between related notes

### Implementation (`agents/linker_agent.py`)

```python
from agents.base_agent import BaseAgent
from core.ai_client import ai_client
import numpy as np

class LinkerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Link Suggester",
            description="Finds related notes and suggests links"
        )
    
    def run(self, context):
        """
        context: {
            'note_id': int,
            'title': str,
            'content': str,
            'all_notes': List[Dict]  # Other notes in system
        }
        """
        note_id = context['note_id']
        content = context['content']
        all_notes = context['all_notes']
        
        # Get embedding for current note
        note_embedding = ai_client.get_embedding(content)
        if not note_embedding:
            return {'success': False, 'error': 'AI unavailable'}
        
        # Calculate similarity with other notes
        similarities = []
        for other_note in all_notes:
            if other_note['id'] == note_id:
                continue
            
            other_embedding = other_note.get('embedding')
            if not other_embedding:
                # Generate embedding if not exists
                other_embedding = ai_client.get_embedding(other_note['content'])
            
            if other_embedding:
                similarity = self._cosine_similarity(note_embedding, other_embedding)
                similarities.append({
                    'note_id': other_note['id'],
                    'title': other_note['title'],
                    'similarity': similarity
                })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Take top 5
        suggested_links = similarities[:5]
        
        self.log_action("suggest_links", f"Note {note_id}: {len(suggested_links)} suggestions")
        
        return {
            'success': True,
            'suggested_links': suggested_links,
            'note_id': note_id
        }
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

## Agent 3: Task Assistant

**Purpose:** Analyze tasks and provide productivity insights

### Implementation (`agents/task_agent.py`)

```python
from agents.base_agent import BaseAgent
from core.ai_client import ai_client
from datetime import datetime, timedelta

class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Task Assistant",
            description="Analyzes tasks and provides productivity insights"
        )
    
    def run(self, context):
        """
        context: {
            'tasks': List[Dict]  # All tasks
        }
        """
        tasks = context['tasks']
        
        # Analyze tasks
        overdue = self._get_overdue_tasks(tasks)
        high_priority = self._get_high_priority_tasks(tasks)
        completed_today = self._get_completed_today(tasks)
        
        # Generate insights with AI
        prompt = f"""
        Analyze these task statistics and provide 3 actionable insights:
        
        - Overdue tasks: {len(overdue)}
        - High priority pending: {len(high_priority)}
        - Completed today: {len(completed_today)}
        - Total pending: {sum(1 for t in tasks if t['status'] == 'pending')}
        
        Task samples:
        {self._format_tasks(tasks[:10])}
        
        Provide:
        1. Most urgent priority
        2. Productivity tip
        3. Task organization suggestion
        
        Be brief and actionable.
        """
        
        response = ai_client.complete(
            prompt=prompt,
            system="You are a productivity coach. Be concise and helpful."
        )
        
        return {
            'success': True,
            'insights': response,
            'stats': {
                'overdue': len(overdue),
                'high_priority': len(high_priority),
                'completed_today': len(completed_today)
            }
        }
    
    def suggest_priorities(self, tasks):
        """Suggest priority changes for tasks"""
        # Analyze task content and suggest priority adjustments
        pass
    
    def break_down_task(self, task):
        """Break a large task into subtasks"""
        prompt = f"""
        Break this task into 3-5 smaller, actionable subtasks:
        
        Task: {task['title']}
        Description: {task.get('description', 'N/A')}
        
        Return numbered list of subtasks.
        """
        
        response = ai_client.complete(prompt=prompt)
        return response
    
    def _get_overdue_tasks(self, tasks):
        """Get overdue tasks"""
        now = datetime.now()
        return [t for t in tasks if t.get('due_date') and datetime.fromisoformat(t['due_date']) < now and t['status'] == 'pending']
    
    def _get_high_priority_tasks(self, tasks):
        """Get high priority pending tasks"""
        return [t for t in tasks if t['priority'] == 'high' and t['status'] == 'pending']
    
    def _get_completed_today(self, tasks):
        """Get tasks completed today"""
        today = datetime.now().date().isoformat()
        return [t for t in tasks if t.get('completed_at', '').startswith(today)]
    
    def _format_tasks(self, tasks):
        """Format tasks for prompt"""
        return '\n'.join([f"- [{t['priority']}] {t['title']}" for t in tasks])
```

## Agent Manager

Central manager for all agents (`agents/manager.py`):

```python
from agents.tagger_agent import TaggerAgent
from agents.linker_agent import LinkerAgent
from agents.task_agent import TaskAgent

class AgentManager:
    def __init__(self):
        self.agents = {
            'tagger': TaggerAgent(),
            'linker': LinkerAgent(),
            'task': TaskAgent()
        }
    
    def get_agent(self, name: str):
        """Get agent by name"""
        return self.agents.get(name)
    
    def run_agent(self, agent_name: str, context):
        """Run specific agent"""
        agent = self.get_agent(agent_name)
        if agent and agent.is_available():
            return agent.run(context)
        return {'success': False, 'error': 'Agent not available'}
    
    def list_agents(self):
        """List all available agents"""
        return [
            {
                'name': name,
                'description': agent.description,
                'available': agent.is_available()
            }
            for name, agent in self.agents.items()
        ]

agent_manager = AgentManager()
```

## CLI Commands

```bash
# List agents
agents

# Run specific agent
agent tagger --note 1
agent linker --note 1
agent task

# Get task insights
task insights

# Suggest tags for note
note tag-suggest 1

# Find related notes
note find-related 1

# Break down complex task
task breakdown 5
```

## Database Schema for Agents

```sql
-- Agent activity log
CREATE TABLE agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    timestamp TEXT NOT NULL
);

-- Note embeddings (for link suggester)
CREATE TABLE note_embeddings (
    note_id INTEGER PRIMARY KEY,
    embedding BLOB NOT NULL,  -- Store as JSON or pickle
    updated_at TEXT NOT NULL,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);
```

## Automated Agent Runs

### Triggers
1. **After creating note** → Run tagger agent
2. **After creating note** → Run linker agent (if >10 notes)
3. **Daily at 9am** → Run task agent
4. **After completing task** → Update task insights

### Configuration

```python
# In settings.py
AUTO_TAG = True
AUTO_LINK = True
DAILY_TASK_INSIGHTS = True
```

## Testing Requirements

### Unit Tests
- [ ] Test each agent individually
- [ ] Test agent with/without AI
- [ ] Test agent manager
- [ ] Test error handling

### Integration Tests
- [ ] Test agent triggers
- [ ] Test agent logging
- [ ] Test multi-agent workflow

## Success Criteria
- ✅ At least 3 agents implemented
- ✅ Agents provide useful suggestions
- ✅ Agents can run automatically or on-demand
- ✅ Agent activity is logged
- ✅ Graceful degradation when AI unavailable
- ✅ All tests pass

## Implementation Order
1. Create base agent class
2. Implement tagger agent
3. Implement linker agent  
4. Implement task agent
5. Create agent manager
6. Add CLI commands
7. Add automated triggers
8. Tests

---
**Previous Spec:** `03-ai-setup.md`  
**Next Spec:** `05-semantic-search.md`
