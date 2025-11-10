#!/usr/bin/env python3
"""
Tasks4: OpenAI Chat Completions API Experiment
Summarizes paragraph-length task descriptions into clear summaries using GPT-4o
"""

import os
from openai import OpenAI


# Sample paragraph-length task descriptions
SAMPLE_TASKS = [
    """
    I need to complete my CSC299 final project which includes finishing all the remaining tasks 
    including tasks4, tasks5, and tasks6. Each task requires setting up a new Python package with uv, 
    implementing the core functionality, writing comprehensive tests, and documenting everything properly. 
    The project is due on November 24th, and I also need to make sure all my previous tasks are working 
    correctly and integrated properly. This also involves learning new APIs like OpenAI and potentially 
    setting up AI agents for automation. I should allocate at least 3-4 hours per task and make sure 
    to test everything thoroughly before submission.
    """,
    
    """
    Study for the upcoming database systems midterm exam scheduled for November 15th. This includes 
    reviewing all lecture notes from weeks 1 through 8, practicing SQL queries especially joins and 
    subqueries, understanding normalization forms (1NF through BCNF), and working through the practice 
    problems provided by the professor. I also need to review transaction management, ACID properties, 
    and indexing strategies. The exam will be 2 hours long and cover both theoretical concepts and 
    practical SQL coding. I should create a study guide summarizing key concepts and spend at least 
    2 hours practicing SQL queries on the provided database samples.
    """,
    
    """
    Organize my computer files and backup system before the end of the semester. This involves going 
    through all my Downloads folder and sorting files into appropriate directories, cleaning up my 
    Desktop which has accumulated various screenshots and documents, setting up an automated backup 
    system using Time Machine or cloud storage for important school work, organizing my code projects 
    into a proper GitHub repository structure with good README files, and deleting old virtual 
    environments and cached files that are taking up disk space. I should also archive completed course 
    materials from previous semesters and ensure all my current coursework is properly organized and 
    easily accessible.
    """
]


def summarize_task(client: OpenAI, task_description: str) -> str:
    """
    Use OpenAI Chat Completions API to summarize a task description into a short phrase.
    
    Args:
        client: OpenAI client instance
        task_description: Paragraph-length task description
        
    Returns:
        Short phrase summary of the task
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "developer",
                    "content": "You are a helpful assistant that summarizes task descriptions into clear, concise summaries (15-25 words). Include the main action, key objectives, and important deadlines or details."
                },
                {
                    "role": "user",
                    "content": f"Summarize this task into a clear, detailed summary:\n\n{task_description}"
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main function to summarize multiple task descriptions."""
    
    print("=" * 80)
    print("🤖 Tasks4: OpenAI Task Summarizer")
    print("=" * 80)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ Error: OPENAI_API_KEY environment variable not set!")
        print("Please set your API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    print(f"\n✅ OpenAI client initialized")
    print(f"📝 Processing {len(SAMPLE_TASKS)} task descriptions...\n")
    
    # Process each task description
    summaries = []
    for i, task_desc in enumerate(SAMPLE_TASKS, 1):
        print(f"\n{'─' * 80}")
        print(f"Task #{i}:")
        print(f"{'─' * 80}")
        
        # Show original (truncated for display)
        original = task_desc.strip()
        print(f"\n📄 Original ({len(original)} characters):")
        print(f"   {original[:100]}...")
        
        # Get summary from OpenAI
        print(f"\n🔄 Summarizing with GPT-4o...")
        summary = summarize_task(client, task_desc)
        summaries.append(summary)
        
        print(f"✨ Summary: {summary}")
    
    # Print all summaries at the end
    print(f"\n{'═' * 80}")
    print("📋 All Summaries:")
    print(f"{'═' * 80}")
    for i, summary in enumerate(summaries, 1):
        print(f"  {i}. {summary}")
    
    print(f"\n✅ Done! Summarized {len(summaries)} tasks.\n")


if __name__ == "__main__":
    main()
