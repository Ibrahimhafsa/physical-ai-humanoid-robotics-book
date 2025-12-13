#!/usr/bin/env python
"""Re-index Qdrant directly from markdown files."""

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
    """Re-index from markdown files."""
    from src.config import load_settings
    from src.chunker import TextChunker
    from src.deduplicator import Deduplicator
    from src.embedder import CohereEmbedder
    from src.storage import QdrantStorage
    from src.models import Chunk

    # Load config
    config = load_settings()

    print(f"Starting re-indexing from markdown files...")
    print(f"Model: {config.cohere_model}")
    print(f"Collection: {config.qdrant_collection}")

    # Find all markdown files in docs
    docs_dir = repo_root / "book-docs" / "docs"
    md_files = list(docs_dir.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    # Initialize components
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

    # Process markdown files
    all_chunks = []
    for md_file in md_files:
        rel_path = md_file.relative_to(docs_dir)
        # Skip template files
        if rel_path.name.startswith("_"):
            continue

        print(f"\nProcessing: {rel_path}")

        try:
            text = md_file.read_text(encoding="utf-8")
            # Skip if too short (less than 100 chars of actual content)
            content_only = text.split("---")[-1]  # Remove frontmatter
            if not text or len(content_only.strip()) < 100:
                print(f"  - Skipped (too short or empty)")
                continue

            # Extract title from file or frontmatter
            title = rel_path.stem.replace("-", " ").title()
            if text.startswith("---"):
                try:
                    # Simple frontmatter extraction
                    lines = text.split("\n")
                    for i, line in enumerate(lines[1:], 1):
                        if line.startswith("---"):
                            break
                        if line.startswith("title:"):
                            title = line.split(":", 1)[1].strip().strip("'\"")
                except:
                    pass

            # Create simulated URL (must be http/https for Chunk validation)
            # Convert path like "02-humanoid-robotics/01-ros2-architecture.md"
            # to "http://localhost:3000/docs/02-humanoid-robotics/01-ros2-architecture"
            url_path = str(rel_path.with_suffix('')).replace("\\", "/")
            url = f"http://localhost:3000/docs/{url_path}"

            # Create chunks
            chunks = chunker.chunk_text(text, str(url), title)
            print(f"  - Created {len(chunks)} chunks")

            # Deduplicate
            new_chunks = [c for c in chunks if not deduplicator.is_duplicate(c.chunk_id)]
            for chunk in new_chunks:
                deduplicator.register_hash(chunk.chunk_id)
            print(f"  - After dedup: {len(new_chunks)} chunks")

            all_chunks.extend(new_chunks)

        except Exception as e:
            print(f"  - ERROR: {e}")
            continue

    print(f"\n\nTotal chunks to embed: {len(all_chunks)}")

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
        import traceback
        traceback.print_exc()
        return

    # Store vectors
    print(f"Uploading vectors to Qdrant...")
    print(f"Vector dimension: {vector_dimension}")
    if vectors:
        print(f"Sample vector type: {type(vectors[0].vector)}")
        print(f"Sample vector length: {len(vectors[0].vector)}")
        if isinstance(vectors[0].vector, list) and len(vectors[0].vector) > 0:
            print(f"Sample vector[0] type: {type(vectors[0].vector[0])}")
            print(f"Sample first 3 elements: {vectors[0].vector[:3]}")
    print(f"\nDEBUG: About to call upsert_vectors")
    print(f"DEBUG: storage.vector_dimension = {storage.vector_dimension}")
    print(f"DEBUG: Number of vectors = {len(vectors)}")

    try:
        result = storage.upsert_vectors(vectors)
        print(f"DEBUG: upsert_vectors returned: {result}")
        upserted = result.get("upserted", 0)
        skipped = result.get("skipped", 0)
        print(f"Upserted {upserted} vectors, Skipped {skipped} vectors")
        if skipped > 0:
            print(f"WARNING: {skipped} vectors were skipped (dimension mismatch?)")
        if "error" in result:
            print(f"ERROR in upsert: {result['error']}")
    except Exception as e:
        print(f"ERROR: Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Verify collection
    print(f"\nVerifying collection...")
    try:
        stats = storage.get_collection_stats()
        points_count = stats.get("points_count", 0)
        print(f"Collection stats: {points_count} points")
        if points_count > 0:
            print("SUCCESS: Collection verified!")
        else:
            print("WARNING: Collection exists but is empty!")
    except Exception as e:
        print(f"ERROR: Verification failed: {e}")
        return

    print(f"\nRe-indexing complete!")
    print(f"Total vectors stored: {upserted}")

if __name__ == "__main__":
    asyncio.run(main())
