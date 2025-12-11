# Implementation Plan: Docusaurus Frontend Integration with RAG Agent API

**Branch**: `005-frontend-integration` | **Date**: 2025-12-12 | **Spec**: [specs/005-frontend-integration/spec.md](spec.md)

**Input**:
- Create `/src/components/RAGChatWidget` in Docusaurus
- Add API call util to POST queries to FastAPI backend
- Implement UI with input box + selected-text injection
- Add global layout plugin to mount the widget
- Test full request cycle with local backend

## Summary

Build a React-based chatbot widget that integrates seamlessly into Docusaurus, enabling readers to ask questions about book content and receive context-grounded answers from the RAG Agent API (Feature 004). The widget captures user queries and optional selected text, sends them to the backend `/ask` endpoint, displays responses with source attribution, and provides clear feedback for loading, errors, and empty results. Architecture emphasizes minimal disruption to existing theme, responsive design, keyboard accessibility, and graceful error handling. Widget is globally injected via Docusaurus layout plugin, appears on all pages, respects light/dark theme switching, and remains functional during navigation.

## Technical Context

**Language/Framework**: React 18+ with Hooks (TypeScript recommended)

**Primary Dependencies**:
- **React** 18+ - Component library
- **Docusaurus** 2.x/3.x - Static site generation and theme infrastructure
- **Fetch API** - HTTP client (no external library required, uses native browser API)
- **CSS Modules** or **Tailwind CSS** - Styling (must inherit Docusaurus theme tokens)
- *Optional*: **@docusaurus/theme-common** - Access to dark mode state and theme context

**Storage**: Browser memory only (no localStorage for MVP; optional for session state persistence)

**Testing**: Jest + React Testing Library for unit/integration tests, manual testing with local FastAPI backend

**Target Platform**: Browser (Chrome, Firefox, Safari, Edge latest 2 versions), mobile browsers (iOS Safari, Chrome Mobile)

**Project Type**: Frontend widget embedded in Docusaurus

**Performance Goals**:
- Widget load time: <500ms (lazy load recommended)
- Backend request latency: <5s p95 (inherited from Feature 004)
- UI response to user input: <100ms (input debouncing recommended for text selection)
- Widget DOM footprint: <10KB initial, <50KB with dependencies

**Constraints**:
- No authentication required (anonymous/public mode)
- No persistent conversation history (each page visit fresh session)
- REST-only communication (no WebSockets)
- Widget styling must not break Docusaurus theme (CSS isolation recommended)
- Selected text limited to DOM-selectable content (no iframes, dynamically loaded content)
- No server-side state (all context passed per-request)

**Scale/Scope**:
- Supports concurrent queries from multiple users (no shared state)
- Handles 10+ sources in response display
- Large response text (>500 words) must be readable with scrolling
- Mobile: responsive down to 320px viewport width

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I: Education-First Design** ✅ PASS
- Widget serves learner needs (conversational access to book content)
- Clear UI feedback for all states (loading, error, empty results, success)
- User-friendly error messages (no technical jargon: "Service temporarily unavailable. Please try again.")
- Keyboard navigable (Tab to focus input, Enter to submit, Escape to close)
- **Evidence**: Spec US1-4 (user stories describe learner interactions), SC-011 (90% user success), FR-002/FR-007/FR-008-010 (clear UI states)

**Principle II: Practical, Engineering-Focused Content** ✅ PASS
- Widget connects to real book content (Feature 004 backend retrieves from indexed chapters)
- Display of sources with similarity scores enables verification (learner can check basis of answer)
- Text selection mode enables practical, passage-specific learning workflows
- **Evidence**: Spec SC-003 (95% valid queries return with sources), FR-005 (sources displayed), FR-006 (text selection)

**Principle III: Content Accuracy & Safety** ✅ PASS
- Widget displays backend responses verbatim (no client-side modifications to answers)
- Source attribution enables fact-checking (learner can click through to source passage)
- Backend enforces context-only generation (no hallucination from frontend)
- **Evidence**: Spec SC-004-006 (graceful handling prevents misleading empty/error states), FR-005 (sources with URLs)

**Principle IV: Docusaurus Standards & Consistency** ✅ PASS
- Widget integrates via Docusaurus layout plugin (respects doc structure)
- Inherits theme tokens (light/dark mode automatic via CSS variables)
- Cross-page navigation compatible (widget persists, state resets gracefully)
- **Evidence**: Spec FR-012 (theme adaptation), FR-001 (global embed), SC-009 (no styling breakage)

**Principle V: Testable, Reproducible Examples** ✅ PASS
- Success criteria measurable and testable (SC-001-012)
- Widget testable with mocked backend (no real API keys in test code)
- Setup instructions enable local development and testing with Feature 004 backend
- **Evidence**: Spec SC-002 (latency testable), SC-010 (mobile responsive testable), testing strategy covers unit/integration/manual

