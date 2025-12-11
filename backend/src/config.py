"""Configuration management for Book Embedding Pipeline."""

import logging
from pathlib import Path
from typing import Optional

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pipeline configuration loaded from environment variables."""

    # Cohere Configuration
    cohere_api_key: str = Field(..., description="Cohere API key for embeddings")
    cohere_model: str = Field(
        default="embed-3-large",
        description="Cohere embedding model to use",
    )

    # Qdrant Configuration
    qdrant_url: HttpUrl = Field(..., description="Qdrant Cloud instance URL")
    qdrant_api_key: str = Field(..., description="Qdrant API key")
    qdrant_collection: str = Field(
        default="book_embeddings",
        description="Qdrant collection name",
    )

    # Book Configuration
    book_root_url: HttpUrl = Field(..., description="Root URL of the Docusaurus book")

    # Pipeline Configuration
    batch_size: int = Field(
        default=8,
        ge=1,
        le=100,
        description="Batch size for Cohere embedding API calls",
    )
    max_pages: Optional[int] = Field(
        default=None,
        ge=1,
        description="Maximum pages to process (None = all pages)",
    )
    max_retries: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Max retries for transient failures",
    )
    retry_delay_ms: int = Field(
        default=1000,
        ge=100,
        le=60000,
        description="Initial retry delay in milliseconds",
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    output_dir: str = Field(
        default="./embeddings_output",
        description="Directory for output logs and checkpoints",
    )

    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is valid."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v_upper

    @field_validator("output_dir")
    @classmethod
    def ensure_output_dir_exists(cls, v: str) -> str:
        """Ensure output directory is created if it doesn't exist."""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def get_logger(self, name: str) -> logging.Logger:
        """Get configured logger."""
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)

        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(self.log_level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        if not logger.handlers:
            logger.addHandler(handler)

        return logger


def load_settings() -> Settings:
    """Load and validate settings from environment."""
    try:
        settings = Settings()
        return settings
    except Exception as e:
        raise RuntimeError(f"Failed to load settings: {e}") from e
