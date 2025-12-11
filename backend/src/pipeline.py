"""Main pipeline orchestrating the embedding workflow."""

import asyncio
import logging
import time
from datetime import datetime
from typing import List, Optional

from src.checkpoint import CheckpointManager
from src.chunker import TextChunker
from src.config import Settings
from src.crawler import DocosaurusCrawler
from src.deduplicator import Deduplicator
from src.embedder import CohereEmbedder
from src.extractor import TextExtractor
from src.models import IngestionLog, IngestionLogAPIUsage, IngestionLogPerformance, IngestionLogSummary
from src.storage import QdrantStorage


class EmbeddingPipeline:
    """Orchestrate the complete embedding pipeline."""

    def __init__(self, config: Settings):
        """Initialize pipeline with configuration.

        Args:
            config: Pipeline configuration settings
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        self.crawler = DocosaurusCrawler(str(config.book_root_url))
        self.extractor = TextExtractor()
        self.chunker = TextChunker()
        self.deduplicator = Deduplicator()
        self.embedder = CohereEmbedder(
            api_key=config.cohere_api_key,
            model=config.cohere_model,
            batch_size=config.batch_size,
        )
        self.storage = QdrantStorage(
            url=str(config.qdrant_url),
            api_key=config.qdrant_api_key,
            collection_name=config.qdrant_collection,
        )
        self.checkpoint = CheckpointManager(config.output_dir)

        # Statistics
        self.start_time: Optional[datetime] = None
        self.urls_discovered = 0
        self.urls_fetched = 0
        self.urls_failed = 0
        self.chunks_created = 0
        self.chunks_deduplicated = 0
        self.chunks_embedded = 0
        self.vectors_stored = 0

    async def run(self, resume: bool = False, dry_run: bool = False) -> IngestionLog:
        """Run the complete embedding pipeline.

        Args:
            resume: Resume from checkpoint if available
            dry_run: Run without API calls (crawl and extract only)

        Returns:
            Complete ingestion log
        """
        self.start_time = datetime.utcnow()
        start_time_seconds = time.time()

        try:
            self.logger.info("Starting embedding pipeline...")

            # Load checkpoint if resuming
            if resume:
                if self.checkpoint.load_checkpoint():
                    self.logger.info("Loaded checkpoint - resuming from last progress")
                else:
                    self.logger.info("No checkpoint found - starting fresh")

            # Create Qdrant collection
            if not dry_run:
                self.logger.info("Creating Qdrant collection if needed...")
                if not self.storage.create_collection_if_needed():
                    self.logger.error("Failed to create Qdrant collection")
                    raise RuntimeError("Failed to create Qdrant collection")

            # Discover URLs
            self.logger.info("Discovering URLs from sitemap...")
            urls = await self.crawler.discover_urls(
                max_pages=self.config.max_pages
            )
            self.urls_discovered = len(urls)
            self.logger.info(f"Discovered {self.urls_discovered} URLs")

            # Filter out already-processed URLs (if resuming)
            if resume:
                processed = self.checkpoint.get_processed_urls()
                urls = [u for u in urls if u not in processed]
                self.logger.info(f"Skipping {len(processed)} already-processed URLs, processing {len(urls)} new URLs")

            if not urls:
                self.logger.info("No new URLs to process")
                return self._create_log(start_time_seconds)

            # Fetch pages
            self.logger.info(f"Fetching {len(urls)} pages...")
            pages = await self.crawler.fetch_pages(urls)

            self.urls_fetched = sum(1 for p in pages if p.status_code == 200)
            self.urls_failed = len(pages) - self.urls_fetched
            self.logger.info(f"Fetched {self.urls_fetched} pages ({self.urls_failed} failed)")

            # Extract and chunk
            all_chunks = []
            for page in pages:
                if page.status_code != 200:
                    continue

                self.checkpoint.mark_url_processed(str(page.url))

                # Extract text
                text, extraction_method = self.extractor.extract_text(page.html_content)
                if not text:
                    continue

                # Create chunks
                chunks = self.chunker.chunk_text(text, str(page.url), page.title)
                self.chunks_created += len(chunks)

                # Check for duplicates
                new_chunks = []
                for chunk in chunks:
                    if self.deduplicator.is_duplicate(chunk.chunk_id):
                        self.chunks_deduplicated += 1
                    else:
                        self.deduplicator.register_hash(chunk.chunk_id)
                        new_chunks.append(chunk)

                all_chunks.extend(new_chunks)

            self.logger.info(
                f"Created {self.chunks_created} chunks, "
                f"{self.chunks_deduplicated} duplicates, "
                f"{len(all_chunks)} new chunks for embedding"
            )

            # Embed chunks (if not dry-run)
            if not dry_run and all_chunks:
                self.logger.info(f"Generating embeddings for {len(all_chunks)} chunks...")
                vectors = await self.embedder.embed_chunks(all_chunks)
                self.chunks_embedded = len(vectors)
                self.logger.info(f"Generated {self.chunks_embedded} embeddings")

                # Store in Qdrant
                self.logger.info("Storing vectors in Qdrant...")
                result = self.storage.upsert_vectors(vectors)
                self.vectors_stored = result.get("upserted", 0)
                self.logger.info(f"Stored {self.vectors_stored} vectors in Qdrant")

                # Mark chunks as embedded in checkpoint
                for chunk in all_chunks:
                    self.checkpoint.mark_chunk_embedded(chunk.chunk_id)

            # Save checkpoint
            self.checkpoint.save_checkpoint()

            self.logger.info("Pipeline completed successfully!")

            return self._create_log(start_time_seconds)

        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise

    def _create_log(self, start_time_seconds: float) -> IngestionLog:
        """Create final ingestion log."""
        elapsed = time.time() - start_time_seconds

        # Get Qdrant stats
        qdrant_stats = self.storage.get_collection_stats()

        log = IngestionLog(
            run_id=f"run-{self.start_time.isoformat()}",
            started_at=self.start_time,
            completed_at=datetime.utcnow(),
            duration_seconds=elapsed,
            status="success",
            book_root_url=str(self.config.book_root_url),
            cohere_model=self.config.cohere_model,
            qdrant_collection=self.config.qdrant_collection,
            summary=IngestionLogSummary(
                urls_discovered=self.urls_discovered,
                urls_fetched=self.urls_fetched,
                urls_failed=self.urls_failed,
                chunks_created=self.chunks_created,
                chunks_deduplicated=self.chunks_deduplicated,
                chunks_embedded=self.chunks_embedded,
                vectors_stored=self.vectors_stored,
                duplicate_skipped=self.chunks_deduplicated,
            ),
            performance=IngestionLogPerformance(
                crawl_time_seconds=0,  # TODO: Track individual times
                extraction_time_seconds=0,
                embedding_time_seconds=0,
                storage_time_seconds=0,
                total_time_seconds=elapsed,
            ),
            api_usage=IngestionLogAPIUsage(
                cohere_api_calls=self.chunks_embedded // self.config.batch_size + (1 if self.chunks_embedded % self.config.batch_size else 0),
                cohere_tokens_used=sum(
                    chunk.token_count
                    for chunk in (self.chunker.chunk_text("", "") if hasattr(self, "chunker") else [])
                ),  # Placeholder
                cohere_quota_remaining=0,  # TODO: Get from API
                qdrant_upserts=self.vectors_stored,
                qdrant_collection_size_mb=0,  # TODO: Calculate
            ),
            errors=[],
            pages=[],
        )

        return log
