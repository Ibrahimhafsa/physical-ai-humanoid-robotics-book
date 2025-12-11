"""Book Embedding Pipeline - Automated crawling, extraction, embedding, and storage."""

__version__ = "0.1.0"
__author__ = "AI & Physical Robotics Book Project"

from src.config import Settings, load_settings
from src.models import Chunk, IngestionLog, Page, Vector

__all__ = [
    "Settings",
    "load_settings",
    "Page",
    "Chunk",
    "Vector",
    "IngestionLog",
]
