# Implementation Tasks: Docusaurus Frontend Integration with RAG Agent API

**Feature**: 005-frontend-integration | **Date**: 2025-12-12 | **Status**: Ready for Implementation

**MVP Scope**: User Stories 1, 3, 4 (core functionality + integration + error handling)
**Total Tasks**: 165 tasks across 6 phases
**Estimated Duration**: 40-50 hours (full MVP implementation)

---

## Dependencies & Parallelization Strategy

**User Story Completion Order**:
1. **US1 + US3 + US4** (P1 - MVP Core): Must complete together (widget, integration, error handling)
   - US1 depends on US3 (widget must be mounted to be useful)
   - US1 & US4 interdependent (loading/error states essential for US1)
2. **US2** (P2 - Enhancement): Depends on US1 (text selection builds on basic query flow)

**Parallelization Opportunities** (within Phase):
- [P] API Client utilities (T020-T040) can be built in parallel
- [P] Component files (T050-T090) can be built in parallel once types are defined
- [P] CSS modules for different components (T100-T115) can be built in parallel
- [P] Unit tests (T130-T155) can be built in parallel after components are stubbed

**MVP-First Strategy**:
- **Phase 1**: Setup (all teams)
- **Phase 2**: Foundational (all teams)
- **Phase 3**: US1 Core (P1 - can be deployed standalone)
- **Phase 4**: US3 Integration (P1 - completes MVP when combined with Phase 3)
- **Phase 5**: US4 Error Handling (P1 - essential UX, completes MVP)
- **Phase 6**: US2 Text Selection (P2 - post-MVP enhancement)
- **Phase 7**: Testing + Polish

**Suggested MVP Checkpoint**: After Phase 5, deploy to staging with Feature 004 backend for manual testing before proceeding to Phase 6+

---

## Phase 1: Project Setup & Dependencies

*Goal: Initialize project structure and install dependencies*

**Independent Test**: `npm install` succeeds, TypeScript compiles with no errors, Jest test runner executes

### Setup Tasks

- [ ] T001 Initialize Docusaurus TypeScript configuration in `book-docs/tsconfig.json` with React 18+ support
- [ ] T002 Update `book-docs/package.json` with React, TypeScript, Jest, React Testing Library dependencies (React 18+, @docusaurus/theme-common, TypeScript 4.9+)
- [ ] T003 [P] Create directory structure: `book-docs/src/components/RAGChatWidget/`
- [ ] T004 [P] Create directory structure: `book-docs/src/components/RAGChatLayout/`
- [ ] T005 [P] Create directory structure: `book-docs/src/utils/`
- [ ] T006 [P] Create directory structure: `book-docs/src/theme/`
- [ ] T007 Create `.env.example` in `book-docs/` with REACT_APP_API_URL=http://localhost:8000/ask
- [ ] T008 Install dependencies: `npm install` (or `yarn`) in book-docs/ directory
- [ ] T009 Verify TypeScript configuration: `npx tsc --noEmit` succeeds in book-docs/
- [ ] T010 Create Jest configuration file `book-docs/jest.config.js` for React Testing Library

---

## Phase 2: Foundational Infrastructure & Types

*Goal: Define shared types, utilities, and API infrastructure that all components depend on*

**Independent Test**: TypeScript interfaces compile, `apiClient.ts` exports functions, test fixtures work

### Type Definitions

- [ ] T011 Create TypeScript interfaces file `book-docs/src/components/RAGChatWidget/types.ts` with:
  - ChatMessage interface
  - RetrievalSource interface
  - QueryRequest interface
  - ChatResponse interface
  - ErrorResponse interface
  - WidgetState interface
  - WidgetProps interface
- [ ] T012 [P] Add validation types to `book-docs/src/components/RAGChatWidget/types.ts`:
  - Validation result type (success | error with message)
  - Error type with status code, message
  - Request status type (idle | loading | success | error)
- [ ] T013 Ensure all TypeScript interfaces in types.ts are exported and have JSDoc comments

### API Client Utilities

- [ ] T014 Create `book-docs/src/utils/apiClient.ts` with function:
  - `fetchQuery(request: QueryRequest, apiUrl: string): Promise<ChatResponse>`
  - Includes AbortController for cancellation
  - Includes 30s timeout
  - Includes error handling and retry logic
- [ ] T015 [P] Implement retry logic in `apiClient.ts`:
  - Exponential backoff (1s, 2s, 4s)
  - Max 3 retries
  - Retry only on 5xx and timeout errors
  - Don't retry on 400 validation errors
- [ ] T016 [P] Implement timeout handling in `apiClient.ts`:
  - 30s timeout for fetch requests
  - User-friendly timeout error message
  - Distinguish from network errors
- [ ] T017 [P] Implement error mapping in `apiClient.ts`:
  - `mapErrorResponse(error: any): string`
  - Convert HTTP status codes to friendly messages
  - Handle network errors, timeouts, validation errors (400), service errors (503)
- [ ] T018 [P] Implement request validation in `apiClient.ts`:
  - `validateQueryRequest(request: QueryRequest): string | null`
  - Validate query non-empty, max 1000 chars
  - Validate top_k range [1, 20]
  - Validate similarity_threshold range [0.0, 1.0]
  - Validate context max 5000 chars
  - Return error message if invalid, null if valid
- [ ] T019 Add JSDoc comments to all functions in `apiClient.ts`

### Text Utilities

