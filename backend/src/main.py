"""CLI entry point for Book Embedding Pipeline."""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from src.config import load_settings
from src.logger import setup_logging
from src.pipeline import EmbeddingPipeline


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Automated pipeline for crawling, extracting, embedding, and storing book content in Qdrant"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without API calls (crawl and extract only)",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum pages to process (None = all pages)",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from checkpoint if available",
    )

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config file (optional)",
    )

    parser.add_argument(
        "--test-search",
        type=str,
        default=None,
        help="Test similarity search with a query",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    # Load settings
    try:
        config = load_settings()
        if args.max_pages:
            config.max_pages = args.max_pages
        if args.log_level:
            config.log_level = args.log_level
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        print("Make sure .env file exists with required variables", file=sys.stderr)
        sys.exit(1)

    # Setup logging
    logger = setup_logging(
        name="book-embeddings",
        level=config.log_level,
        log_dir=config.output_dir,
    )

    logger.info("Book Embedding Pipeline")
    logger.info(f"Book URL: {config.book_root_url}")
    logger.info(f"Qdrant Collection: {config.qdrant_collection}")

    # Run pipeline
    pipeline = EmbeddingPipeline(config)

    try:
        log = await pipeline.run(
            resume=args.resume,
            dry_run=args.dry_run,
        )

        # Save log to file
        log_file = Path(config.output_dir) / "ingestion_log.json"
        with open(log_file, "w") as f:
            json.dump(log.model_dump(), f, indent=2, default=str)

        # Print summary
        print("\n" + "=" * 60)
        print("EMBEDDING PIPELINE SUMMARY")
        print("=" * 60)
        print(f"URLs Discovered: {log.summary.urls_discovered}")
        print(f"URLs Fetched: {log.summary.urls_fetched}")
        print(f"URLs Failed: {log.summary.urls_failed}")
        print(f"Chunks Created: {log.summary.chunks_created}")
        print(f"Chunks Deduplicated: {log.summary.chunks_deduplicated}")
        print(f"Chunks Embedded: {log.summary.chunks_embedded}")
        print(f"Vectors Stored: {log.summary.vectors_stored}")
        print(f"Total Time: {log.performance.total_time_seconds:.2f}s")
        print(f"Log saved to: {log_file}")
        print("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