**Principle VI: Iterative Improvement & Community Feedback** ✅ PASS
- Widget modular design enables easy updates (component-based architecture)
- Console logging enables user debugging and feedback
- Configuration via environment variables (e.g., backend URL)
- **Evidence**: Spec FR-016 (logging), theme tokens enable easy customization, request IDs enable user support

**Overall Status**: ✅ **PASS** - All 6 principles satisfied. Design is education-focused, learner-friendly, practical, safe, testable, and iterable.

## Project Structure

### Documentation (this feature)

```text
specs/005-frontend-integration/
├── spec.md                       # Feature specification (complete)
├── plan.md                        # This file (in-progress)
├── research.md                    # Phase 0: Research findings (TBD)
├── data-model.md                  # Phase 1: Data entities & component props
├── quickstart.md                  # Phase 1: Getting started guide
├── contracts/                     # Phase 1: API contracts & integration examples
│   ├── component-interface.md      # Component props and events
│   └── request-response-examples.md # Example requests/responses with widget state
├── checklists/
│   └── requirements.md            # Quality checklist (complete)
└── tasks.md                       # Phase 2: Implementation tasks (TBD)
```

### Source Code (repository root)

```text
book-docs/
├── src/
│   ├── components/
│   │   ├── RAGChatWidget/         # NEW: Chatbot widget
│   │   │   ├── index.tsx          # Main component
│   │   │   ├── ChatWidget.tsx     # Widget container with state
│   │   │   ├── QueryInput.tsx     # User query input
│   │   │   ├── ResponseDisplay.tsx # Answer + sources display
│   │   │   ├── SourceList.tsx     # Retrieved sources list
│   │   │   ├── LoadingState.tsx   # Loading indicator
│   │   │   ├── ErrorState.tsx     # Error message display
│   │   │   ├── useTextSelection.ts # Hook for capturing selected text
│   │   │   ├── useApiClient.ts    # Hook for backend API calls
│   │   │   ├── types.ts           # TypeScript interfaces (ChatMessage, RetrievalSource, etc.)
│   │   │   ├── RAGChatWidget.module.css # Component styles (CSS Modules, theme-aware)
│   │   │   └── __tests__/         # Unit tests
│   │   │       ├── ChatWidget.test.tsx
│   │   │       ├── QueryInput.test.tsx
│   │   │       ├── ResponseDisplay.test.tsx
│   │   │       └── useApiClient.test.ts
│   │   │
│   │   └── RAGChatLayout/         # NEW: Docusaurus layout plugin
│   │       ├── index.tsx          # Layout wrapper component
│   │       ├── RAGChatLayout.tsx  # Injects widget into layout
│   │       └── __tests__/
│   │           └── RAGChatLayout.test.tsx
│   │
│   ├── utils/
│   │   ├── apiClient.ts           # NEW: API utilities for backend calls
│   │   │   ├── fetchQuery
│   │   │   ├── handleErrors
│   │   │   └── buildRequestPayload
│   │   │
│   │   └── formatters.ts          # NEW: Text/response formatting utilities
│   │       ├── formatAnswer
│   │       ├── formatSourceList
│   │       └── formatErrorMessage
│   │
│   ├── theme/
│   │   └── RAGChatWidget.css      # Global theme tokens (optional, theme inheritance)
│   │
│   └── pages/
│       └── ... (existing Docusaurus pages)
│
├── docusaurus.config.js            # MODIFY: Register RAGChatLayout as custom layout
├── sidebars.js                     # (no changes needed)
├── package.json                    # MODIFY: Add dev dependencies (testing, TypeScript)
├── tsconfig.json                   # (ensure TypeScript configured for React)
└── README.md                       # Update with widget integration instructions
```

**Structure Decision**: Widget embedded as React component within Docusaurus. Uses custom layout plugin to inject widget globally (no per-page changes). Modular component architecture: ChatWidget (container) + QueryInput + ResponseDisplay + SourceList + loading/error states. API utilities separate from UI components (easy testing). Hooks for text selection and API calls (reusable, testable). CSS Modules for scoped styling with theme inheritance.

## Phase 0: Research & Architecture Decisions

*Output: research.md with decision log*

**Key Research Tasks:**

1. **Docusaurus Layout Plugin API** - Confirm layout swizzling/plugin mechanism for Feature 005 version (2.x vs 3.x)
2. **CSS Theme Inheritance** - How to access Docusaurus theme context (dark mode, color tokens)
3. **Text Selection API** - Best practices for capturing selected text from DOM (document.getSelection, Range API)
4. **Fetch Error Handling** - Patterns for handling network errors, timeouts, backend errors in React
5. **React Hooks Patterns** - useEffect cleanup for canceling requests, useContext for theme
6. **Responsive Design** - CSS Grid/Flexbox best practices for mobile-first widget layout
7. **Accessibility** - ARIA roles, semantic HTML, keyboard navigation (Tab, Enter, Escape)

