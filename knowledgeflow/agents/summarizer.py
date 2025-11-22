"""
Summarizer Agent
Uses OpenAI GPT-4o to summarize notes and tasks
"""

import os
from typing import Optional
from openai import OpenAI


class SummarizerAgent:
    """AI agent that summarizes text using GPT-4o"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the summarizer with OpenAI API key"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"
    
    def summarize_text(self, text: str, max_words: int = 30) -> str:
        """
        Summarize text to a concise summary
        
        Args:
            text: The text to summarize
            max_words: Maximum words in summary (default: 30)
        
        Returns:
            Summarized text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "developer",
                        "content": f"You are a summarization expert. Summarize the following text into approximately {max_words} words or less. Be concise and capture the key points."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this text:\n\n{text}"
                    }
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        
        except Exception as e:
            return f"Error summarizing: {str(e)}"
    
    def summarize_note(self, note: dict, max_words: int = 30) -> str:
        """
        Summarize a note dictionary
        
        Args:
            note: Note dictionary with 'title' and 'content'
            max_words: Maximum words in summary
        
        Returns:
            Summary of the note
        """
        text = f"Title: {note.get('title', '')}\nContent: {note.get('content', '')}"
        return self.summarize_text(text, max_words)
    
    def summarize_task(self, task: dict, max_words: int = 30) -> str:
        """
        Summarize a task dictionary
        
        Args:
            task: Task dictionary with 'title' and 'description'
            max_words: Maximum words in summary
        
        Returns:
            Summary of the task
        """
        text = f"Task: {task.get('title', '')}\nDescription: {task.get('description', '')}"
        if task.get('status'):
            text += f"\nStatus: {task['status']}"
        if task.get('priority'):
            text += f"\nPriority: {task['priority']}"
        
        return self.summarize_text(text, max_words)
    
    def batch_summarize(self, items: list, item_type: str = "note", max_words: int = 30) -> dict:
        """
        Summarize multiple items
        
        Args:
            items: List of note or task dictionaries
            item_type: Either 'note' or 'task'
            max_words: Maximum words per summary
        
        Returns:
            Dictionary mapping item IDs to summaries
        """
        summaries = {}
        
        for item in items:
            item_id = item.get('id')
            if not item_id:
                continue
            
            if item_type == "note":
                summaries[item_id] = self.summarize_note(item, max_words)
            elif item_type == "task":
                summaries[item_id] = self.summarize_task(item, max_words)
        
        return summaries
    
    def generate_title(self, content: str, max_words: int = 5) -> str:
        """
        Generate a concise title from content
        
        Args:
            content: The content to generate title from
            max_words: Maximum words in title (default: 5)
        
        Returns:
            Generated title
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "developer",
                        "content": f"You are a title generator. Generate a concise title of {max_words} words or less that captures the essence of the text."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a title for:\n\n{content}"
                    }
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            title = response.choices[0].message.content.strip()
            # Remove quotes if present
            title = title.strip('"\'')
            return title
        
        except Exception as e:
            return f"Error generating title: {str(e)}"
