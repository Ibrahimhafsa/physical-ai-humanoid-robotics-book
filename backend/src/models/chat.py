"""
Chat request/response models for RAG Agent API.

Models for handling user queries, retrieval results, and agent responses.
All models use Pydantic v2 for validation and JSON serialization.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class ChatRequest(BaseModel):
    """User query for RAG agent.

    Attributes:
        query: User question (required, non-empty)
        top_k: Number of chunks to retrieve (1-20, optional, default 5)
        similarity_threshold: Minimum relevance score (0.0-1.0, optional, default 0.5)
        user_id: Optional user identifier
        session_id: Optional session identifier
        metadata: Optional additional metadata
    """

    model_config = ConfigDict(json_schema_extra={"examples": [
        {
            "query": "What is humanoid robotics?",
            "top_k": 5,
            "similarity_threshold": 0.5
        }
    ]})

    query: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
    similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum similarity score")
    user_id: Optional[str] = Field(default=None, description="Optional user identifier")
    session_id: Optional[str] = Field(default=None, description="Optional session identifier")
    metadata: Optional[dict] = Field(default=None, description="Optional additional metadata")

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

    chunk_id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., description="Chunk text content")
    similarity_score: float = Field(ge=0.0, le=1.0, description="Cosine similarity score (0.0-1.0)")
    source_url: str = Field(..., description="URL of source document")
    section_title: str = Field(..., description="Document section/chapter title")
    rank: int = Field(ge=1, description="Position in result set (1-indexed)")


class ChatResponse(BaseModel):
    """Agent response with sources and metadata.

    Attributes:
        request_id: Request tracking ID (UUID format)
        answer: Agent-generated answer (required)
        sources: Retrieved chunks used (optional, default empty list)
        context_used: Number of chunks included
        tokens_used: Total tokens consumed
        response_time_ms: API latency in milliseconds
        timestamp: ISO 8601 timestamp
        note: Optional message (e.g., "Limited context available")
    """

    model_config = ConfigDict(json_schema_extra={"examples": [
        {
            "request_id": "550e8400-e29b-41d4-a716-446655440000",
            "answer": "Humanoid robotics is the field of robotics focused on creating robots with human-like form and capabilities.",
            "sources": [],
            "context_used": 3,
            "tokens_used": 250,
            "response_time_ms": 1200,
            "timestamp": "2025-12-25T12:00:00",
            "note": None
        }
    ]})

    request_id: str = Field(..., description="Request tracking ID (UUID format)")
    answer: str = Field(..., description="Agent-generated answer")
    sources: list[RetrievalResult] = Field(default_factory=list, description="Retrieved chunks used as sources")
    context_used: int = Field(default=0, ge=0, description="Number of chunks included in context")
    tokens_used: int = Field(default=0, ge=0, description="Total tokens consumed")
    response_time_ms: int = Field(default=0, ge=0, description="API latency in milliseconds")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    note: Optional[str] = Field(default=None, description="Optional message (e.g., 'Limited context available')")


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