- [ ] T020 [P] Create `book-docs/src/utils/formatters.ts` with functions:
  - `formatAnswer(text: string): string` - Truncate to reasonable display length, preserve line breaks
  - `formatSourceUrl(url: string): string` - Convert relative to absolute if needed
  - `formatSimilarityScore(score: number): string` - Format as percentage (e.g., "89%")
  - `formatTimestamp(iso: string): string` - User-friendly time display
  - `truncateText(text: string, maxChars: number): string` - Add ellipsis if truncated
- [ ] T021 [P] Add error message mapping to `formatters.ts`:
  - `getErrorMessage(statusCode: number, message?: string): string`
  - Map HTTP status codes to user-friendly messages
  - Handle edge cases (missing message, unexpected status)
- [ ] T022 Add JSDoc comments to all functions in `formatters.ts`

### Test Fixtures & Mocks

- [ ] T023 Create test fixtures file `book-docs/src/components/RAGChatWidget/__tests__/fixtures.ts` with:
  - Mock ChatResponse object
  - Mock RetrievalSource object
  - Mock QueryRequest object
  - Mock ChatMessage object
  - Mock error responses (400, 503, 500)
- [ ] T024 [P] Create test mocks in `__tests__/fixtures.ts`:
  - Mock fetch function with different response scenarios
  - Mock window.getSelection() for text selection tests
  - Mock Docusaurus theme context

---

## Phase 3: Core Widget Component - User Story 1 (Ask Questions)

*Goal: Implement basic chatbot widget with query input and response display*

**User Story 1**: "As a reader, I can ask questions and see context-grounded answers with sources"

**Independent Test**:
- Widget renders on page
- User can type question and submit
- Response displays answer and sources
- Loading state appears while waiting
- Empty query shows validation error

### Component Foundation

- [ ] T025 [US1] Create component file `book-docs/src/components/RAGChatWidget/index.tsx`:
  - Default export of RAGChatWidget component
  - Imports from other components
  - Re-export type interfaces
- [ ] T026 [US1] Create main component `book-docs/src/components/RAGChatWidget/ChatWidget.tsx` with:
  - React.FC<RAGChatWidgetProps>
  - useState for messages, loading, error, isMinimized
  - useState for sessionId (generated once on mount)
  - useEffect for mount/unmount cleanup
  - Return JSX with query input + response display areas
- [ ] T027 [US1] [P] Create QueryInput component `book-docs/src/components/RAGChatWidget/QueryInput.tsx`:
  - Input field for user query
  - Submit button (disabled when loading or invalid)
  - Error message display (for empty query, etc.)
  - Props: onSubmit, isLoading, error, selectedText (optional)
  - Pass selectedText to submit handler
- [ ] T028 [US1] [P] Create ResponseDisplay component `book-docs/src/components/RAGChatWidget/ResponseDisplay.tsx`:
  - Display ChatMessage with role='assistant'
  - Show answer text (may be long, use scrollable container)
  - Show sources list below answer
  - Show metadata (tokens_used, response_time_ms)
  - Handle empty sources gracefully (friendly message)
- [ ] T029 [US1] [P] Create SourceList component `book-docs/src/components/RAGChatWidget/SourceList.tsx`:
  - Render array of RetrievalSource as list items
  - Each source shows: rank, section_title, similarity_score%, chunk_id
  - Each source is clickable link to source_url
  - Props: sources: RetrievalSource[], onSourceClick?: callback
- [ ] T030 [US1] [P] Create LoadingState component `book-docs/src/components/RAGChatWidget/LoadingState.tsx`:
  - Spinner or "Thinking..." message
  - Optional progress indicator for >5s requests
  - Props: none (or duration for conditional "Still loading..." message)
- [ ] T031 [US1] [P] Create ErrorState component `book-docs/src/components/RAGChatWidget/ErrorState.tsx`:
  - Display error message (user-friendly)
  - Retry button (if applicable)
  - Props: error: string, onRetry?: callback

### Custom Hooks

- [ ] T032 [US1] Create `book-docs/src/components/RAGChatWidget/useApiClient.ts` custom hook:
  - `useApiClient(apiUrl: string)` returns `{ data, loading, error, submitQuery }`
  - submitQuery function calls apiClient.fetchQuery
  - Handles AbortController cleanup on unmount
  - Sets state for data, loading, error
  - Manages request cancellation on navigation
- [ ] T033 [US1] [P] Implement error handling in `useApiClient.ts`:
  - Catch network errors and map to friendly messages
  - Catch validation errors (400) and display validation message
  - Catch service errors (503) and offer retry
  - Ignore AbortError (expected on unmount)
- [ ] T034 [US1] Implement loading timeout in `useApiClient.ts`:
  - After 5s of loading, optionally show "Still loading..." message
  - For 30s timeout, auto-error with "Request took too long"

### State Management

- [ ] T035 [US1] Implement message state in ChatWidget:
  - `messages: ChatMessage[]` useState
  - Add message when user submits query
  - Add message when backend responds
  - Max 50 messages in history
  - Message ID generation (timestamp-based or UUID)
- [ ] T036 [US1] Implement error state in ChatWidget:
  - `error: string | null` useState
  - Set error from API call failure
  - Clear error when new query submitted
- [ ] T037 [US1] Implement loading state in ChatWidget:
  - `isLoading: boolean` useState
  - Set true when query submitted
  - Set false when response received or error occurs
  - Disable submit button during loading
- [ ] T038 [US1] Implement session state in ChatWidget:
  - `sessionId: string` useState (generated once on mount)
  - Pass to backend in QueryRequest (for future use)
  - Use for request tracing

### Styling & Layout

