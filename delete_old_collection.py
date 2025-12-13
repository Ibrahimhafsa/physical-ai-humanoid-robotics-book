#!/usr/bin/env python
"""Delete old Qdrant collection to prepare for re-indexing."""

import os
import sys
from pathlib import Path

# Add repo root to Python path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
env_file = repo_root / "backend" / ".env"
load_dotenv(env_file)

# Get configuration
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION", "book_embeddings")

if not qdrant_url or not qdrant_api_key:
    print("Error: QDRANT_URL and QDRANT_API_KEY must be set in .env")
    sys.exit(1)

print(f"Connecting to Qdrant at: {qdrant_url}")
client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, prefer_grpc=False)

# Check if collection exists
try:
    collections = client.get_collections()
    existing_collections = [c.name for c in collections.collections]

    if collection_name not in existing_collections:
        print(f"Collection '{collection_name}' does not exist.")
        print(f"Existing collections: {existing_collections}")
        sys.exit(0)

    print(f"Found collection: {collection_name}")

    # Get collection info
    collection_info = client.get_collection(collection_name)
    points_count = collection_info.points_count
    print(f"Collection has {points_count} vectors")

    # Confirm deletion
    response = input(f"Delete collection '{collection_name}' with {points_count} vectors? (yes/no): ")
    if response.lower() != "yes":
        print("Deletion cancelled.")
        sys.exit(0)

    # Delete collection
    print(f"Deleting collection '{collection_name}'...")
    client.delete_collection(collection_name)
    print(f"✅ Collection '{collection_name}' deleted successfully")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
