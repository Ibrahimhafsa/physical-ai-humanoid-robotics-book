/**
 * RAG Chat Widget
 * Main component for the chatbot widget
 * Manages state, API calls, and component orchestration
 */

import React, {
  useState,
  useCallback,
  useEffect,
  useRef,
  useMemo,
} from 'react';
import type {
  RAGChatWidgetProps,
  ChatMessage,
  QueryRequest,
} from './types';
import { QueryInput } from './QueryInput';
import { ResponseDisplay } from './ResponseDisplay';
import { LoadingState } from './LoadingState';
import { ErrorState } from './ErrorState';
import { fetchQuery, validateQueryRequest } from '../../utils/apiClient';
import { normalizeSelectedText } from '../../utils/formatters';
import styles from './RAGChatWidget.module.css';


/**
 * RAGChatWidget - Main chatbot component
 * Renders the complete widget with input, responses, and state management
 */
export const RAGChatWidget: React.FC<RAGChatWidgetProps> = ({
  apiUrl,
  position = 'bottom-right',
  theme = 'auto',
  enableTextSelection = true,
  maxMessages = 50,
  className,
  onError,
}) => {
  // State management
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  /**
   * Auto-scroll to latest message
   */
  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  /**
   * Handle text selection from page
   */
  useEffect(() => {
    if (!enableTextSelection) return;

    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString();

      if (text && text.trim().length > 0) {
        const normalized = normalizeSelectedText(text);
        setSelectedText(normalized);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [enableTextSelection]);

  /**
   * Clear selected text
   */
  const handleClearSelection = useCallback(() => {
    setSelectedText(null);
  }, []);

  /**
   * Handle query submission
   */
  const handleSubmitQuery = useCallback(
    async (query: string) => {
      // Validate query
      const validation = validateQueryRequest({ query });
      if (!validation.valid) {
        setError(validation.error);
        return;
      }

      // Create request
      const request: QueryRequest = {
        query,
        top_k: 5,
        similarity_threshold: 0.5,
        context: selectedText || undefined,
      };

      // Add user message
      const userMessage: ChatMessage = {
        id: `msg-${Date.now()}`,
        role: 'user',
        content: query,
        timestamp: new Date().toISOString(),
        selectedText: selectedText || undefined,
      };

      setMessages(prev => {
        const updated = [...prev, userMessage];
        // Trim to max messages
        if (updated.length > maxMessages) {
          return updated.slice(-maxMessages);
        }
        return updated;
      });

      setError(null);
      setIsLoading(true);

      try {
        // Create abort controller for this request
        abortControllerRef.current = new AbortController();

        // Call API
        const response = await fetchQuery(request, apiUrl);

        // Check if component is still mounted (not aborted)
        if (!abortControllerRef.current.signal.aborted) {
          // Add assistant message
          const assistantMessage: ChatMessage = {
            id: `msg-${Date.now()}`,
            role: 'assistant',
            content: response.answer,
            timestamp: response.timestamp,
            sources: response.sources,
            metadata: {
              durationMs: response.response_time_ms,
              tokensUsed: response.tokens_used,
              contextUsed: response.context_used,
            },
          };

          setMessages(prev => {
            const updated = [...prev, assistantMessage];
            if (updated.length > maxMessages) {
              return updated.slice(-maxMessages);
            }
            return updated;
          });

          // Clear selected text after successful request
          setSelectedText(null);
        }
      } catch (err) {
        // Don't update state if request was aborted
        if (
          err instanceof Error &&
          err.name === 'AbortError'
        ) {
          return;
        }

        const errorMessage =
          err instanceof Error
            ? err.message
            : 'An unexpected error occurred.';

        setError(errorMessage);

        // Call error callback if provided
        if (onError) {
          onError(
            err instanceof Error
              ? err
              : new Error(errorMessage)
          );
        }
      } finally {
        setIsLoading(false);
        abortControllerRef.current = null;
      }
    },
    [apiUrl, selectedText, maxMessages, onError]
  );

  /**
   * Cleanup on unmount
   */
  useEffect(() => {
    return () => {
      // Abort any in-flight requests
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  /**
   * Handle source click - navigate to source
   */
  const handleSourceClick = useCallback((source: any) => {
    // Open source URL in new tab
    window.open(source.source_url, '_blank', 'noopener,noreferrer');
  }, []);

  /**
   * Retry last message
   */
  const handleRetry = useCallback(async () => {
    const lastUserMessage = [...messages]
      .reverse()
      .find(m => m.role === 'user');

    if (lastUserMessage) {
      await handleSubmitQuery(lastUserMessage.content);
    }
  }, [messages, handleSubmitQuery]);

  /**
   * Clear conversation
   */
  const handleClearConversation = useCallback(() => {
    if (
      window.confirm(
        'Clear conversation history? This cannot be undone.'
      )
    ) {
      setMessages([]);
      setError(null);
      setSelectedText(null);
    }
  }, []);

  /**
   * Toggle minimized state
   */
  const handleToggleMinimize = useCallback(() => {
    setIsMinimized(prev => !prev);
  }, []);

  // Determine theme class
  const themeClass = useMemo(() => {
    if (theme === 'auto') {
      // Detect dark mode from Docusaurus
      const isDark =
        typeof document !== 'undefined' &&
        document.documentElement.getAttribute('data-theme') === 'dark';
      return isDark ? 'dark' : 'light';
    }
    return theme;
  }, [theme]);

  // Widget container class
  const positionClass =
    position === 'bottom-right'
      ? styles.positionBottomRight
      : position === 'bottom-left'
        ? styles.positionBottomLeft
        : styles.positionTopRight;

  const themeStyleClass =
    themeClass === 'dark'
      ? styles.themeDark
      : styles.themeLight;

  const containerClass = [
    styles.widget,
    positionClass,
    themeStyleClass,
    isMinimized && styles.minimized,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      className={containerClass}
      data-testid="rag-chat-widget"
      aria-label="RAG Chat Widget"
      role="region"
    >
      {/* Header */}
      <div className={styles.header}>
        <h3 className={styles.title}>💬 Ask</h3>
        <div className={styles.headerActions}>
          <button
            onClick={handleToggleMinimize}
            className={styles.minimizeButton}
            aria-label={
              isMinimized ? 'Expand widget' : 'Minimize widget'
            }
            title={isMinimized ? 'Expand' : 'Minimize'}
          >
            {isMinimized ? '▲' : '▼'}
          </button>
        </div>
      </div>

      {/* Main content (hidden when minimized) */}
      {!isMinimized && (
        <div className={styles.content}>
          {/* Messages area */}
          <div className={styles.messagesArea}>
            {messages.length === 0 && !error && (
              <div className={styles.emptyState}>
                <p className={styles.emptyMessage}>
                  👋 Hi! Ask me anything about this content.
                </p>
                <p className={styles.emptySubtext}>
                  {enableTextSelection
                    ? 'Select text on the page or type a question below.'
                    : 'Type a question below.'}
                </p>
              </div>
            )}

            {messages.map(message => (
              <ResponseDisplay
                key={message.id}
                message={message}
                onSourceClick={handleSourceClick}
              />
            ))}

            {isLoading && <LoadingState />}

            {error && !isLoading && (
              <ErrorState
                error={error}
                onRetry={messages.length > 0 ? handleRetry : undefined}
                onDismiss={() => setError(null)}
              />
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Query input */}
          <QueryInput
            onSubmit={handleSubmitQuery}
            isLoading={isLoading}
            error={
              messages.length > 0 ? null : error
            }
            selectedText={selectedText}
            onClearSelection={handleClearSelection}
          />

          {/* Footer with clear button */}
          {messages.length > 0 && (
            <div className={styles.footer}>
              <button
                onClick={handleClearConversation}
                className={styles.clearButton}
                aria-label="Clear conversation"
                title="Clear all messages"
              >
                🗑️ Clear
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RAGChatWidget;