**Architecture Decisions to Document:**

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| **Custom layout plugin (not per-page component)** | Global injection, no per-page code changes, matches spec FR-001 | Sidebar component (less global), swizzled layout (more intrusive) |
| **React hooks (not Redux/Context)** | Minimal dependencies, local state sufficient, easier testing | Redux (overkill for single widget), Context (adds boilerplate) |
| **CSS Modules (not styled-components/Tailwind)** | Scoped styles prevent Docusaurus theme conflicts, works with any theme | Styled-components (adds runtime JS), Tailwind (conflicts with Docusaurus Tailwind) |
| **Fetch API (not axios/fetch wrapper lib)** | Native browser API, no external dependency, sufficient for MVP | Axios (adds dependency), native sufficient for simple REST calls |
| **Session ephemeral (not localStorage persistence)** | Matches spec assumption, simplifies state management, respects privacy | localStorage (adds complexity, privacy concerns) |
| **String-based text selection (not DOM nodes)** | Simpler to send to backend, backend-agnostic | DOM nodes (backend must handle, more complex) |
| **Abort signal for request cancellation** | Prevents stale response handling, good UX for navigation | Fire and forget (wasted work, potential errors) |
| **Client-side validation before API call** | Fast feedback, reduces backend load (400 errors) | Backend-only validation (slower feedback) |
| **Request ID from backend (not client-generated)** | Backend controls tracing, matches Feature 004 spec | Client-generated (duplicate IDs possible, less reliable) |

---

## Phase 1: Data Model & Component Design

*Output: data-model.md, contracts/component-interface.md, contracts/request-response-examples.md, quickstart.md*

### Data Model Entities

**ChatMessage** (internal widget state)
```typescript
interface ChatMessage {
  id: string;                      // UUID or timestamp-based
  role: 'user' | 'assistant';      // Role in conversation
  content: string;                 // Text content
  timestamp: Date;                 // When sent/received
  sources?: RetrievalSource[];     // Populated for assistant messages
  selectedText?: string;            // Optional: selected text context from user
  error?: string;                   // Optional: error message if request failed
}
```

**RetrievalSource** (from backend response)
```typescript
interface RetrievalSource {
  chunk_id: string;                 // Backend chunk identifier
  text: string;                     // Snippet preview (truncate >100 chars)
  similarity_score: number;         // 0.0-1.0
  source_url: string;               // Link to book page
  section_title: string;            // Chapter/section name
  rank: number;                     // Order (1-indexed)
}
```

**QueryRequest** (sent to backend)
```typescript
interface QueryRequest {
  query: string;                    // Required: user question
  top_k?: number;                   // Optional: default 5, range 1-20
  similarity_threshold?: number;    // Optional: default 0.5, range 0.0-1.0
  context?: string;                 // Optional: selected text context
  user_id?: string;                 // Optional: anonymous user ID (not MVP)
  session_id?: string;              // Optional: session ID (not MVP)
}
```

**ChatResponse** (from backend)
```typescript
interface ChatResponse {
  request_id: string;               // For tracing
  answer: string;                   // Generated response
  sources: RetrievalSource[];       // Retrieved chunks
  context_used: number;             // Chunks included
  tokens_used: number;              // Token count
  response_time_ms: number;         // Latency
  timestamp: string;                // ISO timestamp
  note?: string;                    // Optional: metadata notes
}
```

**WidgetState** (React component state)
```typescript
interface WidgetState {
  messages: ChatMessage[];          // Conversation history
  isLoading: boolean;               // Request in flight
  error: string | null;             // Error message (if any)
  selectedText: string | null;      // Currently selected text
  isMinimized: boolean;             // Widget collapsed
  apiUrl: string;                   // Backend endpoint URL
  sessionId: string;                // Generated session ID
}
```

### Component Interface

**RAGChatWidget** (main component)
```typescript
interface RAGChatWidgetProps {
  apiUrl: string;                   // Backend `/ask` endpoint URL (e.g., http://localhost:8000/ask)
  position?: 'bottom-right' | 'bottom-left' | 'top-right'; // Widget position (default: bottom-right)
  theme?: 'light' | 'dark' | 'auto';  // Theme override (default: auto from Docusaurus)
  enableTextSelection?: boolean;    // Enable text selection capture (default: true)
  maxMessages?: number;             // Max messages in history (default: 50)
  onError?: (error: Error) => void; // Optional error callback
}
```

