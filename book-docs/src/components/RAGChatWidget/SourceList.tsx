/**
 * SourceList Component
 * Renders a list of retrieved source documents
 */

import React, { useCallback } from 'react';
import type { SourceListProps } from './types';
import { formatSourceDisplay } from '../../utils/formatters';
import styles from './RAGChatWidget.module.css';

/**
 * SourceList component
 * Shows retrieved sources with relevance scores and links
 */
export const SourceList: React.FC<SourceListProps> = ({
  sources,
  onSourceClick,
}) => {
  const handleSourceClick = useCallback(
    (sourceId: string, url: string) => {
      // Call the callback if provided
      if (onSourceClick) {
        const source = sources.find(s => s.chunk_id === sourceId);
        if (source) {
          onSourceClick(source);
        }
      }

      // Open link in new tab (don't navigate away from widget)
      window.open(url, '_blank', 'noopener,noreferrer');
    },
    [sources, onSourceClick]
  );

  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div
      className={styles.sourcesList}
      role="list"
      aria-label={`${sources.length} sources`}
    >
      {sources.map((source, index) => {
        const display = formatSourceDisplay(source);
        const sourceNumber = index + 1;

        return (
          <div
            key={source.chunk_id}
            className={styles.sourceItem}
            role="listitem"
          >
            {/* Source rank indicator */}
            <span
              className={styles.sourceRank}
              aria-label={`Source ${sourceNumber}`}
            >
              {sourceNumber}
            </span>

            {/* Source content */}
            <div className={styles.sourceContent}>
              {/* Title/Section */}
              <h5 className={styles.sourceTitle}>
                {display.title}
              </h5>

              {/* Snippet */}
              <p className={styles.sourceSnippet}>
                {display.snippet}
              </p>

              {/* Metadata */}
              <div className={styles.sourceMetadata}>
                <span
                  className={styles.relevanceScore}
                  title={`Relevance: ${display.relevance}`}
                >
                  📊 {display.relevance} match
                </span>
                <span
                  className={styles.sourceUrl}
                  title={display.url}
                >
                  📄 {display.url}
                </span>
              </div>

              {/* Read more link */}
              <button
                className={styles.sourceLink}
                onClick={() =>
                  handleSourceClick(source.chunk_id, source.source_url)
                }
                aria-label={`Read more from ${display.title}`}
                title={`Open ${display.title} in new tab`}
              >
                Read more →
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SourceList;
