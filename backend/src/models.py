"""Pydantic models for the Book Embedding Pipeline."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Page(BaseModel):
    """A single Docusaurus page with fetched content."""

    url: HttpUrl = Field(..., description="Page URL")
    title: str = Field(..., description="Page title", max_length=255)
    html_content: str = Field(..., description="Raw HTML content")
    status_code: int = Field(..., ge=100, le=599, description="HTTP response status")
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    fetch_error: Optional[str] = Field(
        default=None, description="Error message if fetch failed"
    )

    class Config:
        """Model configuration."""

        json_schema_extra = {
            "example": {
                "url": "https://example.com/docs/intro",
                "title": "Introduction",
                "html_content": "<html>...</html>",
                "status_code": 200,
                "fetched_at": "2025-12-12T10:30:00Z",
            }
        }


class Chunk(BaseModel):
    """A semantic unit of text extracted from a page."""

    chunk_id: str = Field(
        ..., description="Unique ID (SHA256 hash of normalized text)"
    )
    url: HttpUrl = Field(..., description="Parent page URL")
    text: str = Field(..., description="Clean text content", max_length=8192)
    section_title: Optional[str] = Field(
        default=None, description="Section/heading context", max_length=255
    )
    chunk_index: int = Field(..., ge=0, description="Position within page")
    token_count: int = Field(..., ge=1, le=512, description="Estimated token count")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    extraction_method: str = Field(
        default="semantic_paragraph",
        description="How text was extracted",
    )

    class Config:
        """Model configuration."""

        json_schema_extra = {
            "example": {
                "chunk_id": "abc123def456",
                "url": "https://example.com/docs/intro",
                "text": "This is the extracted text of the chunk...",
                "section_title": "Introduction",
                "chunk_index": 0,
                "token_count": 128,
                "created_at": "2025-12-12T10:30:00Z",
                "extraction_method": "semantic_paragraph",
            }
        }


class Vector(BaseModel):
    """A 4096-dimensional embedding stored in Qdrant."""

    vector_id: str = Field(..., description="Unique ID for Qdrant point (chunk_id)")
    vector: List[float] = Field(..., description="4096-dimensional embedding")
    url: str = Field(..., description="Source page URL (metadata)")
    chunk_id: str = Field(..., description="Source chunk hash (metadata)")
    text: str = Field(..., description="Original text content (metadata)")
    section_title: Optional[str] = Field(
        default=None, description="Section context (metadata)"
    )
    chunk_index: int = Field(..., ge=0, description="Position within page (metadata)")
    token_count: int = Field(..., description="Token count (metadata)")
    embedded_at: datetime = Field(default_factory=datetime.utcnow)
    embedding_model: str = Field(default="embed-3-large")

    @property
    def vector_dimension(self) -> int:
        """Return vector dimension."""
        return len(self.vector)

    def validate_vector_dimension(self) -> bool:
        """Validate vector has exactly 4096 dimensions."""
        return self.vector_dimension == 4096

    class Config:
        """Model configuration."""

        json_schema_extra = {
            "example": {
                "vector_id": "abc123def456",
                "vector": [0.1, 0.2, 0.3],  # Actually 4096 values
                "url": "https://example.com/docs/intro",
                "chunk_id": "abc123def456",
                "text": "Full text of chunk...",
                "section_title": "Installation",
                "chunk_index": 0,
                "token_count": 128,
                "embedded_at": "2025-12-12T10:30:00Z",
                "embedding_model": "embed-3-large",
            }
        }


class IngestionLogSummary(BaseModel):
    """Summary statistics for pipeline run."""

    urls_discovered: int = Field(..., ge=0)
    urls_fetched: int = Field(..., ge=0)
    urls_failed: int = Field(..., ge=0)
    chunks_created: int = Field(..., ge=0)
    chunks_deduplicated: int = Field(..., ge=0)
    chunks_embedded: int = Field(..., ge=0)
    vectors_stored: int = Field(..., ge=0)
    duplicate_skipped: int = Field(..., ge=0)


class IngestionLogPerformance(BaseModel):
    """Performance metrics for pipeline run."""

    crawl_time_seconds: float = Field(..., ge=0)
    extraction_time_seconds: float = Field(..., ge=0)
    embedding_time_seconds: float = Field(..., ge=0)
    storage_time_seconds: float = Field(..., ge=0)
    total_time_seconds: float = Field(..., ge=0)


class IngestionLogAPIUsage(BaseModel):
    """API usage statistics."""

    cohere_api_calls: int = Field(..., ge=0)
    cohere_tokens_used: int = Field(..., ge=0)
    cohere_quota_remaining: int = Field(..., ge=0)
    qdrant_upserts: int = Field(..., ge=0)
    qdrant_collection_size_mb: float = Field(..., ge=0)


class IngestionLogError(BaseModel):
    """Error entry in ingestion log."""

    url: str = Field(...)
    error_type: str = Field(...)
    message: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IngestionLogPageStats(BaseModel):
    """Per-page statistics."""

    url: str = Field(...)
    title: str = Field(...)
    status: str = Field(...)  # success, failed, partial
    chunks_created: int = Field(..., ge=0)
    chunks_embedded: int = Field(..., ge=0)
    fetch_time_ms: int = Field(..., ge=0)
    extraction_time_ms: int = Field(..., ge=0)
    embedding_time_ms: int = Field(..., ge=0)


class IngestionLog(BaseModel):
    """Complete ingestion log for a pipeline run."""

    run_id: str = Field(..., description="Unique run identifier")
    started_at: datetime = Field(...)
    completed_at: datetime = Field(...)
    duration_seconds: float = Field(..., ge=0)
    status: str = Field(...)  # success, partial, failed

    book_root_url: str = Field(...)
    cohere_model: str = Field(...)
    qdrant_collection: str = Field(...)

    summary: IngestionLogSummary = Field(...)
    performance: IngestionLogPerformance = Field(...)
    api_usage: IngestionLogAPIUsage = Field(...)
    errors: List[IngestionLogError] = Field(default_factory=list)
    pages: List[IngestionLogPageStats] = Field(default_factory=list)

    class Config:
        """Model configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}