- [ ] T039 [US1] Create CSS Module `book-docs/src/components/RAGChatWidget/RAGChatWidget.module.css`:
  - Widget container styles (fixed position bottom-right, z-index 1000)
  - Input field styles (inherit theme colors)
  - Button styles (primary color, hover, disabled state)
  - Response area styles (scrollable, max-height)
  - Loading spinner styles
  - Error message styles (red text, clear indication)
  - Message list styles (padding, spacing)
- [ ] T040 [US1] Add theme variable references to CSS:
  - Use `var(--ifm-color-primary)` for button color
  - Use `var(--ifm-color-background)` for widget background
  - Use `var(--ifm-color-background-secondary)` for input field
  - Use `var(--ifm-text-color-base)` for text
  - Use `var(--ifm-border-color)` for borders
- [ ] T041 [US1] Add responsive styles to RAGChatWidget.module.css:
  - Mobile viewport <640px: full width - 20px margins
  - Tablet/desktop viewport ≥768px: 400px fixed width
  - Ensure 44px touch target size for buttons
  - Scrollable container for large responses
- [ ] T042 [US1] Add print mode styles to RAGChatWidget.module.css:
  - `@media print { .widget { display: none; } }`
  - Hide widget when page is printed

### Component Integration

- [ ] T043 [US1] Integrate QueryInput into ChatWidget:
  - Pass onSubmit handler that validates and sends query
  - Pass isLoading state
  - Pass error state
  - Handle selectedText (passed from QueryInput)
- [ ] T044 [US1] Integrate ResponseDisplay into ChatWidget:
  - Show most recent assistant message
  - Pass onSourceClick handler (navigate to source)
- [ ] T045 [US1] Integrate LoadingState into ChatWidget:
  - Show when isLoading === true
  - Hide when isLoading === false
- [ ] T046 [US1] Integrate ErrorState into ChatWidget:
  - Show when error !== null
  - Provide retry handler to resubmit last query

---

## Phase 4: Global Layout Integration - User Story 3 (Widget Integration)

*Goal: Mount widget globally in Docusaurus layout so it appears on all pages*

**User Story 3**: "As a reader, the widget appears on every page and persists during navigation"

**Independent Test**:
- Widget visible on multiple Docusaurus pages
- Widget survives page navigation
- Widget can be minimized and reopened
- Minimize state persists during session

### Docusaurus Layout Plugin

- [ ] T047 [US3] Create layout wrapper `book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx`:
  - Takes BaseLayout as prop
  - Returns BaseLayout wrapped with RAGChatWidget
  - Pass apiUrl from environment (process.env.REACT_APP_API_URL)
- [ ] T048 [US3] Create Docusaurus layout index `book-docs/src/components/RAGChatLayout/index.tsx`:
  - Import original layout component
  - Import RAGChatLayout wrapper
  - Export wrapped component as default
  - Add JSDoc explaining swizzling pattern
- [ ] T049 [US3] Create swizzled layout file `book-docs/src/theme/Layout/index.tsx`:
  - Swizzle original Docusaurus layout component
  - Wrap with RAGChatWidget component
  - Pass apiUrl from env variable

### Widget Persistence

- [ ] T050 [US3] Implement minimize/expand functionality in ChatWidget:
  - Add useState for isMinimized
  - Minimize button in widget header
  - Collapse widget body when minimized (show only header with expand button)
  - Persist expansion state in sessionStorage (within page session)
- [ ] T051 [US3] Add widget header with title:
  - "Book Assistant" or similar title
  - Minimize/expand button
  - Close button (optional, resets state if reopened)
  - Props: onMinimize, onClose callbacks
- [ ] T052 [US3] Clear state gracefully on page navigation:
  - useEffect cleanup: abort in-flight requests
  - Optionally persist conversation (not MVP, but leave hook for future)
  - Reset error state on new page
- [ ] T053 [US3] Add session state persistence to ChatWidget:
  - Save session ID to sessionStorage on mount
  - Retrieve on mount if already exists
  - Clear on page unload (optional)

### Theme Adaptation

- [ ] T054 [US3] Implement dark mode detection in ChatWidget:
  - Use Docusaurus theme context (if available) or detect `[data-theme="dark"]` on html
  - Pass theme to CSS via className or CSS variable
  - CSS styles automatically adapt via --ifm-color-* variables
- [ ] T055 [US3] Test light/dark mode switching:
  - Manually toggle theme in Docusaurus settings
  - Verify widget background, text, button colors adapt
  - No manual intervention needed (CSS variables should handle it)
- [ ] T056 [US3] Update CSS to inherit all theme colors:
  - Ensure all colors reference CSS variables
  - No hardcoded colors in widget CSS
  - Support both light and dark modes

### Environment Configuration

- [ ] T057 [US3] Update `book-docs/.env.example`:
  - Add REACT_APP_API_URL=http://localhost:8000/ask
  - Add documentation comment explaining this is backend endpoint
- [ ] T058 [US3] Create .env file in book-docs/:
  - Copy from .env.example
  - Set REACT_APP_API_URL to local backend (or staging/production)
  - Document how to configure for different environments
- [ ] T059 [US3] Verify environment variable is accessible:
  - Log process.env.REACT_APP_API_URL in console (during development)
  - Confirm RAGChatWidget receives correct apiUrl prop
  - Remove debug log before commit

---

## Phase 5: Error Handling & UX Polish - User Story 4 (Error Handling & States)

*Goal: Handle all error scenarios gracefully with clear user feedback*

