"""Qdrant vector database storage and management."""

from typing import Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from src.models import Vector


class QdrantStorage:
    """Manage vector storage in Qdrant Cloud."""

    VECTOR_DIMENSION = 4096

    def __init__(self, url: str, api_key: str, collection_name: str = "book_embeddings"):
        """Initialize Qdrant storage.

        Args:
            url: Qdrant Cloud instance URL
            api_key: Qdrant API key
            collection_name: Collection name for vectors
        """
        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
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
                    size=self.VECTOR_DIMENSION,
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

        points = []
        skipped = 0

        for vector in vectors:
            # Validate vector dimension
            if len(vector.vector) != self.VECTOR_DIMENSION:
                skipped += 1
                continue

            # Create point with metadata payload
            point = PointStruct(
                id=vector.vector_id,
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
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=None,
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
                for hit in results
            ]
        except Exception:
            return []

    def close(self):
        """Close Qdrant client."""
        if hasattr(self.client, "close"):
            self.client.close()
