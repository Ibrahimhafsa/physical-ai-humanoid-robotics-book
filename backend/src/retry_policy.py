"""Exponential backoff retry logic for transient failures."""

import asyncio
import time
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


class RetryPolicy:
    """Implement exponential backoff retry strategy."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay_ms: int = 1000,
        max_delay_ms: int = 60000,
        backoff_multiplier: float = 2.0,
    ):
        """Initialize retry policy.

        Args:
            max_retries: Maximum number of retry attempts
            initial_delay_ms: Initial retry delay in milliseconds
            max_delay_ms: Maximum delay between retries in milliseconds
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.initial_delay_ms = initial_delay_ms
        self.max_delay_ms = max_delay_ms
        self.backoff_multiplier = backoff_multiplier

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt (in seconds).

        Args:
            attempt: Attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        delay_ms = min(
            self.initial_delay_ms * (self.backoff_multiplier ** attempt),
            self.max_delay_ms,
        )
        return delay_ms / 1000.0

    async def retry_async(
        self,
        func: Callable[..., Awaitable[T]],
        *args,
        retryable_exceptions: tuple = (Exception,),
        **kwargs,
    ) -> T:
        """Execute async function with retry logic.

        Args:
            func: Async function to execute
            args: Positional arguments for func
            retryable_exceptions: Tuple of exceptions to retry on
            kwargs: Keyword arguments for func

        Returns:
            Result from successful function call

        Raises:
            Last exception if all retries exhausted
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except retryable_exceptions as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    await asyncio.sleep(delay)
                continue

        raise last_exception

    def retry_sync(
        self,
        func: Callable[..., T],
        *args,
        retryable_exceptions: tuple = (Exception,),
        **kwargs,
    ) -> T:
        """Execute sync function with retry logic.

        Args:
            func: Sync function to execute
            args: Positional arguments for func
            retryable_exceptions: Tuple of exceptions to retry on
            kwargs: Keyword arguments for func

        Returns:
            Result from successful function call

        Raises:
            Last exception if all retries exhausted
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except retryable_exceptions as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                continue

        raise last_exception
