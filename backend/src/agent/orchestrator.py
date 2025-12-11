"""
RAG Orchestrator coordinating query → retrieval → generation flow.

Handles request processing, context assembly, and response generation
with token limit management and error handling.
"""

import logging
import time
from typing import Optional
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from backend.src.models.chat import ChatRequest, ChatResponse, RetrievalResult
from backend.src.agent.rag_agent import RAGAgent
from backend.src.retrieve import QueryEmbedder, QdrantRetriever, ContextExtractor

logger = logging.getLogger(__name__)


class RAGOrchestrator:
    """Orchestrates RAG request → retrieval → generation flow.

    Coordinates:
    1. Query validation
    2. Qdrant retrieval
    3. Context assembly with token limits
    4. Agent response generation
    5. Response formatting
    """

    def __init__(
        self,
        embedder: QueryEmbedder,
        retriever: QdrantRetriever,
        agent: RAGAgent,
        extractor: ContextExtractor,
        similarity_threshold: float = 0.5,
        max_context_tokens: int = 6000,
    ):
        """Initialize orchestrator.

        Args:
            embedder: QueryEmbedder for query embedding
            retriever: QdrantRetriever for similarity search
            agent: RAGAgent for response generation
            extractor: ContextExtractor for context assembly
            similarity_threshold: Minimum similarity score (default 0.5)
            max_context_tokens: Maximum context tokens (default 6000)
        """
        self.embedder = embedder
        self.retriever = retriever
        self.agent = agent
        self.extractor = extractor
        self.similarity_threshold = similarity_threshold
        self.max_context_tokens = max_context_tokens
        logger.info(f"Initialized RAG orchestrator (threshold={similarity_threshold}, max_tokens={max_context_tokens})")

    def process_query(self, chat_request: ChatRequest) -> ChatResponse:
        """Process query end-to-end: retrieve → assemble context → generate response.

        Args:
            chat_request: User query with optional parameters

        Returns:
            ChatResponse with answer, sources, and metadata

        Raises:
            ValueError: If query validation fails
            RuntimeError: If retrieval or generation fails
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Validate request
            if not chat_request.query.strip():
                raise ValueError("Query cannot be empty")

            logger.info(f"[{request_id}] Processing query: {chat_request.query[:50]}...")

            # Step 1: Embed query
            try:
                query_embedding = self.embedder.embed_query(chat_request.query)
                logger.debug(f"[{request_id}] Query embedded (dimension: {len(query_embedding)})")
            except Exception as e:
                logger.error(f"[{request_id}] Embedding failed: {e}")
                raise RuntimeError(f"Failed to embed query: {e}")

            # Step 2: Retrieve chunks from Qdrant
            try:
                search_results = self.retriever.search_similar(
                    query_embedding,
                    top_k=chat_request.top_k,
                    score_threshold=chat_request.similarity_threshold,
                )
                logger.info(f"[{request_id}] Retrieved {len(search_results)} chunks (threshold={chat_request.similarity_threshold})")
            except Exception as e:
                logger.error(f"[{request_id}] Retrieval failed: {e}")
                raise RuntimeError(f"Failed to retrieve context: {e}")

            # Convert to RetrievalResult models
            retrieval_results = [
                RetrievalResult(
                    chunk_id=result.get("chunk_id", "unknown"),
                    text=result.get("text", ""),
                    similarity_score=result.get("similarity_score", 0.0),
                    source_url=result.get("source_url", ""),
                    section_title=result.get("section_title", ""),
                    rank=i + 1,
                )
                for i, result in enumerate(search_results)
            ]

            # Step 3: Check if results meet threshold
            if not retrieval_results or all(r.similarity_score < self.similarity_threshold for r in retrieval_results):
                logger.warning(f"[{request_id}] No relevant chunks found (all below threshold)")
                response = ChatResponse(
                    request_id=request_id,
                    answer="I don't have information about this topic in the provided materials.",
                    sources=[],
                    context_used=0,
                    tokens_used=100,
                    response_time_ms=int((time.time() - start_time) * 1000),
                    timestamp=str(time.time()),
                    note="No chunks with sufficient similarity found for this query",
                )
                return response

            # Step 4: Assemble context (limit by token count)
            context_text = self._assemble_context(retrieval_results)
            logger.debug(f"[{request_id}] Context assembled ({len(context_text)} chars)")

            # Step 5: Generate response using agent
            try:
                answer = self.agent.generate_response(chat_request.query, context_text)
                logger.info(f"[{request_id}] Response generated ({len(answer)} chars)")
            except Exception as e:
                logger.error(f"[{request_id}] Generation failed: {e}")
                raise RuntimeError(f"Failed to generate response: {e}")

            # Step 6: Build response
            tokens_used = self._estimate_tokens(chat_request.query + context_text + answer)
            response = ChatResponse(
                request_id=request_id,
                answer=answer,
                sources=retrieval_results[:chat_request.top_k],  # Include top-K sources
                context_used=len(retrieval_results),
                tokens_used=tokens_used,
                response_time_ms=int((time.time() - start_time) * 1000),
                timestamp=str(time.time()),
            )

            logger.info(f"[{request_id}] Response complete ({tokens_used} tokens, {response.response_time_ms}ms)")
            return response

        except ValueError as e:
            logger.warning(f"[{request_id}] Validation error: {e}")
            raise
        except RuntimeError as e:
            logger.error(f"[{request_id}] Processing failed: {e}")
            raise

    def _assemble_context(self, results: list[RetrievalResult]) -> str:
        """Assemble context from retrieved chunks with token limit management.

        Args:
            results: Retrieved chunks ranked by similarity

        Returns:
            Formatted context text
        """
        context_lines = []
        total_tokens = 0

        for result in results:
            # Estimate tokens in this chunk
            chunk_tokens = self._estimate_tokens(result.text)
            if total_tokens + chunk_tokens > self.max_context_tokens - 1000:  # Reserve 1000 tokens
                logger.debug(f"Stopping context assembly: token limit approaching ({total_tokens} tokens)")
                break

            context_lines.append(f"[{result.rank}. {result.section_title} (similarity: {result.similarity_score:.2f})]")
            context_lines.append(result.text)
            context_lines.append("")
            total_tokens += chunk_tokens

        context = "\n".join(context_lines)
        logger.debug(f"Context assembled: {len(context_lines)} sections, ~{total_tokens} tokens")
        return context

    def _estimate_tokens(self, text: str) -> int:
        """Estimate tokens in text (rough approximation).

        Uses heuristic: 1 token ≈ 4 characters.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        return max(1, len(text) // 4)
