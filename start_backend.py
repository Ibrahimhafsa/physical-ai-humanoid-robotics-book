#!/usr/bin/env python
"""
Simple wrapper to start FastAPI backend from any directory.
Adds repo root to Python path and starts Uvicorn.
"""

import sys
import os
from pathlib import Path

# Add repo root to Python path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

# Load environment variables from backend/.env
from dotenv import load_dotenv
env_file = repo_root / "backend" / ".env"
load_dotenv(env_file)
print(f"Loaded environment from: {env_file}")
print(f"COHERE_API_KEY present: {'COHERE_API_KEY' in os.environ}")
print(f"COHERE_MODEL: {os.getenv('COHERE_MODEL', 'not set')}")
print(f"QDRANT_URL: {os.getenv('QDRANT_URL', 'not set')}")

# Now run uvicorn
if __name__ == '__main__':
    import uvicorn

    print(f"Starting FastAPI backend from: {repo_root}")
    print(f"Python path includes: {sys.path[0]}")

    uvicorn.run(
        "backend.src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(repo_root / "backend")]
    )