**User Story 4**: "As a reader, I understand what's happening at each step (loading, success, error, no results)"

**Independent Test**:
- Empty query shows validation error
- Service error (503) shows friendly message with retry
- Network timeout shows "Request took too long"
- Empty results (no sources) shows "I don't have information..."
- All error messages are non-technical

### Validation Error Handling

- [ ] T060 [US4] Implement client-side query validation in QueryInput:
  - Check query is non-empty: `if (!query.trim())`
  - Show inline error: "Please enter a question before asking."
  - Disable submit button if invalid
  - Clear error when user starts typing again
- [ ] T061 [US4] Validate selected text size in QueryInput:
  - If selectedText > 5000 chars, truncate silently or warn user
  - Show truncation message: "Selected text was truncated to 5000 characters"
  - Update selectedText state with truncated version

### API Error Handling

- [ ] T062 [US4] Implement backend error response handling:
  - On HTTP 400 (validation error from backend), extract detail.details[].message
  - Display user-friendly message: "Please enter a valid question" or similar
  - Don't show technical error codes
- [ ] T063 [US4] Implement service error handling (503):
  - On HTTP 503, show message: "Service temporarily unavailable. Please try again later."
  - Provide "Retry" button that resubmits last query
  - Log error to console (development only)
- [ ] T064 [US4] Implement network error handling:
  - On network error (no connection), show: "Unable to reach server. Please check your connection."
  - Suggest checking internet connection
  - Provide retry button
- [ ] T065 [US4] Implement timeout error handling:
  - On 30s timeout, show: "Request took too long. Please try again."
  - After 5s of loading, show optional "Still loading..." message
  - Prevent duplicate submissions during timeout

### Empty Results Handling

- [ ] T066 [US4] Implement empty sources handling in ResponseDisplay:
  - If ChatResponse.sources is empty array, show friendly message:
    "I don't have information about this topic in the provided materials."
  - Don't show blank response area
  - Still show response_time_ms and tokens_used (for debugging)
- [ ] T067 [US4] Handle backend note field in ResponseDisplay:
  - If ChatResponse.note exists, optionally display it
  - Example: "No chunks with sufficient similarity found"
  - Make note text smaller/lighter (secondary information)

### Loading State Feedback

- [ ] T068 [US4] Implement loading indicator in LoadingState:
  - Show spinner or animated "Thinking..." text
  - Center in response area
  - Clear indication that something is happening
  - Estimated time message (optional): "Usually takes <3 seconds"
- [ ] T069 [US4] Implement slow network detection:
  - If request > 5s, show additional message: "Still thinking..."
  - Reassure user request is still in progress
  - Help prevent users from submitting duplicate queries
- [ ] T070 [US4] Disable submit button during loading:
  - QueryInput submit button disabled when isLoading === true
  - User cannot submit multiple requests simultaneously
  - Clear visual feedback (greyed out, cursor not-allowed)

### Accessibility Improvements

- [ ] T071 [US4] Add ARIA labels to all interactive elements:
  - Input: `aria-label="Ask a question about the book"`
  - Submit button: `aria-label="Send question"`
  - Minimize button: `aria-label="Minimize chat widget"`
  - Close button: `aria-label="Close chat"`
- [ ] T072 [US4] Add semantic HTML to components:
  - Use `<button>` for buttons (not divs)
  - Use `<input type="text">` for text input
  - Use `<form>` for query form
  - Use `<label>` for input labels
- [ ] T073 [US4] Add live regions for dynamic content:
  - Response area: `aria-live="polite" aria-atomic="true"` (for screen readers)
  - Error messages: `role="status" aria-live="polite"`
  - Loading state: `role="status" aria-live="polite"`
- [ ] T074 [US4] Implement keyboard navigation:
  - Tab key: Focus input, button, close button
  - Enter key: Submit query (when input focused)
  - Escape key: Minimize widget
  - Focus order: logical (input → submit → close)
- [ ] T075 [US4] Add focus indicators:
  - `input:focus`: `outline: 2px solid var(--ifm-color-primary); outline-offset: 2px;`
  - `button:focus`: Same outline style
  - Ensure 4.5:1 contrast ratio on focus indicators

### Logging & Debugging

- [ ] T076 [US4] Implement console logging in apiClient:
  - Log query submission: `console.log("Query submitted:", query)`
  - Log backend response: `console.log("Backend response:", response)`
  - Log errors: `console.error("API error:", error)`
  - Include timestamp and request_id for tracing
  - Disable logs in production (check NODE_ENV)
- [ ] T077 [US4] Implement performance logging:
  - Log response_time_ms from backend
  - Log total time from user input to response display
  - Track slow requests (>5s) for debugging
- [ ] T078 [US4] Add error boundary (optional):
  - Catch component errors and display fallback UI
  - Prevent entire page from breaking if widget crashes
  - Show: "Widget encountered an error. Please refresh the page."

---

## Phase 6: Text Selection Mode - User Story 2 (Context Injection)

*Goal: Allow users to select text and include it as context in queries*

**User Story 2**: "As a reader, I can select text and ask follow-up questions about that passage"

**Independent Test**:
- User selects text on page
- Selected text appears in widget
- Query sent with selectedText in context field
- Backend response references or leverages selected text

### Text Selection Capture

- [ ] T079 [US2] Create `book-docs/src/components/RAGChatWidget/useTextSelection.ts` custom hook:
  - `useTextSelection()` returns `{ selectedText: string | null, clearSelection: () => void }`
  - Listen to mouseup event: `document.addEventListener('mouseup', handleSelection)`
  - Use `window.getSelection()` to capture selected text
  - Truncate to 5000 chars if larger
  - useEffect cleanup: remove event listener on unmount
