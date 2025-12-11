# Data Model: Frontend Integration with RAG Agent API

**Feature**: 005-frontend-integration | **Date**: 2025-12-12 | **Phase**: Phase 1 Design

## Entity Definitions

### 1. ChatMessage (Internal Widget State)

Represents a single message in the widget's conversation history.

```typescript
interface ChatMessage {
  id: string;                         // UUID or timestamp-based unique ID
  role: 'user' | 'assistant';         // Sender (user=reader, assistant=backend)
  content: string;                    // Text content (answer or query)
  timestamp: Date;                    // When sent/received
  sources?: RetrievalSource[];        // Populated only for assistant messages
  selectedText?: string;               // Optional: text user selected when asking query
  error?: string;                     // Optional: error message if request failed
  requestId?: string;                 // Optional: request_id from backend (for tracing)
  metadata?: {
    durationMs?: number;              // Time taken to receive response
    tokensUsed?: number;              // Token count from backend
    contextUsed?: number;             // Number of sources used
  };
}
```

**Constraints**:
- `id`: Required, unique per widget instance
- `role`: Required, one of two values
- `content`: Required, non-empty string, max 10,000 chars (truncate if longer)
- `timestamp`: Required, ISO 8601 format recommended
- `sources`: Array of RetrievalSource, max 10 items (from backend response)
- `selectedText`: Optional, max 5,000 chars (truncate if user selects >5K)
- `error`: Optional, user-friendly error message (non-technical)

**Validation Rules**:
- Messages with role='user' MUST have non-empty `content`
- Messages with role='assistant' SHOULD have `sources` (unless error occurred)
- Messages with `error` set indicate failed request (content may be partial/empty)
- `timestamp` MUST be valid Date object

**Usage**:
- Stored in widget component state: `messages: ChatMessage[]`
- Each submitted query creates ChatMessage with role='user'
- Each response from backend creates ChatMessage with role='assistant'
- Max 50 messages retained in memory (older messages discarded to prevent memory bloat)

---

### 2. RetrievalSource (From Backend Response)

Represents a single chunk of text retrieved from the book by the backend.

```typescript
interface RetrievalSource {
  chunk_id: string;                   // Backend-assigned chunk identifier
  text: string;                       // Snippet preview (truncated to 200 chars for display)
  similarity_score: number;           // Float 0.0-1.0, confidence that chunk matches query
  source_url: string;                 // Docusaurus page URL (e.g., /docs/01-fundamentals/physical-ai)
  section_title: string;              // Chapter/section name (e.g., "What is Physical AI?")
  rank: number;                       // Order: 1 = most relevant, 10 = least relevant
}
```

**Constraints**:
- All fields required, non-empty
- `similarity_score`: Range 0.0-1.0 (validated on receive)
- `text`: Truncate to 200 chars for UI display (preserve full text in data)
- `source_url`: Must be valid URL path (starts with /)
- `rank`: Positive integer, 1-indexed

**Validation Rules**:
- Validate `chunk_id` matches backend format (non-empty string)
- Validate `similarity_score` is float in range
- Validate `source_url` is absolute or relative Docusaurus path
- Log warning if rank > 10 (unexpected from backend)

**Display**:
- Show as list item in ResponseDisplay component
- Each source is clickable link to source_url
- Display format: "Section: similarity_score% (rank #N)"
- Truncate long section_title with ellipsis

**Example**:
```typescript
const source: RetrievalSource = {
  chunk_id: "chunk_001",
  text: "Physical AI is the study of intelligence in physical systems and robots...",
  similarity_score: 0.89,
  source_url: "/docs/01-fundamentals/physical-ai",
  section_title: "What is Physical AI?",
  rank: 1
};
```

---

### 3. QueryRequest (Sent to Backend)

Payload sent from widget to backend `/ask` endpoint.

```typescript
interface QueryRequest {
  query: string;                      // User question (required)
  top_k?: number;                     // Number of chunks to retrieve (default: 5, range: 1-20)
  similarity_threshold?: number;      // Minimum similarity score (default: 0.5, range: 0.0-1.0)
  context?: string;                   // Optional: selected text to include as context
  user_id?: string;                   // Optional: anonymous user ID (not MVP, for future)
  session_id?: string;                // Optional: session ID (not MVP, for future)
}
```

