/**
 * RAGChatWidget - Core TypeScript interfaces and types
 * Defines all data models used throughout the chatbot widget
 */

/**
 * Represents a single message in the chat conversation
 * Can be either a user query or an assistant response
 */
export interface ChatMessage {
  /** Unique identifier for the message (UUID or timestamp-based) */
  id: string;
  /** Role of the message author: 'user' for queries, 'assistant' for responses */
  role: 'user' | 'assistant';
  /** Message content text (max 10000 characters) */
  content: string;
  /** ISO 8601 timestamp when message was created */
  timestamp: string;
  /** Retrieved sources (present only in assistant messages) */
  sources?: RetrievalSource[];
  /** Original selected text from page (optional, user context for query) */
  selectedText?: string;
  /** Error message if request failed (optional) */
  error?: string;
  /** Additional metadata about the response */
  metadata?: {
    /** Time taken to generate response in milliseconds */
    durationMs?: number;
    /** Number of tokens used in generation */
    tokensUsed?: number;
    /** Number of context chunks used */
    contextUsed?: number;
  };
}

/**
 * Represents a single retrieved source document chunk
 * Returned by the backend with relevance score
 */
export interface RetrievalSource {
  /** Backend identifier for the chunk */
  chunk_id: string;
  /** Snippet of text from the source (truncate to 200 chars for display) */
  text: string;
  /** Relevance score from 0.0 (no match) to 1.0 (perfect match) */
  similarity_score: number;
  /** URL to the source document/page in Docusaurus */
  source_url: string;
  /** Chapter or section title of the source */
  section_title: string;
  /** Ranking position: 1 (most relevant) to 10 (least relevant) */
  rank: number;
}

/**
 * Request payload sent to the backend /ask endpoint
 * Contains the user query and optional context parameters
 */
export interface QueryRequest {
  /** The user's question (required, non-empty, max 1000 chars) */
  query: string;
  /** Number of top sources to retrieve (optional, default 5, range 1-20) */
  top_k?: number;
  /** Minimum similarity score threshold (optional, default 0.5, range 0.0-1.0) */
  similarity_threshold?: number;
  /** Selected text from page as context (optional, max 5000 chars) */
  context?: string;
  /** User identifier for future analytics (not used in MVP) */
  user_id?: string;
  /** Session identifier for correlation (not used in MVP) */
  session_id?: string;
}

/**
 * Response payload from the backend /ask endpoint
 * Contains the generated answer and supporting sources
 */
export interface ChatResponse {
  /** Unique request ID for tracing and debugging */
  request_id: string;
  /** Generated response text */
  answer: string;
  /** Array of retrieved sources (0-10 items) */
  sources: RetrievalSource[];
  /** Number of context chunks used in generation */
  context_used: number;
  /** Total tokens used in generation */
  tokens_used: number;
  /** Total time taken for backend processing in milliseconds */
  response_time_ms: number;
  /** ISO 8601 timestamp of response */
  timestamp: string;
  /** Optional metadata or notes from backend */
  note?: string;
}

/**
 * Error response from the backend
 * Returned when a request fails validation or processing
 */
export interface ErrorResponse {
  /** Error details object */
  detail: {
    /** Error type/category (e.g., "Validation Error", "Service Unavailable") */
    error: string;
    /** Array of field-specific error messages (if applicable) */
    details?: Array<{
      field: string;
      message: string;
    }>;
    /** Request ID for correlation with logs */
    request_id?: string;
  };
  /** Optional timestamp of error */
  timestamp?: string;
}

/**
 * Complete widget component state
 * Manages all internal state for the RAGChatWidget
 */
export interface WidgetState {
  /** Array of chat messages in conversation (max 50) */
  messages: ChatMessage[];
  /** Whether a request is currently in progress */
  isLoading: boolean;
  /** Error message if current operation failed */
  error: string | null;
  /** Currently selected text from page (if any) */
  selectedText: string | null;
  /** Whether widget is minimized/collapsed */
  isMinimized: boolean;
  /** Backend API endpoint URL */
  apiUrl: string;
  /** Unique session identifier (generated once on mount) */
  sessionId: string;
  /** Last query sent to backend (for reference) */
  lastRequest?: QueryRequest;
  /** Last response received from backend (for reference) */
  lastResponse?: ChatResponse;
}

/**
 * Props for the RAGChatWidget component
 * Configuration passed from parent (Docusaurus layout)
 */
export interface RAGChatWidgetProps {
  /** REQUIRED: Backend API endpoint URL (e.g., http://localhost:8000) */
  apiUrl: string;
  /** Position of widget on screen (default: 'bottom-right') */
  position?: 'bottom-right' | 'bottom-left' | 'top-right';
  /** Theme mode (default: 'auto' - follows Docusaurus theme) */
  theme?: 'light' | 'dark' | 'auto';
  /** Enable text selection capture feature (default: true) */
  enableTextSelection?: boolean;
  /** Maximum messages to keep in conversation (default: 50) */
  maxMessages?: number;
  /** Additional CSS classes to apply to widget */
  className?: string;
  /** Callback when an error occurs */
  onError?: (error: Error) => void;
}

/**
 * Props for QueryInput component
 * Handles user question submission
 */
export interface QueryInputProps {
  /** Callback when user submits a query */
  onSubmit: (query: string) => Promise<void>;
  /** Whether a request is currently processing */
  isLoading: boolean;
  /** Error message from previous request (if any) */
  error?: string | null;
  /** Currently captured selected text (if any) */
  selectedText?: string | null;
  /** Callback to clear selected text */
  onClearSelection?: () => void;
}

/**
 * Props for ResponseDisplay component
 * Shows the assistant's response
 */
export interface ResponseDisplayProps {
  /** The chat message to display */
  message: ChatMessage;
  /** Callback when user clicks on a source */
  onSourceClick?: (source: RetrievalSource) => void;
}

/**
 * Props for SourceList component
 * Shows retrieved source documents
 */
export interface SourceListProps {
  /** Array of sources to display */
  sources: RetrievalSource[];
  /** Callback when user clicks on a source */
  onSourceClick?: (source: RetrievalSource) => void;
}

/**
 * Validation result type
 * Returned by validation functions
 */
export type ValidationResult =
  | { success: true; data: any }
  | { success: false; error: string };

/**
 * API error type with status information
 */
export interface APIError extends Error {
  status: number;
  retry: boolean;
  timestamp?: string;
}

/**
 * Request status type
 * Tracks the state of an API request
 */
export type RequestStatus = 'idle' | 'loading' | 'success' | 'error';