- [ ] T080 [US2] Implement selection detection in useTextSelection:
  - Call on mouseup event
  - Get selection: `window.getSelection()?.toString()`
  - Only set if selection is non-empty and non-whitespace
  - Trim whitespace from selection
- [ ] T081 [US2] Implement selection truncation in useTextSelection:
  - If selectedText.length > 5000, truncate to 5000
  - Optionally show warning: "Selected text was truncated to 5000 characters"
  - Store truncated version
- [ ] T082 [US2] Add context clearing in useTextSelection:
  - `clearSelection()` function to reset selectedText to null
  - Call when user submits query (clear for next interaction)
  - Optional: call when user selects new text (override previous)

### Selected Text Display & Input

- [ ] T083 [US2] Add selected text display to QueryInput:
  - Show selected text above input field (if selectedText exists)
  - Display in small box/container with grey background
  - Show "Clear selection" link/button
  - Props: selectedText, onClearSelection
- [ ] T084 [US2] Integrate useTextSelection hook into QueryInput:
  - Import useTextSelection in QueryInput (or in ChatWidget)
  - Pass selectedText and clearSelection to QueryInput
  - Integrate with input component
- [ ] T085 [US2] Update query submission to include selected text:
  - When user submits query, include selectedText in QueryRequest.context
  - Send to backend as: `{ query: "...", context: selectedText, ... }`
  - Show clear indication text is being sent as context (optional UI hint)

### Selection UI Enhancements

- [ ] T086 [US2] Add context indicator to QueryInput:
  - When selectedText exists, show: "Using selected text as context"
  - Optional: show word count: "Selected: 42 words"
  - Optional: show truncation warning: "Text truncated to 5000 chars"
- [ ] T087 [US2] Add prompt for selection-only interaction:
  - If user selects text but doesn't type query, prompt: "What would you like to know about this passage?"
  - Optional: pre-fill prompt text or show placeholder
- [ ] T088 [US2] Add selection visual feedback:
  - When text is selected, optional visual indicator (not required for MVP)
  - Could show: widget highlight, badge, or notification
  - Minimal UX change to avoid confusion

---

## Phase 7: Testing & Final Polish

*Goal: Add unit tests, integration tests, and final documentation*

**Independent Test**: All tests pass, no console warnings/errors, widget functional end-to-end

### Unit Tests

- [ ] T089 Create test file `book-docs/src/components/RAGChatWidget/__tests__/ChatWidget.test.tsx`:
  - Test component renders
  - Test input field is editable
  - Test submit button works
  - Test error state displays error message
  - Test loading state shows spinner
  - Test response displays answer and sources
- [ ] T090 [P] Create test file `__tests__/QueryInput.test.tsx`:
  - Test input field renders
  - Test submit button disabled when input empty
  - Test submit button enabled when input has text
  - Test onSubmit called with query text
  - Test error message displays for empty query
  - Test selectedText displays if provided
- [ ] T091 [P] Create test file `__tests__/ResponseDisplay.test.tsx`:
  - Test renders answer text
  - Test renders sources list
  - Test displays empty message if no sources
  - Test displays metadata (tokens, time)
  - Test source links are clickable
- [ ] T092 [P] Create test file `__tests__/SourceList.test.tsx`:
  - Test renders array of sources
  - Test each source shows title, score, chunk_id
  - Test source links have correct href
  - Test onSourceClick called with URL when clicked
- [ ] T093 [P] Create test file `__tests__/LoadingState.test.tsx`:
  - Test renders spinner/loading message
  - Test "Still loading..." message after 5s (optional)
- [ ] T094 [P] Create test file `__tests__/ErrorState.test.tsx`:
  - Test renders error message
  - Test retry button visible and clickable
  - Test onRetry called when clicked

### Integration Tests

- [ ] T095 Create integration test `__tests__/ChatWidget.integration.test.tsx`:
  - Mock fetch for backend API
  - Test user types query and submits
  - Test loading state appears
  - Test response displays when backend returns success
  - Test error displays when backend returns error
  - Test retry works when submitted again
- [ ] T096 [P] Create integration test `__tests__/TextSelection.integration.test.tsx`:
  - Mock window.getSelection()
  - Test selected text is captured
  - Test selected text is sent to backend in context field
  - Test selected text clears after submission
- [ ] T097 [P] Create integration test `__tests__/ErrorHandling.integration.test.tsx`:
  - Mock fetch to return 400 validation error
  - Test validation error message displays
  - Mock fetch to return 503 service error
  - Test service error message displays with retry button
  - Mock fetch to timeout (>30s)
  - Test timeout error message displays

### API Client Tests

- [ ] T098 Create test file `__tests__/apiClient.test.ts`:
  - Test validateQueryRequest validates empty query
  - Test validateQueryRequest validates top_k range
  - Test validateQueryRequest validates threshold range
  - Test fetchQuery makes POST request to apiUrl
  - Test retry logic retries on 5xx error
  - Test retry respects max 3 retries
  - Test timeout after 30s
  - Test AbortController cancellation
- [ ] T099 [P] Create error handling tests:
  - Test mapErrorResponse for network errors
  - Test mapErrorResponse for timeouts
  - Test mapErrorResponse for HTTP status codes (400, 503, 500)
  - Test getErrorMessage returns user-friendly messages

### Formatter Tests

