#!/usr/bin/env python
"""Manual re-indexing script for Qdrant with specific book pages."""

import sys
import os
import asyncio
from pathlib import Path

# Add repo root to Python path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "backend"))

# Load environment variables
from dotenv import load_dotenv
env_file = repo_root / "backend" / ".env"
load_dotenv(env_file)

# Change to backend directory
os.chdir(str(repo_root / "backend"))

async def main():
    """Main entry point for manual re-indexing."""
    from src.config import load_settings
    from src.crawler import DocosaurusCrawler
    from src.extractor import TextExtractor
    from src.chunker import TextChunker
    from src.deduplicator import Deduplicator
    from src.embedder import CohereEmbedder
    from src.storage import QdrantStorage
    from src.models import Page

    # Load config
    config = load_settings()

    print(f"Starting manual re-indexing...")
    print(f"Book URL: {config.book_root_url}")
    print(f"Model: {config.cohere_model}")
    print(f"Collection: {config.qdrant_collection}")

    # Manually specify URLs to index
    urls_to_index = [
        "http://localhost:3000/docs/01-fundamentals/01-what-is-physical-ai",
        "http://localhost:3000/docs/01-fundamentals/02-embodied-intelligence",
        "http://localhost:3000/docs/01-fundamentals/03-basics-of-robotics",
        "http://localhost:3000/docs/02-humanoid-robotics/01-ros2-architecture",
        "http://localhost:3000/docs/02-humanoid-robotics/02-nodes-and-topics",
        "http://localhost:3000/docs/02-humanoid-robotics/03-robot-control-basics",
        "http://localhost:3000/docs/03-digital-twin/01-simulation-fundamentals",
        "http://localhost:3000/docs/03-digital-twin/02-gazebo-setup-tutorial",
        "http://localhost:3000/docs/04-ai-brain/01-nvidia-isaac-overview",
        "http://localhost:3000/docs/04-ai-brain/02-computer-vision-basics",
    ]

    print(f"\nIndexing {len(urls_to_index)} pages...")

    # Initialize components
    crawler = DocosaurusCrawler(str(config.book_root_url))
    extractor = TextExtractor()
    chunker = TextChunker()
    deduplicator = Deduplicator()
    embedder = CohereEmbedder(
        api_key=config.cohere_api_key,
        model=config.cohere_model,
        batch_size=config.batch_size,
    )

    # Create vector storage with correct dimension
    vector_dimension = {
        "embed-3-large": 4096,
        "embed-english-v3.0": 1024,
    }.get(config.cohere_model, 1024)

    storage = QdrantStorage(
        url=str(config.qdrant_url),
        api_key=config.qdrant_api_key,
        collection_name=config.qdrant_collection,
        vector_dimension=vector_dimension,
    )

    # Create collection
    print("\nCreating Qdrant collection if needed...")
    if not storage.create_collection_if_needed():
        print("ERROR: Failed to create Qdrant collection")
        return

    # Fetch and process pages
    print(f"Fetching {len(urls_to_index)} pages...")
    pages = await crawler.fetch_pages(urls_to_index)

    fetched = sum(1 for p in pages if p.status_code == 200)
    print(f"Successfully fetched: {fetched}/{len(pages)} pages")

    # Extract, chunk, and embed
    all_chunks = []
    for page in pages:
        if page.status_code != 200:
            print(f"  SKIP (status {page.status_code}): {page.url}")
            continue

        print(f"  Processing: {page.url}")

        # Extract text
        text, method = extractor.extract_text(page.html_content)
        if not text:
            print(f"    - No text extracted")
            continue

        # Create chunks
        chunks = chunker.chunk_text(text, str(page.url), page.title)
        print(f"    - Created {len(chunks)} chunks")

        # Deduplicate
        new_chunks = [c for c in chunks if not deduplicator.is_duplicate(c.chunk_id)]
        for chunk in new_chunks:
            deduplicator.register_hash(chunk.chunk_id)
        print(f"    - After dedup: {len(new_chunks)} chunks")

        all_chunks.extend(new_chunks)

    print(f"\nTotal chunks to embed: {len(all_chunks)}")

    if not all_chunks:
        print("ERROR: No chunks to embed!")
        return

    # Generate embeddings
    print(f"Generating embeddings with {config.cohere_model}...")
    try:
        vectors = await embedder.embed_chunks(all_chunks)
        print(f"Generated {len(vectors)} embeddings")
    except Exception as e:
        print(f"ERROR: Embedding failed: {e}")
        return

    # Store vectors
    print(f"Uploading vectors to Qdrant...")
    try:
        result = storage.upsert_vectors(vectors)
        upserted = result.get("upserted", 0)
        print(f"Upserted {upserted} vectors")
    except Exception as e:
        print(f"ERROR: Upload failed: {e}")
        return

    # Verify collection
    print(f"\nVerifying collection...")
    try:
        storage.verify_collection_exists()
        print("SUCCESS: Collection verified!")
    except Exception as e:
        print(f"ERROR: Verification failed: {e}")
        return

    print(f"\nRe-indexing complete!")
    print(f"Total vectors stored: {upserted}")

if __name__ == "__main__":
    asyncio.run(main())
