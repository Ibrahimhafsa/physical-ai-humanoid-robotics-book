"""Content deduplication using SHA256 hashing."""

from typing import Dict, Set


class Deduplicator:
    """Detect duplicate chunks using content hash."""

    def __init__(self):
        """Initialize deduplicator with empty hash set."""
        self.seen_hashes: Set[str] = set()
        self.dedup_count = 0

    def is_duplicate(self, chunk_id: str) -> bool:
        """Check if chunk hash has been seen before.

        Args:
            chunk_id: SHA256 hash of normalized chunk text

        Returns:
            True if duplicate (hash seen before), False if new
        """
        if chunk_id in self.seen_hashes:
            self.dedup_count += 1
            return True
        return False

    def register_hash(self, chunk_id: str) -> None:
        """Register a chunk hash as seen.

        Args:
            chunk_id: SHA256 hash to register
        """
        self.seen_hashes.add(chunk_id)

    def get_report(self) -> Dict[str, int]:
        """Get deduplication statistics.

        Returns:
            Dictionary with dedup stats
        """
        total_seen = len(self.seen_hashes) + self.dedup_count
        dedup_rate = (
            (self.dedup_count / total_seen * 100) if total_seen > 0 else 0
        )

        return {
            "total_chunks_processed": total_seen,
            "unique_chunks": len(self.seen_hashes),
            "duplicates_found": self.dedup_count,
            "dedup_rate_percent": round(dedup_rate, 2),
        }

    def reset(self) -> None:
        """Reset deduplicator state."""
        self.seen_hashes.clear()
        self.dedup_count = 0