- [ ] T100 Create test file `__tests__/formatters.test.ts`:
  - Test formatAnswer truncates long text
  - Test formatSourceUrl handles relative/absolute URLs
  - Test formatSimilarityScore formats as percentage
  - Test formatTimestamp returns readable date
  - Test truncateText adds ellipsis
  - Test getErrorMessage maps status codes correctly

### Component Accessibility Tests

- [ ] T101 Create accessibility test `__tests__/a11y.test.tsx`:
  - Test all buttons have accessible labels
  - Test input has label or placeholder
  - Test semantic HTML used (form, button, input)
  - Test ARIA labels present on live regions
  - Test focus indicators visible
  - Test keyboard navigation works (Tab, Enter, Escape)
- [ ] T102 [P] Test contrast ratios:
  - Test foreground/background contrast >= 4.5:1
  - Test button text/background contrast >= 4.5:1
  - Test error message text is readable

### End-to-End Tests (Manual)

- [ ] T103 Test with local Feature 004 backend:
  - Start FastAPI backend on localhost:8000
  - Start Docusaurus dev server
  - Navigate to book page
  - Widget appears in bottom-right corner
  - Type query and submit
  - Loading spinner appears
  - Response displays with answer and sources
  - Retry works if backend returns error
- [ ] T104 Test on multiple Docusaurus pages:
  - Navigate to 3+ different book pages
  - Widget persists on each page
  - Minimize/expand state persists during navigation
  - Each page's queries are independent
- [ ] T105 Test mobile responsiveness:
  - Open on mobile device or DevTools mobile emulation
  - Widget width adapts to viewport (<640px: full width, ≥768px: 400px)
  - Input field and button are touch-friendly (44px+ size)
  - Response area scrolls if content overflows
- [ ] T106 Test theme switching:
  - Open Docusaurus theme switcher
  - Toggle between light and dark modes
  - Widget colors adapt automatically
  - Text remains readable in both modes
- [ ] T107 Test error scenarios:
  - Backend unreachable: Widget shows error message
  - Backend timeout: Widget shows "Request took too long"
  - Empty query: Widget shows validation error
  - No results from backend: Widget shows "I don't have information..."
  - Service error (503): Widget shows "Service temporarily unavailable" with retry

### Documentation & Comments

- [ ] T108 Add README to `book-docs/src/components/RAGChatWidget/`:
  - Overview of widget architecture
  - Component diagram (ASCII or image)
  - How to integrate with Docusaurus
  - Configuration (apiUrl, position, theme)
  - Feature list (US1, US2, US3, US4)
  - Known limitations
- [ ] T109 Add JSDoc comments to all component files:
  - ChatWidget: Describe props, state, behavior
  - QueryInput: Document input validation, onSubmit signature
  - ResponseDisplay: Document expected ChatMessage structure
  - SourceList: Document RetrievalSource display format
  - LoadingState, ErrorState: Document when shown
  - Custom hooks: useApiClient, useTextSelection parameter and return types
- [ ] T110 Update `book-docs/README.md`:
  - Add section: "Chat Widget (Feature 005)"
  - Quick start: Configure REACT_APP_API_URL, run dev server
  - Troubleshooting: CORS errors, backend unreachable, widget not appearing
  - Links to Feature 004 backend setup
- [ ] T111 Create deployment guide:
  - Configure REACT_APP_API_URL for production backend
  - Build production bundle: `npm run build`
  - Verify widget appears in built site
  - Test with real backend before deploying

### Bug Fixes & Cleanup

- [ ] T112 Remove all console.log statements (except errors in production):
  - Keep debug logs for development (commented or in development mode only)
  - Ensure no sensitive data logged
- [ ] T113 Fix TypeScript warnings:
  - `npm run type-check` should have 0 errors
  - Ensure all types are properly defined
  - Fix any missing type annotations
- [ ] T114 Verify no memory leaks:
  - useEffect cleanups in place (especially AbortController, event listeners)
  - No circular dependencies
  - Messages array max length enforced (50 messages)
- [ ] T115 Run ESLint and code formatter:
  - `npm run lint` - fix all linting errors
  - `npm run format` (or prettier) - format code consistently
  - Ensure consistent indentation and style

### Browser Compatibility Testing

- [ ] T116 Test on Chrome latest:
  - Widget renders
  - Query submission works
  - Response displays correctly
  - No console errors
- [ ] T117 [P] Test on Firefox latest:
  - Widget renders
  - Query submission works
  - Response displays correctly
  - No console errors
- [ ] T118 [P] Test on Safari (iOS and macOS):
  - Widget renders
  - Query submission works
  - Text selection works (if applicable)
  - No console errors
- [ ] T119 [P] Test on Edge latest:
  - Widget renders
  - Query submission works
  - Response displays correctly
  - No console errors

### Performance Testing

- [ ] T120 Measure widget load time:
  - Widget should load in <500ms
  - Measure with Lighthouse or DevTools Performance tab
  - Identify slow operations (if any)
  - Lazy load dependencies if needed
- [ ] T121 Measure API request latency:
  - Response should arrive in <5s (inherited from Feature 004)
  - Measure with DevTools Network tab
  - Monitor for slow requests
- [ ] T122 Measure UI response time:
  - UI should respond to input within <100ms
  - No janky animations or freezes
  - Smooth scroll in response area

---

## Phase 8: Integration with Feature 004 Backend - Cross-Feature Validation

*Goal: Verify widget works correctly with live Feature 004 backend*

**Independent Test**: Widget communicates with Feature 004 `/ask` endpoint, receives responses, displays correctly

