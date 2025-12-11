"""
Retrieval module for querying Qdrant with Cohere embeddings.

Provides functionality to:
- Generate query embeddings via Cohere API
- Search Qdrant for similar chunks
- Extract and merge context from retrieved results
"""

import logging
import os
import time
from typing import List, Optional, Tuple

import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

logger = logging.getLogger(__name__)


class QueryEmbedder:
    """Generates embeddings for queries using Cohere API."""

    def __init__(self, api_key: str, model: str = "embed-3-large", batch_size: int = 8):
        """
        Initialize Cohere embedder.

        Args:
            api_key: Cohere API key
            model: Embedding model name (default: embed-3-large)
            batch_size: Number of texts to embed per API call (default: 8)
        """
        self.api_key = api_key
        self.model = model
        self.batch_size = batch_size
        self.client = cohere.ClientV2(api_key=api_key)
        logger.info(f"Initialized QueryEmbedder with model {model}")

    def embed_query(self, query_text: str) -> List[float]:
        """
        Generate embedding for a single query.

        Args:
            query_text: Query string to embed

        Returns:
            4096-dimensional embedding vector

        Raises:
            ValueError: If query is empty or API fails
        """
        if not query_text or len(query_text.strip()) < 3:
            raise ValueError("Query must be non-empty and at least 3 characters")

        try:
            start = time.time()
            response = self.client.embed(
                texts=[query_text],
                model=self.model,
                input_type="search_query"
            )
            elapsed = time.time() - start
            logger.debug(f"Embedded query in {elapsed:.2f}s: {query_text[:50]}...")

            if response.embeddings:
                return response.embeddings[0]
            else:
                raise ValueError("No embeddings returned from Cohere")
        except Exception as e:
            logger.error(f"Failed to embed query: {e}")
            raise

    def embed_batch(self, queries: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple queries with batching.

        Args:
            queries: List of query strings

        Returns:
            List of embedding vectors (one per query)
        """
        all_embeddings = []

        for i in range(0, len(queries), self.batch_size):
            batch = queries[i : i + self.batch_size]
            try:
                start = time.time()
                response = self.client.embed(
                    texts=batch,
                    model=self.model,
                    input_type="search_query"
                )
                elapsed = time.time() - start
                logger.debug(f"Embedded batch of {len(batch)} queries in {elapsed:.2f}s")

                all_embeddings.extend(response.embeddings)
            except Exception as e:
                logger.error(f"Failed to embed batch: {e}")
                raise

        return all_embeddings


class QdrantRetriever:
    """Searches Qdrant for similar chunks given query embeddings."""

    def __init__(self, url: str, api_key: str, collection_name: str = "book_embeddings"):
        """
        Initialize Qdrant retriever.

        Args:
            url: Qdrant instance URL (https://...)
            api_key: Qdrant API key
            collection_name: Name of collection to search (default: book_embeddings)
        """
        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.client = QdrantClient(url=url, api_key=api_key, prefer_grpc=False)
        logger.info(f"Initialized QdrantRetriever for collection '{collection_name}'")

    def verify_collection_exists(self) -> bool:
        """
        Verify that the Qdrant collection exists and is accessible.

        Returns:
            True if collection exists and has vectors

        Raises:
            ValueError: If collection doesn't exist or is empty
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            points_count = collection_info.points_count
            logger.info(f"Collection '{self.collection_name}' has {points_count} vectors")

            if points_count == 0:
                raise ValueError(f"Collection '{self.collection_name}' is empty")

            return True
        except Exception as e:
            logger.error(f"Failed to verify collection: {e}")
            raise

    def search_similar(
        self,
        query_vector: List[float],
        top_k: int = 5,
        score_threshold: float = 0.5
    ) -> List[dict]:
        """
        Search Qdrant for chunks similar to query embedding.

        Args:
            query_vector: Query embedding (4096-D vector)
            top_k: Number of results to return (default: 5)
            score_threshold: Minimum similarity score (default: 0.5)

        Returns:
            List of results, each with:
            {
                "rank": int (1-K),
                "similarity_score": float (0.0-1.0),
                "chunk_id": str,
                "source_url": str,
                "section_title": str,
                "text_excerpt": str
            }

        Raises:
            ValueError: If query vector dimension is invalid
            Exception: If Qdrant search fails
        """
        if len(query_vector) != 4096:
            raise ValueError(f"Query vector must be 4096-D, got {len(query_vector)}")

        try:
            start = time.time()
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=score_threshold
            )
            elapsed = time.time() - start
            logger.debug(f"Searched Qdrant in {elapsed:.2f}s, found {len(search_result)} results")

            results = []
            for rank, point in enumerate(search_result, 1):
                payload = point.payload or {}

                # Flag unusual scores
                if point.score > 0.95:
                    logger.warning(f"Unusually high score: {point.score:.3f} (potential embedding issue)")
                if point.score < 0.5:
                    logger.warning(f"Low score: {point.score:.3f} (potentially irrelevant)")

                result = {
                    "rank": rank,
                    "similarity_score": float(point.score),
                    "chunk_id": payload.get("chunk_id", ""),
                    "source_url": payload.get("url", ""),
                    "section_title": payload.get("section_title", ""),
                    "text_excerpt": payload.get("text", "")[:200],  # First 200 chars
                }
                results.append(result)

            return results
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            raise


class ContextExtractor:
    """Extracts and merges context from retrieved chunks."""

    @staticmethod
    def extract_context(results: List[dict], max_length: int = 1000) -> str:
        """
        Merge top chunks into a clean paragraph.

        Args:
            results: List of retrieval results from QdrantRetriever.search_similar()
            max_length: Maximum length of merged context

        Returns:
            Merged context string with sentences separated by spaces
        """
        if not results:
            return "No context found"

        # Extract text from top 3 results
        texts = [result.get("text_excerpt", "") for result in results[:3]]

        # Clean and merge
        merged = " ".join(texts)

        # Truncate to max length
        if len(merged) > max_length:
            merged = merged[:max_length] + "..."

        return merged.strip()

    @staticmethod
    def format_results(results: List[dict]) -> str:
        """
        Format results for console output.

        Args:
            results: List of retrieval results

        Returns:
            Formatted string for display
        """
        if not results:
            return "No results found"

        output = []
        for result in results:
            output.append(
                f"Rank {result['rank']}: Score {result['similarity_score']:.3f} | "
                f"URL: {result['source_url'][:60]} | "
                f"Chunk: {result['chunk_id']}"
            )
            output.append(f"  Section: {result['section_title']}")
            output.append(f"  Text: {result['text_excerpt'][:100]}...")

        return "\n".join(output)
