"""
Models package for RAG Agent API and Pipeline

This package bridges the gap between:
- Pipeline models (Chunk, Page, Vector, etc.) from ../models.py
- API models (ChatRequest, ChatResponse, etc.) from ./chat.py
"""

import sys
from pathlib import Path

# Handle circular import: add parent directory to path to import parent models.py
parent_src = Path(__file__).parent.parent
if str(parent_src) not in sys.path:
    sys.path.insert(0, str(parent_src))

# Import pipeline models (these need to come from models.py in parent directory)
# We need to be careful here - when this __init__ is imported, we want to expose
# the classes from ../models.py

def __getattr__(name):
    """Lazy load models from parent models.py or chat.py"""
    if name in ['Chunk', 'Page', 'Vector', 'IngestionLog', 'IngestionLogSummary', 'IngestionLogPerformance', 'IngestionLogAPIUsage']:
        # Load from parent models.py
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("parent_models", Path(__file__).parent.parent / "models.py")
            parent_models = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(parent_models)
            return getattr(parent_models, name)
        except Exception:
            raise AttributeError(f"module 'src.models' has no attribute '{name}'")
    elif name in ['ChatRequest', 'ChatResponse', 'ErrorResponse', 'ErrorDetail']:
        # Load from chat.py
        try:
            from .chat import (
                ChatRequest,
                ChatResponse,
                ErrorResponse,
                ErrorDetail,
            )
            return {'ChatRequest': ChatRequest, 'ChatResponse': ChatResponse, 'ErrorResponse': ErrorResponse, 'ErrorDetail': ErrorDetail}[name]
        except ImportError:
            raise AttributeError(f"module 'src.models' has no attribute '{name}'")
    raise AttributeError(f"module 'src.models' has no attribute '{name}'")

__all__ = [
    'ChatRequest',
    'ChatResponse',
    'ErrorResponse',
    'ErrorDetail',
    'Chunk',
    'Page',
    'Vector',
    'IngestionLog',
    'IngestionLogSummary',
    'IngestionLogPerformance',
    'IngestionLogAPIUsage',
]
