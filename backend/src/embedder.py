"""Cohere embeddings generation with batch processing."""

import asyncio
from typing import List

import cohere

from src.models import Chunk, Vector
from src.retry_policy import RetryPolicy


class CohereEmbedder:
    """Generate embeddings using Cohere API."""

    def __init__(self, api_key: str, model: str = "embed-3-large", batch_size: int = 8):
        """Initialize Cohere embedder.

        Args:
            api_key: Cohere API key
            model: Cohere embedding model to use
            batch_size: Batch size for API calls (max 100)
        """
        self.api_key = api_key
        self.model = model
        self.batch_size = min(batch_size, 100)
        self.client = cohere.AsyncClientV2(api_key=api_key)
        self.retry_policy = RetryPolicy(max_retries=3, initial_delay_ms=1000)

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts.

        Args:
            texts: List of texts to embed (max 100)

        Returns:
            List of 4096-dimensional embeddings
        """
        if not texts or len(texts) > 100:
            raise ValueError("Batch size must be 1-100")

        async def _embed():
            response = await self.client.embed(
                model=self.model,
                texts=texts,
                input_type="search_document",
            )
            return response.embeddings

        embeddings = await self.retry_policy.retry_async(
            _embed,
            retryable_exceptions=(Exception,),
        )
        return embeddings

    async def embed_chunks(self, chunks: List[Chunk]) -> List[Vector]:
        """Generate embeddings for a list of chunks.

        Args:
            chunks: List of chunks to embed

        Returns:
            List of Vector objects with embeddings
        """
        if not chunks:
            return []

        vectors = []
        texts = [chunk.text for chunk in chunks]

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i : i + self.batch_size]
            batch_chunks = chunks[i : i + self.batch_size]

            embeddings = await self.embed_batch(batch_texts)

            for chunk, embedding in zip(batch_chunks, embeddings):
                vector = Vector(
                    vector_id=chunk.chunk_id,
                    vector=embedding,
                    url=str(chunk.url),
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    section_title=chunk.section_title,
                    chunk_index=chunk.chunk_index,
                    token_count=chunk.token_count,
                    embedding_model=self.model,
                )
                vectors.append(vector)

        return vectors

    async def close(self):
        """Close the Cohere client."""
        if hasattr(self.client, "close"):
            await self.client.close()