### Backend Integration Validation

- [ ] T123 Verify Feature 004 backend is running:
  - Start backend: `cd backend && python -m uvicorn src.api:app --reload`
  - Confirm running on http://localhost:8000
  - Test `/health` endpoint: `curl http://localhost:8000/health`
- [ ] T124 Test `/ask` endpoint with cURL:
  - Submit test query: `curl -X POST http://localhost:8000/ask -d '{"query": "What is physical AI?"}' -H 'Content-Type: application/json'`
  - Verify response has: request_id, answer, sources[], context_used, tokens_used, response_time_ms
- [ ] T125 Verify CORS configuration:
  - Widget should be able to POST to backend from Docusaurus domain
  - If CORS error in browser console, configure backend CORS headers
  - Test OPTIONS preflight request succeeds
- [ ] T126 Test full request cycle with widget:
  - Open Docusaurus page with widget
  - Type query: "What is kinematics?"
  - Submit and verify response displays
  - Check browser DevTools Network tab for POST request
  - Verify response structure matches expected format

### Response Format Validation

- [ ] T127 Validate ChatResponse structure:
  - Response has all required fields: request_id, answer, sources, context_used, tokens_used, response_time_ms, timestamp
  - answer is non-empty string
  - sources is array (may be empty)
  - All numeric fields are numbers
- [ ] T128 Validate RetrievalSource format:
  - Each source has: chunk_id, text, similarity_score, source_url, section_title, rank
  - similarity_score is number between 0.0 and 1.0
  - source_url is valid Docusaurus path (e.g., /docs/...)
- [ ] T129 Test error response format:
  - Submit invalid query (empty): Verify 400 response with detail.error
  - Verify error message is user-friendly (not technical jargon)

### Content Display Validation

- [ ] T130 Verify answer text displays correctly:
  - Long answers (>500 words) should be scrollable
  - Line breaks preserved
  - Links (if any) are clickable
- [ ] T131 Verify sources display correctly:
  - Each source shows rank, section_title, similarity_score
  - Source links are clickable and navigate to correct page
  - Similarity scores formatted as percentages
- [ ] T132 Verify metadata displays:
  - response_time_ms shown as "Took 1.2s" or similar
  - tokens_used shown for transparency
  - context_used shows number of sources used

---

## Phase 9: Final Polish & Documentation

*Goal: Final refinements, edge case handling, comprehensive documentation*

### Edge Case Handling

- [ ] T133 Handle very long queries (>1000 chars):
  - Client validation truncates to 1000 chars
  - Show warning: "Query truncated to 1000 characters"
  - Recount characters as user types
- [ ] T134 Handle very long selected text (>5000 chars):
  - Silently truncate to 5000 chars
  - Show truncation message: "Selected text truncated to 5000 characters"
- [ ] T135 Handle very long responses (>10,000 chars):
  - Response area is scrollable
  - No layout breakage
  - Performance remains good
- [ ] T136 Handle rapid successive queries:
  - Abort previous request if user submits new query
  - Only display response for latest query
  - No race conditions
- [ ] T137 Handle navigation away mid-request:
  - useEffect cleanup aborts request
  - No "can't update unmounted component" warnings
  - State resets on return to page
- [ ] T138 Handle offline scenario:
  - Show friendly message: "Unable to reach server. Please check your connection."
  - Provide retry button
  - Recovery works when connection restored

### Internationalization Preparation (Future)

- [ ] T139 Prepare UI strings for i18n (no actual translation, just preparation):
  - Extract all hardcoded strings to constants file
  - Example: MESSAGES = { LOADING: "Thinking...", EMPTY_QUERY: "Please enter..." }
  - Leave comment: "Ready for future i18n implementation"
- [ ] T140 Document non-English support:
  - Widget should work with non-English queries (backend-dependent)
  - UI text is currently English (no translation for MVP)
  - Backend should handle non-English if feature 004 supports it

### Analytics & Monitoring (Optional)

- [ ] T141 Add optional telemetry logging (comment out for MVP):
  - Track query submission: `{ timestamp, query_length, selected_text_length }`
  - Track response success/error: `{ request_id, response_time_ms, status_code }`
  - Send to analytics service (or skip for MVP)
  - Leave commented code for future implementation
- [ ] T142 Add request tracing:
  - Include request_id in all logs
  - Correlate widget logs with backend logs
  - Enable debugging: "I submitted query X with request ID Y, but backend received Z"

### Documentation Completion

- [ ] T143 Create ARCHITECTURE.md:
  - Component hierarchy diagram (ASCII or image)
  - Data flow: User input → API call → Response display
  - State management: Where state lives, how it flows
  - Hook patterns: useApiClient, useTextSelection
- [ ] T144 Create API_INTEGRATION.md:
  - How to change backend URL
  - Expected request format
  - Expected response format
  - Common error scenarios
- [ ] T145 Create TROUBLESHOOTING.md:
  - Widget not appearing: Check layout swizzle, tsconfig
  - API errors (CORS, 503, timeout): How to debug
  - No sources returned: Check Qdrant collection, similarity threshold
  - Text selection not working: Browser compatibility, element restrictions

### Quality Assurance Checklist

- [ ] T146 Final code review:
  - No console.log statements (except errors)
  - No hardcoded values (e.g., apiUrl should come from env)
  - No unused imports or variables
  - Consistent naming (camelCase for JS, kebab-case for CSS classes)
