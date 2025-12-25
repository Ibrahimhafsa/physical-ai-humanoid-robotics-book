"""
Chat request/response models for RAG Agent API.

Models for handling user queries, retrieval results, and agent responses.
All models use Pydantic v2 for validation and JSON serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    query: str = Field(..., description="User question")
    top_k: int = Field(default=5, ge=1, le=20)
    similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

class RetrievalResult(BaseModel):
    content: str
    source: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[RetrievalResult] = []


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
