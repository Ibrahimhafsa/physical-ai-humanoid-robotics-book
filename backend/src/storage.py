"""Qdrant vector database storage and management."""

from typing import Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from src.models import Vector


class QdrantStorage:
    """Manage vector storage in Qdrant Cloud."""

    # Vector dimensions for different embedding models
    VECTOR_DIMENSIONS = {
        "embed-3-large": 4096,
        "embed-english-v3.0": 1024,
    }
    DEFAULT_DIMENSION = 1024  # Default to embed-english-v3.0

    def __init__(self, url: str, api_key: str, collection_name: str = "book_embeddings", vector_dimension: int = None):
        """Initialize Qdrant storage.

        Args:
            url: Qdrant Cloud instance URL
            api_key: Qdrant API key
            collection_name: Collection name for vectors
        """
        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.vector_dimension = vector_dimension or self.DEFAULT_DIMENSION
        self.client = QdrantClient(
            url=url,
            api_key=api_key,
            timeout=30.0,
        )

    def create_collection_if_needed(self) -> bool:
        """Create collection if it doesn't exist.

        Returns:
            True if collection created or already exists, False on error
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            existing_names = [c.name for c in collections.collections]

            if self.collection_name in existing_names:
                return True

            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_dimension,
                    distance=Distance.COSINE,
                ),
            )
            return True

        except UnexpectedResponse as e:
            if "exists" in str(e).lower():
                return True  # Collection exists
            return False
        except Exception:
            return False

    def upsert_vectors(self, vectors: List[Vector]) -> Dict[str, int]:
        """Upsert vectors with metadata to Qdrant.

        Args:
            vectors: List of Vector objects to store

        Returns:
            Dictionary with upsert statistics
        """
        if not vectors:
            return {"upserted": 0, "skipped": 0}

        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Upserting {len(vectors)} vectors. Storage vector_dimension: {self.vector_dimension}")

        points = []
        skipped = 0

        for vector in vectors:
            # Validate vector dimension
            actual_dim = len(vector.vector) if vector.vector else 0
            if actual_dim != self.vector_dimension:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Dimension mismatch: expected {self.vector_dimension}, got {actual_dim} for chunk {vector.chunk_id}")
                skipped += 1
                continue

            # Create point with metadata payload
            # Convert hash string to unsigned integer for Qdrant point ID
            # Take first 16 chars of hash and convert to int
            try:
                point_id = int(vector.vector_id[:16], 16) % (2**63 - 1)  # Ensure valid unsigned 64-bit int
            except ValueError:
                # Fallback: use hash of the ID string
                import hashlib
                point_id = int(hashlib.md5(vector.vector_id.encode()).hexdigest()[:15], 16)

            point = PointStruct(
                id=point_id,
                vector=vector.vector,
                payload={
                    "url": vector.url,
                    "chunk_id": vector.chunk_id,
                    "text": vector.text,
                    "section_title": vector.section_title,
                    "chunk_index": vector.chunk_index,
                    "token_count": vector.token_count,
                    "embedded_at": vector.embedded_at.isoformat(),
                    "embedding_model": vector.embedding_model,
                },
            )
            points.append(point)

        # Upsert points
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            return {"upserted": len(points), "skipped": skipped}
        except Exception as e:
            return {"upserted": 0, "skipped": len(vectors), "error": str(e)}

    def get_collection_stats(self) -> Dict[str, int]:
        """Get collection statistics.

        Returns:
            Dictionary with collection stats
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "points_count": collection_info.points_count,
                "vectors_count": collection_info.vectors_count,
                "status": collection_info.status,
            }
        except Exception:
            return {"points_count": 0, "vectors_count": 0, "status": "error"}

    def search_similar(
        self, query_vector: List[float], limit: int = 5, score_threshold: float = 0.7
    ) -> List[Dict]:
        """Search for similar vectors.

        Args:
            query_vector: Query embedding vector
            limit: Number of results to return
            score_threshold: Minimum similarity score

        Returns:
            List of similar chunks with metadata
        """
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold,
            )

            return [
                {
                    "score": hit.score,
                    "url": hit.payload.get("url"),
                    "text": hit.payload.get("text"),
                    "section_title": hit.payload.get("section_title"),
                }
                for hit in results.points
            ]
        except Exception:
            return []

    def close(self):
        """Close Qdrant client."""
        if hasattr(self.client, "close"):
            self.client.close()
