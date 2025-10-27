#!/usr/bin/env python3
"""
Experiment 2: OpenAI API Testing
Quick test of OpenAI integration before adding to main codebase

To use this:
1. Get an API key from https://platform.openai.com/api-keys
2. Create a .env file in tasks2/ with: OPENAI_API_KEY=your-key-here
3. Run this script!
"""

import os
from pathlib import Path

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
    print("✅ dotenv loaded")
except ImportError:
    print("⚠️  python-dotenv not installed (pip3 install python-dotenv)")
    print("   You can still set OPENAI_API_KEY environment variable manually")

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n❌ No API key found!")
    print("\nTo set up:")
    print("1. Create a file: tasks2/.env")
    print("2. Add: OPENAI_API_KEY=sk-your-key-here")
    print("3. Run this script again")
    exit(1)

# Try OpenAI
try:
    from openai import OpenAI
    print("✅ OpenAI library installed")
    client = OpenAI(api_key=api_key)
except ImportError:
    print("❌ OpenAI library not installed")
    print("Install with: pip3 install openai")
    exit(1)

def test_simple_completion():
    """Test basic completion"""
    print("\n" + "="*60)
    print("🤖 Testing Simple Completion")
    print("="*60)
    
    prompt = "Suggest 3 tags for a note about Python programming. Return only comma-separated tags."
    
    print(f"\n📝 Prompt: {prompt}")
    print("\n⏳ Calling OpenAI...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful tagging assistant. Be concise."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        print(f"\n✅ Response: {result}")
        print(f"📊 Tokens used: {tokens_used}")
        print(f"💰 Estimated cost: ${tokens_used * 0.00000015:.6f}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_auto_tagging():
    """Test automatic tagging feature"""
    print("\n" + "="*60)
    print("🏷️  Testing Auto-Tagging")
    print("="*60)
    
    note_title = "Machine Learning Basics"
    note_content = "Introduction to neural networks, supervised learning, and deep learning frameworks like PyTorch and TensorFlow."
    
    print(f"\n📄 Note: {note_title}")
    print(f"📝 Content: {note_content[:100]}...")
    
    prompt = f"""
    Analyze this note and suggest 3-5 relevant tags.
    
    Title: {note_title}
    Content: {note_content}
    
    Return ONLY comma-separated tags in lowercase.
    """
    
    print("\n⏳ Generating tags...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a tagging expert. Return only comma-separated tags."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        
        tags = response.choices[0].message.content.strip()
        print(f"\n✅ Suggested tags: {tags}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_task_breakdown():
    """Test breaking down a task into subtasks"""
    print("\n" + "="*60)
    print("📋 Testing Task Breakdown")
    print("="*60)
    
    task = "Build a personal knowledge management system"
    
    print(f"\n🎯 Task: {task}")
    
    prompt = f"""
    Break this task into 4-5 smaller, actionable subtasks:
    
    Task: {task}
    
    Return a numbered list of subtasks. Be specific and actionable.
    """
    
    print("\n⏳ Breaking down task...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a productivity coach. Be concise and actionable."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        subtasks = response.choices[0].message.content
        print(f"\n✅ Subtasks:\n{subtasks}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_embeddings():
    """Test embeddings for semantic search"""
    print("\n" + "="*60)
    print("🔍 Testing Embeddings (for Semantic Search)")
    print("="*60)
    
    texts = [
        "Python is a programming language",
        "Django is a web framework",
        "Cats are cute animals"
    ]
    
    print("\n📝 Sample texts:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")
    
    print("\n⏳ Generating embeddings...")
    
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        embeddings = [item.embedding for item in response.data]
        
        print(f"\n✅ Generated {len(embeddings)} embeddings")
        print(f"📊 Embedding dimension: {len(embeddings[0])}")
        print(f"💰 Estimated cost: ${response.usage.total_tokens * 0.00000002:.8f}")
        
        # Calculate similarity between first two
        import numpy as np
        vec1 = np.array(embeddings[0])
        vec2 = np.array(embeddings[1])
        vec3 = np.array(embeddings[2])
        
        similarity_12 = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        similarity_13 = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))
        
        print(f"\n🔗 Similarity:")
        print(f"  Text 1 ↔ Text 2 (related): {similarity_12:.4f}")
        print(f"  Text 1 ↔ Text 3 (unrelated): {similarity_13:.4f}")
        print(f"\n💡 Higher similarity = more related content!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 OpenAI API Experiments")
    print("="*70)
    print(f"\n🔑 API Key: {api_key[:20]}...{api_key[-4:]}")
    
    try:
        test_simple_completion()
        test_auto_tagging()
        test_task_breakdown()
        
        # Only test embeddings if numpy is available
        try:
            import numpy
            test_embeddings()
        except ImportError:
            print("\n⚠️  Skipping embeddings test (numpy not installed)")
        
        print("\n" + "="*70)
        print("✅ All tests complete!")
        print("="*70)
        print("\n💡 These features are ready to integrate into KnowledgeFlow!")
        
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")

if __name__ == "__main__":
    main()
