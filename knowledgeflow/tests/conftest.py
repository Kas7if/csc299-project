"""
Pytest configuration for knowledgeflow tests
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import from core and agents
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
