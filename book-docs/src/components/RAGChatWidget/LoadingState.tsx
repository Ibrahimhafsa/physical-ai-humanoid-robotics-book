/**
 * LoadingState Component
 * Renders a loading indicator while processing a request
 */

import React, { useState, useEffect } from 'react';
import { getLoadingMessage } from '../../utils/formatters';
import styles from './RAGChatWidget.module.css';

interface LoadingStateProps {
  /** Optional custom message (overrides auto-generated message) */
  message?: string;
  /** Show slow network indicator after this many milliseconds (default: 5000) */
  slowThreshold?: number;
}

/**
 * LoadingState component
 * Shows animated loading indicator with context-aware messages
 */
export const LoadingState: React.FC<LoadingStateProps> = ({
  message,
  slowThreshold = 5000,
}) => {
  const [elapsed, setElapsed] = useState(0);
  const [isSlowNetwork, setIsSlowNetwork] = useState(false);

  // Update elapsed time and detect slow network
  useEffect(() => {
    const interval = setInterval(() => {
      setElapsed(prev => {
        const newElapsed = prev + 100;
        if (newElapsed >= slowThreshold && !isSlowNetwork) {
          setIsSlowNetwork(true);
        }
        return newElapsed;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [isSlowNetwork, slowThreshold]);

  const displayMessage = message || getLoadingMessage(elapsed);

  return (
    <div className={styles.loadingContainer}>
      {/* Animated spinner */}
      <div className={styles.spinnerWrapper}>
        <div
          className={styles.spinner}
          role="status"
          aria-live="polite"
          aria-label="Loading"
        >
          <span className={styles.dot1}>●</span>
          <span className={styles.dot2}>●</span>
          <span className={styles.dot3}>●</span>
        </div>
      </div>

      {/* Loading message */}
      <p className={styles.loadingMessage}>
        {displayMessage}
      </p>

      {/* Slow network warning */}
      {isSlowNetwork && (
        <div
          className={styles.slowNetworkWarning}
          role="status"
          aria-live="polite"
        >
          ⚠️ This is taking longer than usual. Please wait...
        </div>
      )}

      {/* Elapsed time indicator (for debugging) */}
      {elapsed > 10000 && (
        <div
          className={styles.elapsedTime}
          aria-label={`Request in progress for ${(elapsed / 1000).toFixed(1)} seconds`}
        >
          {(elapsed / 1000).toFixed(1)}s
        </div>
      )}
    </div>
  );
};

export default LoadingState;
