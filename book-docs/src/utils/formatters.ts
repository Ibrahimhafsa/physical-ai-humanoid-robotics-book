/**
 * Formatter utilities for RAG Chat Widget
 * Handles text formatting, URL formatting, and user-friendly text generation
 */

import type { RetrievalSource } from '../components/RAGChatWidget/types';

/**
 * Format the assistant's answer for display
 * Handles text truncation and cleanup
 */
export function formatAnswer(answer: string, maxChars = 10000): string {
  if (!answer) {
    return '';
  }

  let formatted = answer.trim();

  // Truncate if too long
  if (formatted.length > maxChars) {
    formatted = formatted.substring(0, maxChars) + '...';
  }

  // Convert markdown-like bold/italic to HTML (optional, depends on display)
  // For now, just return cleaned text
  return formatted;
}

/**
 * Format source URL for display
 * Extracts readable path from full URL
 */
export function formatSourceUrl(url: string): string {
  try {
    const urlObj = new URL(url, window.location.origin);
    const path = urlObj.pathname;

    // Remove leading/trailing slashes and split
    const parts = path.split('/').filter(Boolean);

    // Return last 2-3 meaningful parts (e.g., "docs/guide/setup")
    if (parts.length > 2) {
      return parts.slice(-2).join('/');
    }

    return path || 'Document';
  } catch {
    // If URL is relative, just return it
    return url || 'Document';
  }
}

/**
 * Format similarity score for display as percentage
 * Converts 0.0-1.0 to 0-100%
 */
export function formatSimilarityScore(score: number): string {
  const percentage = Math.round(score * 100);
  return `${percentage}%`;
}

/**
 * Format timestamp for display
 * Shows relative time (e.g., "2 minutes ago") or full timestamp
 */
export function formatTimestamp(isoString: string): string {
  try {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();

    // Less than 1 minute
    if (diffMs < 60000) {
      return 'just now';
    }

    // Less than 1 hour
    if (diffMs < 3600000) {
      const mins = Math.floor(diffMs / 60000);
      return `${mins} ${mins === 1 ? 'minute' : 'minutes'} ago`;
    }

    // Less than 24 hours
    if (diffMs < 86400000) {
      const hours = Math.floor(diffMs / 3600000);
      return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
    }

    // Format as date
    return date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return isoString;
  }
}

/**
 * Truncate text to a maximum length with ellipsis
 * Tries to cut at word boundary if possible
 */
export function truncateText(text: string, maxChars = 200): string {
  if (!text || text.length <= maxChars) {
    return text;
  }

  // Try to cut at word boundary
  const truncated = text.substring(0, maxChars);
  const lastSpace = truncated.lastIndexOf(' ');

  if (lastSpace > maxChars * 0.8) {
    // If last space is reasonably close, use it
    return truncated.substring(0, lastSpace) + '...';
  }

  // Otherwise, just truncate and add ellipsis
  return truncated + '...';
}

/**
 * Format source snippet for display
 * Truncates to reasonable length with ellipsis
 */
export function formatSourceSnippet(text: string): string {
  return truncateText(text, 200);
}

/**
 * Format error message for user display
 * Cleans up technical jargon
 */
export function formatErrorMessage(error: string | Error): string {
  if (error instanceof Error) {
    // Use custom message if available
    if (error.message) {
      return error.message;
    }
    return 'An unexpected error occurred.';
  }

  if (typeof error === 'string') {
    // Clean up common error messages
    if (error.includes('CORS')) {
      return 'Unable to reach the server. Please check the API configuration.';
    }
    if (error.includes('timeout') || error.includes('timed out')) {
      return 'Request took too long. Please try again.';
    }
    if (error.includes('network')) {
      return 'Network error. Please check your connection.';
    }

    return error;
  }

  return 'An unexpected error occurred.';
}

/**
 * Format source for display in source list
 * Returns friendly text for each source
 */
export function formatSourceDisplay(source: RetrievalSource): {
  title: string;
  snippet: string;
  relevance: string;
  url: string;
} {
  return {
    title: source.section_title || 'Untitled Section',
    snippet: formatSourceSnippet(source.text),
    relevance: formatSimilarityScore(source.similarity_score),
    url: formatSourceUrl(source.source_url),
  };
}

/**
 * Format selected text for display
 * Shows truncated version with indicator
 */
export function formatSelectedTextDisplay(text: string | null): string {
  if (!text) {
    return '';
  }

  const truncated = truncateText(text, 100);
  return `📌 "${truncated}"`;
}

/**
 * Generate loading message based on elapsed time
 * Shows different messages to keep user engaged
 */
export function getLoadingMessage(elapsedMs: number): string {
  const seconds = Math.floor(elapsedMs / 1000);

  if (seconds < 2) {
    return 'Searching...';
  }
  if (seconds < 5) {
    return 'Finding relevant sources...';
  }
  if (seconds < 10) {
    return 'Generating response...';
  }
  return 'Still working on that...';
}

/**
 * Format response metadata for display
 * Shows sources count, processing time, etc.
 */
export function formatResponseMetadata(
  sourcesCount: number,
  responseTimeMs: number,
  tokensUsed?: number
): string {
  const sources =
    sourcesCount === 1 ? '1 source' : `${sourcesCount} sources`;
  const time = (responseTimeMs / 1000).toFixed(1);

  let metadata = `Generated from ${sources} in ${time}s`;

  if (tokensUsed) {
    metadata += ` (${tokensUsed} tokens)`;
  }

  return metadata;
}

/**
 * Escape HTML special characters for safe display
 */
export function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Convert selected text to search query
 * Cleans up whitespace and special characters
 */
export function normalizeSelectedText(text: string): string {
  return text
    .trim()
    .replace(/\s+/g, ' ') // Multiple spaces to single space
    .substring(0, 5000); // Max length for context
}
