/**
 * QueryInput Component
 * Renders the user input form for asking questions
 * Handles text input, submission, and selected text display
 */

import React, { useState, useRef, useCallback } from 'react';
import type { QueryInputProps } from './types';
import { formatSelectedTextDisplay } from '../../utils/formatters';
import styles from './RAGChatWidget.module.css';

/**
 * QueryInput component
 * Manages user question submission with support for selected text context
 */
export const QueryInput: React.FC<QueryInputProps> = ({
  onSubmit,
  isLoading,
  error,
  selectedText,
  onClearSelection,
}) => {
  const [inputValue, setInputValue] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  /**
   * Handle form submission
   * Validates input, calls onSubmit, then clears input
   */
  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      const query = inputValue.trim();
      if (!query) {
        return;
      }

      setSubmitting(true);
      try {
        await onSubmit(query);
        setInputValue(''); // Clear input on success
        inputRef.current?.focus(); // Return focus to input
      } finally {
        setSubmitting(false);
      }
    },
    [inputValue, onSubmit]
  );

  /**
   * Handle input change
   */
  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setInputValue(e.target.value);
    },
    []
  );

  /**
   * Handle clear selected text
   */
  const handleClearSelection = useCallback(() => {
    onClearSelection?.();
  }, [onClearSelection]);

  const isDisabled = isLoading || submitting;
  const hasQuery = inputValue.trim().length > 0;

  return (
    <form onSubmit={handleSubmit} className={styles.queryForm}>
      {/* Error message display */}
      {error && (
        <div
          className={styles.errorBox}
          role="alert"
          aria-live="polite"
        >
          <span className={styles.errorIcon}>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Selected text display */}
      {selectedText && (
        <div className={styles.selectedTextBox}>
          <span className={styles.selectedTextLabel}>
            {formatSelectedTextDisplay(selectedText)}
          </span>
          <button
            type="button"
            onClick={handleClearSelection}
            className={styles.clearButton}
            aria-label="Clear selected text"
            title="Clear selected text"
          >
            ✕
          </button>
        </div>
      )}

      {/* Input field container */}
      <div className={styles.inputContainer}>
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Ask a question..."
          disabled={isDisabled}
          maxLength={1000}
          className={styles.inputField}
          aria-label="Enter your question"
          aria-describedby={error ? 'error-message' : undefined}
          aria-busy={isLoading}
        />

        {/* Submit button */}
        <button
          type="submit"
          disabled={isDisabled || !hasQuery}
          className={styles.submitButton}
          aria-label={isLoading ? 'Thinking...' : 'Ask'}
          title={isLoading ? 'Processing request...' : 'Submit question'}
        >
          {isLoading ? (
            <>
              <span className={styles.spinner} aria-hidden="true">
                ⊙
              </span>
              Thinking...
            </>
          ) : (
            <>
              <span aria-hidden="true">→</span> Ask
            </>
          )}
        </button>
      </div>

      {/* Character counter */}
      {inputValue.length > 0 && (
        <div className={styles.charCount}>
          {inputValue.length}/1000
        </div>
      )}
    </form>
  );
};

export default QueryInput;
