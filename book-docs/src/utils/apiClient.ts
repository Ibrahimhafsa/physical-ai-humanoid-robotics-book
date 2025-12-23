/**
 * API Client for RAG Chat Widget
 * Handles all communication with the FastAPI backend
 * Includes retry logic, timeout handling, and error mapping
 */

import type {
  QueryRequest,
  ChatResponse,
  ErrorResponse,
  APIError,
} from '../components/RAGChatWidget/types';

/**
 * Maximum number of retry attempts for transient errors
 */
const MAX_RETRIES = 3;

/**
 * Request timeout in milliseconds (30 seconds)
 */
const REQUEST_TIMEOUT = 30000;

/**
 * Custom error class for API errors
 */
class FetchAPIError extends Error implements APIError {
  status: number;
  retry: boolean;
  timestamp?: string;

  constructor(
    message: string,
    status: number,
    retry: boolean,
    timestamp?: string
  ) {
    super(message);
    this.name = 'FetchAPIError';
    this.status = status;
    this.retry = retry;
    this.timestamp = timestamp;
  }
}

/**
 * Retry logic with exponential backoff
 * Returns delay in milliseconds: 1s, 2s, 4s
 */
function getBackoffDelay(retryCount: number): number {
  return Math.pow(2, retryCount) * 1000; // 1s, 2s, 4s
}

/**
 * Sleep utility for retrying with delay
 */
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Determines if an error is retryable
 * Retries only 5xx errors and timeouts, not client errors (4xx)
 */
function isRetryableError(error: unknown): boolean {
  if (error instanceof FetchAPIError) {
    // Retryable: 5xx server errors and timeouts
    return error.retry;
  }
  // Network errors are retryable
  return true;
}

/**
 * Map HTTP error status and error response to user-friendly message
 */
function mapErrorResponse(
  status: number,
  errorBody?: ErrorResponse
): string {
  const errorDetail = errorBody?.detail?.error;

  // Map specific HTTP status codes
  switch (status) {
    case 400:
      return errorDetail || 'Please enter a valid question.';
    case 408:
      return 'Request took too long. Please try again.';
    case 429:
      return 'Too many requests. Please wait a moment before trying again.';
    case 500:
      return errorDetail || 'Server error. Please try again.';
    case 503:
      return 'Service temporarily unavailable. Please try again later.';
    default:
      return errorDetail || `Request failed with status ${status}`;
  }
}

/**
 * Fetch query with retry logic and exponential backoff
 * @param request - QueryRequest to send to backend
 * @param apiUrl - Backend API endpoint URL
 * @returns Promise<ChatResponse> with answer and sources
 * @throws FetchAPIError if all retries fail or request is not retryable
 */
