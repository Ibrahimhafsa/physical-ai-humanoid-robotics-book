#!/usr/bin/env python
"""Wrapper to run embedding pipeline with proper module path setup."""

import sys
import os
from pathlib import Path

# Add repo root to Python path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "backend"))

# Load environment variables
from dotenv import load_dotenv
env_file = repo_root / "backend" / ".env"
load_dotenv(env_file)

# Change to backend directory so relative imports work
os.chdir(str(repo_root / "backend"))

# Now run the embedding pipeline
if __name__ == '__main__':
    import asyncio
    from src.main import main

    asyncio.run(main())
