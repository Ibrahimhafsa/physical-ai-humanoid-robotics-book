"""Generate and manage ingestion logs."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from src.models import IngestionLog


class IngestionLogGenerator:
    """Generate ingestion logs for pipeline runs."""

    def __init__(self, output_dir: str = "./embeddings_output"):
        """Initialize log generator.

        Args:
            output_dir: Directory for output logs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_log(self, log: IngestionLog, filename: str = "ingestion_log.json"):
        """Save ingestion log to JSON file.

        Args:
            log: IngestionLog object to save
            filename: Output filename
        """
        log_file = self.output_dir / filename
        with open(log_file, "w") as f:
            json.dump(log.model_dump(), f, indent=2, default=str)

    def load_log(self, filename: str = "ingestion_log.json") -> IngestionLog:
        """Load ingestion log from JSON file.

        Args:
            filename: Log filename to load

        Returns:
            Loaded IngestionLog object
        """
        log_file = self.output_dir / filename
        with open(log_file, "r") as f:
            data = json.load(f)
        return IngestionLog(**data)

    def save_chunks_log(self, chunks: List[Dict], filename: str = "chunks.json"):
        """Save processed chunks to JSON file.

        Args:
            chunks: List of chunk dictionaries
            filename: Output filename
        """
        log_file = self.output_dir / filename
        with open(log_file, "w") as f:
            json.dump(chunks, f, indent=2, default=str)

    def save_urls_log(self, urls: List[str], filename: str = "urls.json"):
        """Save crawled URLs to JSON file.

        Args:
            urls: List of crawled URLs
            filename: Output filename
        """
        log_file = self.output_dir / filename
        with open(log_file, "w") as f:
            json.dump({"urls": urls, "count": len(urls)}, f, indent=2, default=str)

    def print_summary(self, log: IngestionLog):
        """Print pipeline summary to stdout.

        Args:
            log: IngestionLog to summarize
        """
        print("\n" + "=" * 70)
        print("EMBEDDING PIPELINE SUMMARY")
        print("=" * 70)
        print(f"Run ID:                 {log.run_id}")
        print(f"Book URL:               {log.book_root_url}")
        print(f"Qdrant Collection:      {log.qdrant_collection}")
        print(f"Started at:             {log.started_at.isoformat()}")
        print(f"Completed at:           {log.completed_at.isoformat()}")
        print(f"Total Duration:         {log.performance.total_time_seconds:.2f}s")
        print()
        print("CRAWLING & EXTRACTION")
        print(f"  URLs Discovered:      {log.summary.urls_discovered}")
        print(f"  URLs Fetched:         {log.summary.urls_fetched}")
        print(f"  URLs Failed:          {log.summary.urls_failed}")
        print()
        print("CHUNKING & DEDUPLICATION")
        print(f"  Chunks Created:       {log.summary.chunks_created}")
        print(f"  Chunks Deduplicated:  {log.summary.chunks_deduplicated}")
        print(f"  Unique Chunks:        {log.summary.chunks_created - log.summary.chunks_deduplicated}")
        print()
        print("EMBEDDING & STORAGE")
        print(f"  Chunks Embedded:      {log.summary.chunks_embedded}")
        print(f"  Vectors Stored:       {log.summary.vectors_stored}")
        print()
        print("API USAGE")
        print(f"  Cohere API Calls:     {log.api_usage.cohere_api_calls}")
        print(f"  Cohere Tokens Used:   {log.api_usage.cohere_tokens_used}")
        print(f"  Qdrant Upserts:       {log.api_usage.qdrant_upserts}")
        print()
        if log.errors:
            print("ERRORS")
            for error in log.errors:
                print(f"  - {error.url}: {error.error_type} - {error.message}")
        print("=" * 70 + "\n")