**Constraints**:
- `query`: Required, non-empty, non-whitespace, max 1,000 chars
- `top_k`: Optional, default 5, range [1, 20]
- `similarity_threshold`: Optional, default 0.5, range [0.0, 1.0]
- `context`: Optional, max 5,000 chars (truncated if user selects larger)
- `user_id`: Optional (reserved for future, not used in MVP)
- `session_id`: Optional (reserved for future, not used in MVP)

**Validation (Client-Side)**:
```typescript
function validateQueryRequest(request: QueryRequest): string | null {
  // Required: query
  if (!request.query || !request.query.trim()) {
    return "Please enter a question before asking.";
  }
  if (request.query.length > 1000) {
    return "Question too long (max 1000 chars).";
  }

  // Optional: top_k
  if (request.top_k && (request.top_k < 1 || request.top_k > 20)) {
    return "Invalid top_k (must be 1-20).";
  }

  // Optional: similarity_threshold
  if (request.similarity_threshold && (request.similarity_threshold < 0 || request.similarity_threshold > 1)) {
    return "Invalid similarity threshold (must be 0.0-1.0).";
  }

  // Optional: context
  if (request.context && request.context.length > 5000) {
    // Silently truncate
    request.context = request.context.substring(0, 5000);
  }

  return null;  // Valid
}
```

**Serialization** (to JSON):
```json
{
  "query": "What is kinematics in robotics?",
  "top_k": 5,
  "similarity_threshold": 0.5,
  "context": "The chapter mentions motion and forces..."
}
```

---

### 4. ChatResponse (From Backend)

Payload received from backend `/ask` endpoint.

```typescript
interface ChatResponse {
  request_id: string;                 // UUID for tracing (same as in header)
  answer: string;                     // Generated answer text
  sources: RetrievalSource[];         // Array of retrieved chunks (0-10 items)
  context_used: number;               // Count of chunks included in context assembly
  tokens_used: number;                // Estimated token count of response
  response_time_ms: number;           // Latency from request to response
  timestamp: string;                  // ISO 8601 timestamp
  note?: string;                      // Optional: metadata notes (e.g., "No chunks above similarity threshold")
}
```

**Constraints**:
- All fields except `note` are required
- `request_id`: String (UUID format, for tracing)
- `answer`: Non-empty string, may be very long (up to 5,000+ chars)
- `sources`: Array of RetrievalSource, 0-10 items
- `context_used`: Non-negative integer
- `tokens_used`: Non-negative integer
- `response_time_ms`: Non-negative integer (milliseconds)
- `timestamp`: ISO 8601 timestamp string
- `note`: Optional, free-form string

**Validation (Client-Side)**:
```typescript
function validateChatResponse(response: any): ChatResponse {
  // Type validation
  if (!response.request_id || typeof response.request_id !== 'string') {
    throw new Error("Missing or invalid request_id");
  }
  if (!response.answer || typeof response.answer !== 'string') {
    throw new Error("Missing or invalid answer");
  }
  if (!Array.isArray(response.sources)) {
    throw new Error("Missing or invalid sources");
  }

  // Validation of sources
  response.sources.forEach((source: any, index: number) => {
    if (!source.chunk_id || !source.text || typeof source.similarity_score !== 'number') {
      throw new Error(`Invalid source at index ${index}`);
    }
  });

  return response as ChatResponse;
}
```

