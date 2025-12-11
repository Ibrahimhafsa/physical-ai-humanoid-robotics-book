/**
 * ResponseDisplay Component
 * Renders the assistant's response with sources
 */

import React from 'react';
import type { ResponseDisplayProps } from './types';
import { SourceList } from './SourceList';
import {
  formatTimestamp,
  formatResponseMetadata,
} from '../../utils/formatters';
import styles from './RAGChatWidget.module.css';

/**
 * ResponseDisplay component
 * Shows the assistant's answer and retrieved sources
 */
export const ResponseDisplay: React.FC<ResponseDisplayProps> = ({
  message,
  onSourceClick,
}) => {
  const isAssistant = message.role === 'assistant';
  const isUser = message.role === 'user';

  return (
    <div
      className={`${styles.message} ${isAssistant ? styles.assistantMessage : styles.userMessage}`}
      role={isAssistant ? 'region' : undefined}
      aria-label={isAssistant ? 'Assistant response' : 'Your question'}
    >
      {/* User message */}
      {isUser && (
        <div className={styles.messageContent}>
          <p>{message.content}</p>
          {message.selectedText && (
            <div className={styles.contextIndicator}>
              📌 Based on selected text
            </div>
          )}
          <span className={styles.timestamp}>
            {formatTimestamp(message.timestamp)}
          </span>
        </div>
      )}

      {/* Assistant message */}
      {isAssistant && (
        <div className={styles.messageContent}>
          {/* Answer */}
          <div
            className={styles.answerBox}
            role="region"
            aria-label="Answer"
            aria-live="polite"
          >
            <p>{message.content}</p>
          </div>

          {/* Metadata */}
          {message.sources && message.sources.length > 0 && (
            <div className={styles.metadata}>
              {formatResponseMetadata(
                message.sources.length,
                message.metadata?.durationMs || 0,
                message.metadata?.tokensUsed
              )}
            </div>
          )}

          {/* Sources */}
          {message.sources && message.sources.length > 0 && (
            <div className={styles.sourcesSection}>
              <h4 className={styles.sourcesTitle}>Sources</h4>
              <SourceList
                sources={message.sources}
                onSourceClick={onSourceClick}
              />
            </div>
          )}

          {/* Empty sources message */}
          {message.sources && message.sources.length === 0 && (
            <div
              className={styles.emptySourcesNote}
              role="note"
            >
              No specific sources found. This is a general response.
            </div>
          )}

          <span className={styles.timestamp}>
            {formatTimestamp(message.timestamp)}
          </span>
        </div>
      )}

      {/* Error message */}
      {message.error && (
        <div
          className={styles.errorBox}
          role="alert"
        >
          <span className={styles.errorIcon}>⚠️</span>
          <span>{message.error}</span>
        </div>
      )}
    </div>
  );
};

export default ResponseDisplay;
