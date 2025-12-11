"""Pipeline checkpoint management for resumable execution."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


class CheckpointManager:
    """Manage pipeline progress checkpoints for resumable execution."""

    def __init__(self, checkpoint_dir: str = "./embeddings_output"):
        """Initialize checkpoint manager.

        Args:
            checkpoint_dir: Directory to store checkpoint files
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = self.checkpoint_dir / "checkpoint.json"

        self.processed_urls: Set[str] = set()
        self.processed_chunk_ids: Set[str] = set()
        self.last_update = datetime.utcnow()

    def load_checkpoint(self) -> bool:
        """Load checkpoint from file if it exists.

        Returns:
            True if checkpoint loaded, False if not found
        """
        if not self.checkpoint_file.exists():
            return False

        try:
            with open(self.checkpoint_file, "r") as f:
                data = json.load(f)
                self.processed_urls = set(data.get("processed_urls", []))
                self.processed_chunk_ids = set(data.get("processed_chunk_ids", []))
                self.last_update = datetime.fromisoformat(
                    data.get("last_update", datetime.utcnow().isoformat())
                )
            return True
        except Exception:
            return False

    def save_checkpoint(self) -> None:
        """Save current checkpoint to file."""
        try:
            data = {
                "processed_urls": list(self.processed_urls),
                "processed_chunk_ids": list(self.processed_chunk_ids),
                "last_update": datetime.utcnow().isoformat(),
            }
            with open(self.checkpoint_file, "w") as f:
                json.dump(data, f, indent=2)
            self.last_update = datetime.utcnow()
        except Exception:
            pass

    def mark_url_processed(self, url: str) -> None:
        """Mark a URL as successfully processed.

        Args:
            url: URL that was processed
        """
        self.processed_urls.add(url)

    def is_url_processed(self, url: str) -> bool:
        """Check if URL was already processed.

        Args:
            url: URL to check

        Returns:
            True if URL was processed before
        """
        return url in self.processed_urls

    def mark_chunk_embedded(self, chunk_id: str) -> None:
        """Mark a chunk as successfully embedded and stored.

        Args:
            chunk_id: Chunk ID that was embedded
        """
        self.processed_chunk_ids.add(chunk_id)

    def is_chunk_embedded(self, chunk_id: str) -> bool:
        """Check if chunk was already embedded.

        Args:
            chunk_id: Chunk ID to check

        Returns:
            True if chunk was embedded before
        """
        return chunk_id in self.processed_chunk_ids

    def get_processed_urls(self) -> Set[str]:
        """Get set of all processed URLs.

        Returns:
            Set of processed URLs
        """
        return self.processed_urls.copy()

    def get_processed_chunk_ids(self) -> Set[str]:
        """Get set of all processed chunk IDs.

        Returns:
            Set of processed chunk IDs
        """
        return self.processed_chunk_ids.copy()

    def get_stats(self) -> Dict[str, int]:
        """Get checkpoint statistics.

        Returns:
            Dictionary with checkpoint stats
        """
        return {
            "processed_urls": len(self.processed_urls),
            "processed_chunks": len(self.processed_chunk_ids),
            "last_update": self.last_update.isoformat(),
        }

    def reset(self) -> None:
        """Clear all checkpoint data."""
        self.processed_urls.clear()
        self.processed_chunk_ids.clear()
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
