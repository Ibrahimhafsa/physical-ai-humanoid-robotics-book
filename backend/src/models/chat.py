"""
Chat request/response models for RAG Agent API.

Models for handling user queries, retrieval results, and agent responses.
All models use Pydantic v2 for validation and JSON serialization.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """User query for RAG agent.

    Attributes:
        query: User question (required, non-empty)
        top_k: Number of chunks to retrieve (1-20)
        similarity_threshold: Minimum relevance score (0.0-1.0)
        user_id: Optional user identifier
        session_id: Optional session identifier
        metadata: Optional additional metadata
    """

    query: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
    similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum similarity score")
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[dict] = None

    @field_validator("query")
    @classmethod
    def query_not_whitespace(cls, v: str) -> str:
        """Validate query is not just whitespace."""
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace")
        return v.strip()


class RetrievalResult(BaseModel):
    """Chunk retrieved from Qdrant.

    Attributes:
        chunk_id: Unique chunk identifier
        text: Chunk text content
        similarity_score: Cosine similarity to query (0.0-1.0)
        source_url: URL of source document
        section_title: Document section/chapter
        rank: Position in result set (1-indexed)
    """

    chunk_id: str
    text: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    source_url: str
    section_title: str
    rank: int = Field(ge=1)


class ChatResponse(BaseModel):
    """Agent response with sources and metadata.

    Attributes:
        request_id: Request tracking ID (UUID format)
        answer: Agent-generated answer
        sources: Retrieved chunks used
        context_used: Number of chunks included
        tokens_used: Total tokens consumed
        response_time_ms: API latency in milliseconds
        timestamp: ISO 8601 timestamp
        note: Optional message (e.g., "Limited context available")
    """

    request_id: str
    answer: str
    sources: list[RetrievalResult] = Field(default_factory=list)
    context_used: int = 0
    tokens_used: int = 0
    response_time_ms: int = 0
    timestamp: str
    note: Optional[str] = None


class ErrorDetail(BaseModel):
    """Error detail for validation errors.

    Attributes:
        field: Field name that caused error
        message: Error message
    """

    field: str
    message: str


class ErrorResponse(BaseModel):
    """Error response with details.

    Attributes:
        request_id: Request tracking ID
        error: Error type
        details: Field-level error details
        timestamp: ISO 8601 timestamp
    """

    request_id: str
    error: str
    details: list[ErrorDetail] = Field(default_factory=list)
    timestamp: str


class ContextWindow(BaseModel):
    """Token limit configuration.

    Attributes:
        max_tokens: Maximum total context tokens (default 6000)
        reserved_for_response: Tokens reserved for LLM response
        chunk_ordering: Ranking strategy (similarity, position, hybrid)
    """

    max_tokens: int = Field(default=6000)
    reserved_for_response: int = Field(default=1500)
    chunk_ordering: str = Field(default="similarity")
