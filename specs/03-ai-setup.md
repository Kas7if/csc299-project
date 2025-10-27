# Specification: AI Integration Setup

**Version:** 1.0  
**Date:** October 27, 2025  
**Phase:** 2.1

## Overview
Set up AI integration infrastructure to enable natural language processing, smart agents, and semantic search.

## Goals
1. Configure API access (OpenAI or Anthropic)
2. Secure API key management
3. Error handling and rate limiting
4. Token usage tracking
5. Fallback for when AI is unavailable

## Provider Choice

**Recommendation: OpenAI**
- Reason: Better embeddings for semantic search
- Cost: ~$0.0001 per 1K tokens (GPT-4o-mini)
- Embeddings: $0.00002 per 1K tokens

**Alternative: Anthropic Claude**
- Better for complex reasoning
- Cost: ~$0.00015 per 1K tokens (Haiku)
- No embeddings API (would need separate solution)

**Decision:** Use OpenAI for Phase 2, can add Anthropic later

## Dependencies

```txt
openai>=1.0.0
python-dotenv>=1.0.0
tiktoken>=0.5.0  # Token counting
```

## Configuration

### Environment Variables (.env)
```bash
# API Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Rate Limiting
MAX_TOKENS_PER_REQUEST=4000
MAX_REQUESTS_PER_MINUTE=60

# Features
ENABLE_AI=true
ENABLE_SEMANTIC_SEARCH=true
ENABLE_AUTO_TAGGING=true
```

### Configuration File (config/settings.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Rate Limiting
    MAX_TOKENS = int(os.getenv("MAX_TOKENS_PER_REQUEST", "4000"))
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
    
    # Features
    ENABLE_AI = os.getenv("ENABLE_AI", "true").lower() == "true"
    ENABLE_SEMANTIC_SEARCH = os.getenv("ENABLE_SEMANTIC_SEARCH", "true").lower() == "true"
    
    @classmethod
    def is_configured(cls):
        """Check if AI is properly configured"""
        return cls.OPENAI_API_KEY is not None and cls.ENABLE_AI

settings = Settings()
```

## AI Client Architecture

### Base AI Client (`core/ai_client.py`)

```python
from openai import OpenAI
from typing import Optional, List
import tiktoken
from config.settings import settings

class AIClient:
    def __init__(self):
        self.client = None
        self.encoding = None
        self._initialize()
    
    def _initialize(self):
        """Initialize OpenAI client"""
        if settings.is_configured():
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.encoding = tiktoken.encoding_for_model(settings.OPENAI_MODEL)
    
    def is_available(self) -> bool:
        """Check if AI is available"""
        return self.client is not None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if not self.encoding:
            return len(text) // 4  # Rough estimate
        return len(self.encoding.encode(text))
    
    def complete(self, prompt: str, system: str = None, max_tokens: int = 1000) -> Optional[str]:
        """Get completion from AI"""
        if not self.is_available():
            return None
        
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"AI Error: {e}")
            return None
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding vector for text"""
        if not self.is_available():
            return None
        
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        
        except Exception as e:
            print(f"Embedding Error: {e}")
            return None
    
    def batch_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Get embeddings for multiple texts"""
        if not self.is_available():
            return [None] * len(texts)
        
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=texts
            )
            return [item.embedding for item in response.data]
        
        except Exception as e:
            print(f"Batch Embedding Error: {e}")
            return [None] * len(texts)

# Singleton instance
ai_client = AIClient()
```

## Rate Limiting

### Rate Limiter (`core/rate_limiter.py`)

```python
import time
from collections import deque
from config.settings import settings

class RateLimiter:
    def __init__(self, max_per_minute: int = None):
        self.max_per_minute = max_per_minute or settings.MAX_REQUESTS_PER_MINUTE
        self.requests = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        minute_ago = now - 60
        
        # Remove requests older than 1 minute
        while self.requests and self.requests[0] < minute_ago:
            self.requests.popleft()
        
        # Check if we're at the limit
        if len(self.requests) >= self.max_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.requests.append(now)

rate_limiter = RateLimiter()
```

## Error Handling

### AI Exception Classes

```python
class AIException(Exception):
    """Base exception for AI errors"""
    pass

class AINotAvailableException(AIException):
    """AI is not configured or available"""
    pass

class AIRateLimitException(AIException):
    """Rate limit exceeded"""
    pass

class AIAPIException(AIException):
    """API error occurred"""
    pass
```

## Setup Commands

Add CLI commands for AI configuration:

```bash
# Check AI status
ai status

# Test AI connection
ai test

# Show token usage
ai usage

# Configure AI
ai setup
```

## Database Extensions

Add table for tracking AI usage:

```sql
CREATE TABLE ai_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL,  -- 'completion', 'embedding', etc.
    tokens_used INTEGER,
    cost REAL,
    timestamp TEXT NOT NULL
);
```

## Testing Requirements

### Unit Tests
- [ ] Test AI client initialization
- [ ] Test completion with/without API key
- [ ] Test embedding generation
- [ ] Test rate limiting
- [ ] Test error handling
- [ ] Test token counting

### Integration Tests
- [ ] Test full AI workflow
- [ ] Test graceful degradation (AI unavailable)
- [ ] Test configuration validation

## Security Considerations

1. **Never commit API keys** - Use .env (already in .gitignore)
2. **Validate inputs** - Sanitize before sending to API
3. **Token limits** - Prevent excessive costs
4. **Error messages** - Don't leak API keys in errors

## Cost Management

### Token Budget
- Development: ~$5 budget
- Estimated usage:
  - 100 completions/day × 500 tokens = 50K tokens = $0.005/day
  - 50 embeddings/day × 100 tokens = 5K tokens = $0.0001/day
  - Monthly: ~$0.15

### Usage Tracking

```python
def track_usage(operation: str, tokens: int):
    """Track AI usage in database"""
    cost = calculate_cost(operation, tokens)
    # Store in ai_usage table
```

## Fallback Behavior

When AI is unavailable:
- Natural language commands → Show suggested exact commands
- Auto-tagging → Skip, user tags manually
- Semantic search → Fall back to keyword search
- Link suggestions → Skip

## File Structure

```
knowledgeflow/
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration management
├── core/
│   ├── ai_client.py        # OpenAI client wrapper
│   ├── rate_limiter.py     # Rate limiting
│   └── exceptions.py       # AI exceptions
└── .env.example            # Example environment file
```

## Success Criteria
- ✅ AI client properly initialized
- ✅ API key securely managed
- ✅ Rate limiting works
- ✅ Error handling is robust
- ✅ Token usage tracked
- ✅ Graceful degradation when AI unavailable
- ✅ All tests pass

## Implementation Order
1. Create config system
2. Implement AI client
3. Add rate limiting
4. Add error handling
5. Add usage tracking
6. Add CLI commands for AI management
7. Tests

---
**Previous Spec:** `02-cli-interface.md`  
**Next Spec:** `04-ai-agents.md`