**Edge Cases**:
- Empty sources (user's query has no relevant chunks) → Display friendly message
- Very long answer (>5,000 chars) → Use scrollable container in UI
- Response latency >5s → Show "Still loading..." message
- Missing optional fields → Treat as undefined, don't error

**Example**:
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "answer": "Kinematics is the study of motion in mechanical systems...",
  "sources": [
    {
      "chunk_id": "chunk_005",
      "text": "Kinematics describes motion without considering forces...",
      "similarity_score": 0.92,
      "source_url": "/docs/02-humanoid-robotics/kinematics-dynamics",
      "section_title": "Kinematics Fundamentals",
      "rank": 1
    }
  ],
  "context_used": 3,
  "tokens_used": 287,
  "response_time_ms": 1850,
  "timestamp": "2025-12-12T14:30:00Z"
}
```

---

### 5. ErrorResponse (From Backend on Errors)

Payload received when backend returns error (400, 503, 500).

```typescript
interface ErrorResponse {
  detail: {
    error: string;                    // Error type (e.g., "Validation Error")
    details?: Array<{
      field?: string;                 // Field that failed validation
      message: string;                // Friendly error message
    }>;
    request_id?: string;              // For tracing
  };
  timestamp?: string;                 // ISO 8601 timestamp
}
```

**Examples**:

**400 Validation Error**:
```json
{
  "detail": {
    "error": "Validation Error",
    "details": [
      {
        "field": "query",
        "message": "Query cannot be empty"
      }
    ],
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**503 Service Unavailable**:
```json
{
  "detail": {
    "error": "Service Unavailable",
    "message": "Qdrant database connection failed",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

### 6. WidgetState (React Component State)

Internal state of RAGChatWidget component.

```typescript
interface WidgetState {
  messages: ChatMessage[];            // Conversation history (max 50)
  isLoading: boolean;                 // Request in flight
  error: string | null;               // Current error message (if any)
  selectedText: string | null;        // Currently selected text on page
  isMinimized: boolean;               // Widget collapsed/expanded
  apiUrl: string;                     // Backend `/ask` endpoint URL
  sessionId: string;                  // Generated session ID for this widget instance
  lastRequest?: QueryRequest;         // Last submitted request (for retry)
  lastResponse?: ChatResponse;        // Last received response
}
```

**Derived State** (computed from above):
```typescript
interface DerivedState {
  canSubmit: boolean;                 // true if not loading and input valid
  hasError: boolean;                  // true if error message exists
  isEmptyHistory: boolean;            // true if no messages yet
  lastMessage?: ChatMessage;          // Most recent message
  displayHeight: number;              // CSS height in pixels
}
```

**State Transitions**:

```
IDLE → LOADING (user submits query)
LOADING → SUCCESS (backend returns 200 with sources)
LOADING → ERROR (backend returns 400/503/500)
LOADING → ERROR (network timeout or fetch error)
ERROR → IDLE (user clicks retry)
SUCCESS → IDLE (user opens new query)
MINIMIZED (user clicks close button) → EXPANDED (user clicks open)
```

**State Management** (React hooks):
```typescript
const [messages, setMessages] = useState<ChatMessage[]>([]);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [selectedText, setSelectedText] = useState<string | null>(null);
const [isMinimized, setIsMinimized] = useState(false);
const [sessionId] = useState(generateSessionId()); // Once on mount
```

---

## Component Props & Interfaces

### RAGChatWidget Props

```typescript
interface RAGChatWidgetProps {
  apiUrl: string;                     // REQUIRED: Backend endpoint
  position?: 'bottom-right' | 'bottom-left' | 'top-right';
  theme?: 'light' | 'dark' | 'auto';  // Default: 'auto' (from Docusaurus)
  enableTextSelection?: boolean;      // Default: true
  maxMessages?: number;               // Default: 50
  className?: string;                 // Optional: CSS class for custom styling
  onError?: (error: Error) => void;   // Optional: callback on errors
}
```

### QueryInput Props

```typescript
interface QueryInputProps {
  onSubmit: (query: string, selectedText?: string) => void;
  isLoading: boolean;
  error?: string;
  selectedText?: string;
  onClearSelection: () => void;
}
```

### ResponseDisplay Props

```typescript
interface ResponseDisplayProps {
  message: ChatMessage;
  onSourceClick?: (sourceUrl: string) => void;
}
```

### SourceList Props

```typescript
interface SourceListProps {
  sources: RetrievalSource[];
  onSourceClick?: (sourceUrl: string) => void;
}
```

---

## Validation Rules Summary

| Entity | Field | Rule | Example |
|--------|-------|------|---------|
| ChatMessage | id | Unique, non-empty | UUID or timestamp |
| ChatMessage | role | One of: 'user', 'assistant' | 'user' |
| ChatMessage | content | Non-empty, max 10K | "What is kinematics?" |
| QueryRequest | query | Non-empty, non-whitespace, max 1K | "What is kinematics?" |
| QueryRequest | top_k | Range [1, 20] | 5 |
| QueryRequest | similarity_threshold | Range [0.0, 1.0] | 0.5 |
| QueryRequest | context | Optional, max 5K | "Motion in systems..." |
| RetrievalSource | chunk_id | Non-empty string | "chunk_001" |
| RetrievalSource | similarity_score | Range [0.0, 1.0] | 0.89 |
| ChatResponse | request_id | UUID format | "550e8400-..." |
| ChatResponse | answer | Non-empty string | "Kinematics is..." |
| ChatResponse | sources | Array, 0-10 items | [...] |

---

## Next Steps

1. ✅ Data model complete
2. Create `contracts/component-interface.md` (component API)
3. Create `contracts/request-response-examples.md` (example payloads)
4. Create `quickstart.md` (setup guide)
5. Proceed to Phase 2: Task generation
