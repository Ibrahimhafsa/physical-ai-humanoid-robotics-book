/**
 * ErrorState Component
 * Renders error messages with retry/recovery options
 */

import React, { useCallback } from 'react';
import { formatErrorMessage } from '../../utils/formatters';
import styles from './RAGChatWidget.module.css';

interface ErrorStateProps {
  /** Error message or Error object */
  error: string | Error;
  /** Optional callback to retry the operation */
  onRetry?: () => void;
  /** Optional callback to dismiss the error */
  onDismiss?: () => void;
  /** Whether a retry is currently in progress */
  isRetrying?: boolean;
}

/**
 * ErrorState component
 * Shows error message with friendly formatting and recovery options
 */
export const ErrorState: React.FC<ErrorStateProps> = ({
  error,
  onRetry,
  onDismiss,
  isRetrying = false,
}) => {
  const message = formatErrorMessage(error);

  const handleRetry = useCallback(() => {
    onRetry?.();
  }, [onRetry]);

  const handleDismiss = useCallback(() => {
    onDismiss?.();
  }, [onDismiss]);

  // Determine error icon based on message
  const getErrorIcon = (msg: string): string => {
    if (msg.includes('network') || msg.includes('connection')) {
      return '🌐';
    }
    if (msg.includes('timeout') || msg.includes('slow')) {
      return '⏱️';
    }
    if (msg.includes('unavailable')) {
      return '🔧';
    }
    if (msg.includes('invalid') || msg.includes('valid')) {
      return '✗';
    }
    return '⚠️';
  };

  return (
    <div
      className={styles.errorState}
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      {/* Error icon and message */}
      <div className={styles.errorContent}>
        <span
          className={styles.errorIcon}
          aria-hidden="true"
        >
          {getErrorIcon(message)}
        </span>
        <div>
          <h4 className={styles.errorTitle}>
            Something went wrong
          </h4>
          <p className={styles.errorMessage}>
            {message}
          </p>
        </div>
      </div>

      {/* Action buttons */}
      <div className={styles.errorActions}>
        {/* Retry button */}
        {onRetry && (
          <button
            onClick={handleRetry}
            disabled={isRetrying}
            className={`${styles.errorButton} ${styles.retryButton}`}
            aria-label="Retry request"
            title="Try the request again"
          >
            {isRetrying ? (
              <>
                <span
                  className={styles.spinner}
                  aria-hidden="true"
                >
                  ⊙
                </span>
                Retrying...
              </>
            ) : (
              <>
                <span aria-hidden="true">↻</span> Retry
              </>
            )}
          </button>
        )}

        {/* Dismiss button */}
        {onDismiss && (
          <button
            onClick={handleDismiss}
            className={`${styles.errorButton} ${styles.dismissButton}`}
            aria-label="Dismiss error"
            title="Dismiss this error message"
          >
            <span aria-hidden="true">✕</span> Dismiss
          </button>
        )}
      </div>

      {/* Troubleshooting tips */}
      <div className={styles.troubleshootingTips}>
        <p className={styles.tipsTitle}>
          💡 If the problem persists:
        </p>
        <ul className={styles.tipsList}>
          <li>Check your internet connection</li>
          <li>Refresh the page</li>
          <li>Try again in a few moments</li>
          {message.includes('API') && (
            <li>
              Verify the backend API is running at the correct
              URL
            </li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ErrorState;