**Events & Callbacks**:
- `onQuerySubmit(message: ChatMessage)` - Called when user submits query
- `onResponseReceived(response: ChatResponse)` - Called when backend responds
- `onError(error: Error)` - Called on API/network errors
- `onTextSelectionChange(text: string | null)` - Called when user selects text

---

## Phase 1.5: Integration Method & Setup

**Docusaurus Integration Approach**:

For Docusaurus 2.x:
- Create `src/theme/RAGChatLayout.tsx` (swizzled layout)
- Wrap BaseLayout with RAGChatWidget
- Register in `docusaurus.config.js`

For Docusaurus 3.x:
- Use layout plugin API or swizzle layout component
- Same approach, different API surface

**Configuration**:
- Backend URL via environment variable: `REACT_APP_API_URL` (default: `http://localhost:8000/ask`)
- Inject via `docusaurus.config.js` theme config

---

## Phase 2: Implementation Tasks

*Output: tasks.md with 150+ actionable tasks*

**Phase 2 will break down into 6 major stages**:

1. **Setup** (10 tasks): Project dependencies, TypeScript config, test infrastructure
2. **API Client & Utilities** (20 tasks): Fetch wrapper, error handling, request building
3. **Core Widget Components** (40 tasks): QueryInput, ResponseDisplay, SourceList, state management
4. **UX States & Error Handling** (30 tasks): LoadingState, ErrorState, empty results, accessibility
5. **Text Selection & Integration** (30 tasks): useTextSelection hook, Docusaurus layout plugin, theme adaptation
6. **Testing & Documentation** (20+ tasks): Unit tests, integration tests, E2E with backend, docs

---

## Non-Functional Requirements

### Performance
- Initial widget load: <500ms (lazy load, async import)
- Backend request latency: <5s p95 (inherited from Feature 004)
- UI response to input: <100ms (smooth typing)
- Widget bundle size: <100KB gzipped (including all dependencies)

### Compatibility
- Browsers: Chrome, Firefox, Safari, Edge (latest 2 versions)
- Mobile: iOS Safari 14+, Chrome Mobile latest
- Docusaurus: 2.4.x, 3.x
- React: 18.0+

### Accessibility
- WCAG AA conformance (4.5:1 contrast ratio)
- Keyboard navigable: Tab to focus, Enter to submit, Escape to close
- Screen reader compatible: semantic HTML, ARIA labels
- Focus indicators: visible on all interactive elements

### Security & Privacy
- No API keys stored in frontend code
- Backend URL configurable via environment variable
- Queries not logged to browser history or stored client-side (unless user explicitly persists)
- No tracking or analytics (optional, not MVP)

---

## Success Criteria Verification

**SC-001**: Widget on 100% of pages - Verified by navigating all pages, checking widget present
**SC-002**: <5s latency - Verified by measuring response_time_ms in backend response
**SC-003**: 95% success rate - Counted 95/100 valid queries return 200
**SC-004-010**: Error handling, loading states, etc. - Verified by manual testing with mocked responses
**SC-011**: 90% user success - Usability testing with 5-10 test users
**SC-012**: No console errors - Browser DevTools console check

---

## Assumptions (from Spec)

1. Backend `/ask` endpoint fully operational and deployed
2. Docusaurus 2.x or 3.x with React support
3. CORS enabled on backend for frontend domain
4. Plain text queries (no rich text/markdown)
5. Ephemeral sessions (no history persistence across page reloads)
6. Anonymous mode (no authentication)
7. Fixed widget position (not moveable/resizable for MVP)
8. Single-turn Q&A (not multi-turn conversation)
9. Selected text from DOM only
10. Theme inheritance via CSS variables

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Backend unavailable | Widget non-functional | Error state with retry button, graceful degradation |
| CORS misconfiguration | Widget cannot reach backend | Clear error message, setup docs, backend team coordination |
| Large responses (>10K chars) | UI layout broken, slow rendering | Truncate/virtualize response display, test with large responses |
| Mobile viewport <320px | Widget unusable | Min-width wrapper, scroll container, test on actual devices |
| Theme token naming mismatch | Widget styling broken | Use Docusaurus theme API, test light/dark mode switching |
| Selected text too large (>10K chars) | Request fails or times out | Truncate to 5000 chars, warn user |
| High latency (>5s) | User abandons request | Timeout after 30s, show "Still loading..." message at 5s |

---

## Next Steps

1. **Phase 0**: Research Docusaurus layout API, CSS theme tokens, text selection best practices
2. **Phase 1**: Design data model, component interface, API contracts
3. **Phase 2**: Generate 150+ tasks, organize by phase
4. **Implementation**: Execute tasks in phases 1-6
5. **Testing**: Unit + integration + E2E with local Feature 004 backend
6. **Deployment**: Integration into live Docusaurus site
