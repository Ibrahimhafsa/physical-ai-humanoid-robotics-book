"""Logging configuration for Book Embedding Pipeline."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


def setup_logging(
    name: str,
    level: str = "INFO",
    log_dir: Optional[str] = None,
    enable_json: bool = True,
) -> logging.Logger:
    """Setup logging with console and optional file output."""
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level.upper())

    if enable_json:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_dir provided)
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        log_file = log_path / f"{name}.log"

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level.upper())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def log_with_extra(logger: logging.Logger, level: str, message: str, **kwargs: Any):
    """Log message with extra fields."""
    log_method = getattr(logger, level.lower())

    # Create a custom LogRecord-like object to pass extra fields
    class ExtraRecord:
        def __init__(self, **fields):
            self.extra_fields = fields

    # Use the standard logging mechanism
    extra = ExtraRecord(**kwargs)
    log_method(message, extra=extra.__dict__)