export async function fetchQuery(
  request: QueryRequest,
  apiUrl: string
): Promise<ChatResponse> {
  let lastError: Error | null = null;

  // Log request details for debugging
  if (process.env.NODE_ENV === 'development') {
    console.log('[RAGChatWidget] Sending query request:', {
      apiUrl,
      query: request.query?.substring(0, 50) + '...',
      top_k: request.top_k,
      similarity_threshold: request.similarity_threshold,
      contextLength: request.context?.length ?? 0,
    });
  }

  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(
        () => controller.abort(),
        REQUEST_TIMEOUT
      );

      try {
        const response = await fetch(`${apiUrl}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
          signal: controller.signal,
        });

        // Log response for debugging
        if (process.env.NODE_ENV === 'development') {
          console.log('[RAGChatWidget] Received response:', {
            status: response.status,
            ok: response.ok,
            contentType: response.headers.get('content-type'),
          });
        }

        clearTimeout(timeoutId);

        // 200-299: success
        if (response.ok) {
          const data: ChatResponse = await response.json();
          return data;
        }

        // Parse error response
        let errorBody: ErrorResponse | undefined;
        try {
          errorBody = await response.json();
        } catch {
          // If response body is not JSON, use generic message
        }

        // 400-499: client errors (don't retry)
        if (response.status >= 400 && response.status < 500) {
          const message = mapErrorResponse(response.status, errorBody);
          throw new FetchAPIError(message, response.status, false);
        }

        // 5xx: server errors (retry)
        if (response.status >= 500) {
          const message = mapErrorResponse(response.status, errorBody);
          lastError = new FetchAPIError(message, response.status, true);

          // Continue to next retry
          if (attempt < MAX_RETRIES - 1) {
            const delay = getBackoffDelay(attempt);
            await sleep(delay);
          }
          continue;
        }

        // Other status codes
        throw new FetchAPIError(
          'Unexpected response from server',
          response.status,
          false
        );
      } finally {
        clearTimeout(timeoutId);
      }
    } catch (error) {
      // Handle AbortError (timeout)
      if (error instanceof DOMException && error.name === 'AbortError') {
        lastError = new FetchAPIError(
          'Request took too long. Please try again.',
          408,
          true
        );

        // Retry on timeout
        if (attempt < MAX_RETRIES - 1) {
          const delay = getBackoffDelay(attempt);
          await sleep(delay);
        }
        continue;
      }

      // Handle network errors
      if (error instanceof TypeError) {
        const message = error.message || 'Network error';

        // Log detailed network error for debugging
        if (process.env.NODE_ENV === 'development') {
          console.error('[RAGChatWidget] Network error:', {
            message,
            apiUrl,
            error: error.toString(),
          });
        }

        lastError = new FetchAPIError(
          'Unable to reach server. Please check your connection.',
          0,
          true
        );

        // Retry on network error
        if (attempt < MAX_RETRIES - 1) {
          const delay = getBackoffDelay(attempt);
          if (process.env.NODE_ENV === 'development') {
            console.log(`[RAGChatWidget] Retrying in ${delay}ms... (attempt ${attempt + 1}/${MAX_RETRIES})`);
          }
          await sleep(delay);
        }
        continue;
      }

      // Handle API errors (already mapped)
      if (error instanceof FetchAPIError) {
        lastError = error;

        // Only retry if error is retryable
        if (isRetryableError(error) && attempt < MAX_RETRIES - 1) {
          const delay = getBackoffDelay(attempt);
          await sleep(delay);
          continue;
        }

        // Don't retry
        throw error;
      }

      // Unknown error
      lastError = error as Error;
      throw error;
    }
  }

  // All retries exhausted
  if (lastError) {
    throw lastError;
  }

  throw new FetchAPIError('Request failed', 0, true);
}

/**
 * Validate a query request before sending to backend
 * Client-side validation reduces backend load
 */
export function validateQueryRequest(
  request: QueryRequest
): { valid: true } | { valid: false; error: string } {
  // Query is required
  if (!request.query || request.query.trim().length === 0) {
    return { valid: false, error: 'Please enter a question.' };
  }

  // Query max length
  if (request.query.length > 1000) {
    return {
      valid: false,
      error: 'Question is too long. Maximum 1000 characters.',
    };
  }

  // Optional: top_k validation
  if (request.top_k !== undefined) {
    if (request.top_k < 1 || request.top_k > 20) {
      return { valid: false, error: 'top_k must be between 1 and 20.' };
    }
  }

  // Optional: similarity_threshold validation
  if (request.similarity_threshold !== undefined) {
    if (
      request.similarity_threshold < 0 ||
      request.similarity_threshold > 1
    ) {
      return {
        valid: false,
        error: 'Similarity threshold must be between 0 and 1.',
      };
    }
  }

  // Optional: context max length
  if (request.context && request.context.length > 5000) {
    return {
      valid: false,
      error: 'Selected text is too long. Maximum 5000 characters.',
    };
  }

  return { valid: true };
}

/**
 * Check if backend is reachable (health check)
 * Used during initialization to verify backend connectivity
 */
export async function checkBackendHealth(apiUrl: string): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${apiUrl.replace('/ask', '')}/health`, {
      method: 'GET',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    return response.ok;
  } catch {
    return false;
  }
}