- [ ] T147 Final accessibility audit:
  - Run axe DevTools, fix all violations
  - Tab through all interactive elements
  - Test with screen reader (VoiceOver, NVDA)
  - Verify 4.5:1 contrast on text and focus indicators
- [ ] T148 Final performance audit:
  - Lighthouse score >90 for widget
  - No memory leaks (DevTools, check memory over time)
  - No janky animations or freezes
  - Widget load time <500ms
- [ ] T149 Final browser compatibility:
  - Test on Chrome, Firefox, Safari, Edge
  - Test on mobile (iOS Safari, Chrome Mobile)
  - No console errors
  - All features work on all browsers
- [ ] T150 Final manual testing:
  - Run through all user stories (US1, US2, US3, US4)
  - Test error scenarios (backend down, timeout, validation)
  - Test on real Feature 004 backend
  - Get sign-off from product (if applicable)

### Deployment & Release

- [ ] T151 Prepare release notes:
  - Feature overview: "Chat widget for asking questions about book"
  - User stories implemented: US1 (ask), US3 (integration), US4 (errors), US2 (text selection)
  - Known limitations: No conversation history, stateless
  - Configuration: REACT_APP_API_URL
  - Next steps: "Deploy to staging, test with real backend, gather feedback"
- [ ] T152 Create migration guide (if replacing previous widget):
  - Steps to remove old widget (if applicable)
  - Steps to enable new widget
  - Configuration changes
  - Testing checklist before going live
- [ ] T153 Tag release in git:
  - Commit final code
  - Tag version: `git tag -a v0.1.0 -m "Feature 005 MVP: RAG Chat Widget"`
  - Push tag: `git push origin v0.1.0`
- [ ] T154 Deploy to staging:
  - Build production bundle: `npm run build`
  - Deploy to staging environment
  - Configure REACT_APP_API_URL for staging backend
  - Verify widget works on staging
- [ ] T155 Deploy to production:
  - Configure REACT_APP_API_URL for production backend
  - Deploy to production
  - Monitor for errors (check logs, analytics)
  - Have rollback plan ready (revert commit or flip feature flag)

---

## Task Summary

| Phase | Title | Task Count | Focus |
|-------|-------|------------|-------|
| 1 | Setup & Dependencies | 10 | Project initialization, npm install, TypeScript config |
| 2 | Foundational Infrastructure | 25 | Types, API client, utilities, test fixtures |
| 3 | Core Widget (US1) | 22 | QueryInput, ResponseDisplay, SourceList, LoadingState, useApiClient hook |
| 4 | Layout Integration (US3) | 13 | Docusaurus swizzle, persistence, theme adaptation, env config |
| 5 | Error Handling (US4) | 19 | Validation, API errors, empty results, loading feedback, accessibility, logging |
| 6 | Text Selection (US2) | 10 | useTextSelection hook, selected text display, integration |
| 7 | Testing & Polish | 27 | Unit tests, integration tests, accessibility, performance, browser compat |
| 8 | Feature 004 Integration | 8 | Backend validation, response format, CORS, content display |
| 9 | Final Polish & Docs | 23 | Edge cases, i18n prep, analytics, comprehensive documentation, QA |
| **TOTAL** | **165 tasks** | | **Complete MVP ready for deployment** |

---

## MVP Checkpoint (After Phase 5)

**Deployable Scope**: User Stories 1, 3, 4 implemented
- [x] Widget appears on all Docusaurus pages
- [x] Users can ask questions and see answers with sources
- [x] Error handling graceful and user-friendly
- [x] Loading states clear
- [x] Theme integration automatic
- [x] Keyboard accessible
- [x] Mobile responsive
- [x] CORS configured for backend

**Still TODO for Full Release**: User Story 2 (text selection), comprehensive testing, production deployment

---

## Implementation Strategy

**Recommended Task Execution Order**:
1. **Phase 1** (Setup): Sequential (dependencies)
2. **Phase 2** (Foundational): Mostly sequential (types first, then APIs, then fixtures)
3. **Phase 3** (Core): Can start types in parallel, then components can be parallel
4. **Phase 4** (Integration): Can start after Phase 3 core is complete
5. **Phase 5** (Error Handling): Can start after Phase 2, in parallel with Phase 3
6. **Phase 6-9**: Sequential (depend on earlier phases)

**Parallel Opportunities**:
- Phase 2: API client, formatters, and fixtures can be parallel after types
- Phase 3: All components can be parallel after types defined
- Phase 7: Unit tests can be parallel after components exist
- Phase 8: Backend validation can start in parallel with testing

**Suggested Development Team Allocation**:
- **1 Dev**: Phases 1-2 (setup, infrastructure) - ~4 hours
- **2 Devs**: Phase 3 (components) in parallel - ~16 hours each = 32 hours total
- **1 Dev**: Phase 4 (integration) - ~8 hours
- **1 Dev**: Phase 5 (error handling) - ~12 hours
- **2 Devs**: Phase 7 (testing) in parallel - ~12 hours each = 24 hours total
- **1 Dev**: Phase 8-9 (backend validation, docs, QA) - ~16 hours

**Total Estimated Duration**: 40-50 hours for MVP (Phases 1-5)

---

## Next Steps

1. ✅ Task generation complete (165 tasks across 9 phases)
2. Run `/sp.implement` to begin Phase 1 (Setup & Dependencies)
3. Or manually start with tasks T001-T010 (project setup)
4. After Phase 1-2 complete, proceed to Phases 3-5 in parallel
5. Deploy MVP after Phase 5 (US1, US3, US4 complete)
6. Continue with Phase 6-9 for full feature set and production readiness
