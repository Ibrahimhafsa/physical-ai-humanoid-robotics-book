---
id: 002
title: Feature 005 Implementation Plan - Docusaurus Frontend Integration
stage: plan
date: 2025-12-12
surface: agent
model: claude-haiku-4-5-20251001
feature: 005-frontend-integration
branch: 005-frontend-integration
user: system
command: /sp.plan
labels: ["planning", "architecture", "frontend", "react", "docusaurus", "design", "phase-1"]
links:
  spec: specs/005-frontend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-frontend-integration/plan.md
  - specs/005-frontend-integration/research.md
  - specs/005-frontend-integration/data-model.md
tests: []
---

## Prompt

User executed `/sp.plan` command with specific implementation guidance:

**User Input**:
```
- Create `/src/components/RAGChatWidget` in Docusaurus.
- Add API call util to POST queries to FastAPI backend.
- Implement UI with input box + selected-text injection.
- Add global layout plugin to mount the widget.
- Test full request cycle with local backend.
```

**Task**: Create comprehensive implementation plan (architecture, design, component structure) without writing code.

## Response snapshot

**Feature 005 Implementation Plan Complete**: Comprehensive technical architecture and design for Docusaurus frontend integration with RAG Agent API, including research findings, data models, and component design specifications.

**Planning Artifacts Created** (3 files, 1300+ lines):

### 1. Implementation Plan (`specs/005-frontend-integration/plan.md` - 550 lines)

**Technical Context**:
- Language: React 18+ with TypeScript recommended
- Framework: Docusaurus 2.x/3.x with native Fetch API
- Performance: <500ms widget load, <5s backend latency, <100ms UI response
- Storage: Browser memory only (no localStorage for MVP)
- Scale: 10+ concurrent requests, responsive down to 320px viewport

**Constitution Check**: ✅ **PASS** (all 6 principles satisfied)
- Principle I: Education-first design (clear UI feedback, learner-focused)
- Principle II: Practical/engineering-focused (real book content, passage-specific)
- Principle III: Content accuracy & safety (source attribution, backend context-only)
- Principle IV: Docusaurus standards (theme inheritance, global integration)
- Principle V: Testable/reproducible (mocked backend, local development)
- Principle VI: Iterative improvement (modular components, configurable, logging)

**Project Structure** (repository layout):
```
book-docs/src/
├── components/RAGChatWidget/        # NEW: Chatbot widget
│   ├── index.tsx                    # Main component
│   ├── ChatWidget.tsx               # Container with state
│   ├── QueryInput.tsx               # User input
│   ├── ResponseDisplay.tsx          # Answer + sources
│   ├── SourceList.tsx               # Sources list
│   ├── LoadingState.tsx, ErrorState.tsx
│   ├── useTextSelection.ts, useApiClient.ts  # Custom hooks
│   ├── types.ts                     # TypeScript interfaces
│   ├── RAGChatWidget.module.css     # Scoped styles
│   └── __tests__/                   # Unit tests
│
├── components/RAGChatLayout/        # NEW: Docusaurus layout plugin
│   ├── index.tsx                    # Layout wrapper
│   └── __tests__/
│
├── utils/
│   ├── apiClient.ts                 # API utilities (fetchQuery, handleErrors)
│   └── formatters.ts                # Text formatting utilities
│
├── theme/
│   └── RAGChatWidget.css            # Optional: global theme tokens
│
└── pages/                           # Existing Docusaurus pages
```

**Architecture Decisions** (8 major decisions documented):
- Custom layout plugin (vs per-page): Global injection, no per-page changes
- React hooks (vs Redux): Minimal dependencies, local state sufficient
- CSS Modules (vs Tailwind/styled-components): Scoped styles prevent theme conflicts
- Fetch API (vs axios): Native browser API, no external dependency
- Ephemeral sessions (vs localStorage): Privacy-respecting, simpler state
- String-based text selection (vs DOM nodes): Backend-agnostic, simpler
- AbortController for cancellation (vs fire-and-forget): Better UX for navigation
- Client-side validation (vs backend-only): Fast feedback, reduces backend load

**Phase Breakdown**:
- **Phase 0**: Research & architecture decisions (COMPLETE)
- **Phase 1**: Data model & API contracts (IN PROGRESS)
- **Phase 2**: Implementation tasks (150+ tasks, 6 phases)

### 2. Research & Architecture Decisions (`specs/005-frontend-integration/research.md` - 400 lines)

**Research Findings** (7 key areas):

1. **Docusaurus Layout Plugin API** ✅ CONFIRMED
   - Layout swizzling at `src/theme/Layout/index.tsx`
   - Works for both 2.x (Infima) and 3.x (@theme-common)
   - No per-page code changes required
   - Wrap BaseLayout component with RAGChatWidget

2. **CSS Theme Inheritance** ✅ CONFIRMED
   - Docusaurus exposes theme tokens as CSS custom properties
   - CSS Modules + CSS variables approach recommended
   - Automatic dark mode via `[data-theme="dark"]` on `<html>`
   - No styled-components or runtime theme context needed

3. **Text Selection API** ✅ CONFIRMED
   - Native `document.getSelection()` + Range API
   - Works across all modern browsers
   - Capture on mouseup event
   - Truncate to 5000 chars to prevent payload size issues

4. **Fetch Error Handling** ✅ CONFIRMED
   - Retry with exponential backoff (1s, 2s, 4s)
   - Max 3 retries balances UX and reliability
   - 30s timeout for request
   - User-friendly error messages (no technical jargon)

5. **React Hooks Patterns** ✅ CONFIRMED
   - useEffect cleanup + AbortController for cancellation
   - Custom hooks for API calls (useApiClient)
   - Custom hooks for text selection (useTextSelection)
   - No need for redux/react-query for MVP

6. **Responsive Design** ✅ CONFIRMED
   - Mobile-first CSS with flex layout
   - Min viewport 320px (with 20px margins)
   - Fixed position bottom-right (standard pattern)
   - Touch targets 44px x 44px minimum (WCAG)
   - Print mode: hide widget with @media print

7. **Accessibility: WCAG AA** ✅ CONFIRMED
   - Semantic HTML (`<button>`, `<input>`, `<label>`)
   - ARIA labels for screen readers (role, aria-label, aria-live)
   - Keyboard navigation: Tab, Enter, Escape
   - Focus indicators on interactive elements
   - 4.5:1 contrast ratio via CSS variables

**Architecture Decision Table** (8 decisions with rationale & alternatives):

| Decision | Status | Rationale | Alternatives |
|----------|--------|-----------|--------------|
| Layout swizzling | ✅ CONFIRMED | Global, no per-page changes | Per-page (intrusive), sidebar (not ideal) |
| CSS variables | ✅ CONFIRMED | Theme inheritance, auto dark mode | Styled-components (adds weight), Tailwind (conflicts) |
| Text selection API | ✅ CONFIRMED | Native, no library | Context menu API (non-standard), button click (less seamless) |
| Fetch + retry | ✅ CONFIRMED | Standard pattern, balances UX/reliability | No retry (poor UX), circuit breaker (overkill) |
| React hooks | ✅ CONFIRMED | Lightweight, local state sufficient | Redux (overkill), SWR/react-query (unnecessary) |
| Mobile-first flex | ✅ CONFIRMED | Docusaurus standard, responsive | Fixed sidebar (overlaps), modal (less seamless) |
| WCAG AA semantic HTML | ✅ CONFIRMED | Industry standard, all modern browsers | Skip links (not needed), custom accessibility (error-prone) |
| Ephemeral sessions | ✅ CONFIRMED | Privacy-respecting, spec-aligned | localStorage (privacy concerns, adds complexity) |

**Risks & Mitigations** (5 key risks):

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Backend CORS misconfigured | Widget cannot reach backend | Clear error, setup docs, backend coordination |
| Theme token naming mismatch | Widget styling breaks | Use @theme-common API, test dark mode |
| Large response text (>10K chars) | UI layout broken | Virtualization, max-height scroll |
| Mobile viewport <320px (rare) | Widget unusable | Min-width wrapper, test on real devices |
| Selected text too large (>10K) | Request fails/timeout | Truncate to 5000 chars, warn user |

### 3. Data Model (`specs/005-frontend-integration/data-model.md` - 350 lines)

**Entity Definitions** (6 core entities):

1. **ChatMessage** (Internal widget state)
   - id: UUID or timestamp-based
   - role: 'user' | 'assistant'
   - content: Text (max 10K)
   - timestamp: Date
   - sources?: RetrievalSource[] (for assistant messages)
   - selectedText?: string (optional, from user)
   - error?: string (optional, if request failed)
   - metadata?: { durationMs, tokensUsed, contextUsed }

2. **RetrievalSource** (From backend response)
   - chunk_id: Backend identifier
   - text: Snippet (truncate to 200 chars for display)
   - similarity_score: 0.0-1.0
   - source_url: Docusaurus page URL
   - section_title: Chapter/section name
   - rank: 1-10 (most to least relevant)

3. **QueryRequest** (Sent to backend)
   - query: Required, non-empty, max 1000 chars
   - top_k?: Optional, range 1-20, default 5
   - similarity_threshold?: Optional, range 0.0-1.0, default 0.5
   - context?: Optional, max 5000 chars (selected text)
   - user_id?, session_id?: Future use (not MVP)

4. **ChatResponse** (From backend)
   - request_id: UUID for tracing
   - answer: Generated response text
   - sources: RetrievalSource[], 0-10 items
   - context_used: Count of chunks used
   - tokens_used: Token count
   - response_time_ms: Latency
   - timestamp: ISO 8601
   - note?: Optional metadata

5. **ErrorResponse** (From backend on errors)
   - detail.error: Error type ("Validation Error", "Service Unavailable", etc.)
   - detail.details?: Array of field errors
   - detail.request_id?: For tracing
   - timestamp?: Optional

6. **WidgetState** (React component state)
   - messages: ChatMessage[] (max 50)
   - isLoading: boolean
   - error: string | null
   - selectedText: string | null
   - isMinimized: boolean
   - apiUrl: string (backend endpoint)
   - sessionId: string (generated once on mount)
   - lastRequest?: QueryRequest
   - lastResponse?: ChatResponse

**Component Props Interfaces**:

**RAGChatWidget Props**:
```typescript
{
  apiUrl: string;                     // REQUIRED: Backend endpoint
  position?: 'bottom-right' | 'bottom-left' | 'top-right';
  theme?: 'light' | 'dark' | 'auto';  // Default: 'auto'
  enableTextSelection?: boolean;      // Default: true
  maxMessages?: number;               // Default: 50
  className?: string;
  onError?: (error: Error) => void;
}
```

**QueryInput Props**: onSubmit, isLoading, error, selectedText, onClearSelection
**ResponseDisplay Props**: message, onSourceClick
**SourceList Props**: sources, onSourceClick

**Validation Rules** (per entity):

| Entity | Field | Rule | Example |
|--------|-------|------|---------|
| ChatMessage | id | Unique, non-empty | UUID |
| ChatMessage | role | 'user' \| 'assistant' | 'user' |
| QueryRequest | query | Non-empty, max 1K | "What is kinematics?" |
| QueryRequest | top_k | Range [1, 20] | 5 |
| QueryRequest | similarity_threshold | Range [0.0, 1.0] | 0.5 |
| RetrievalSource | similarity_score | Range [0.0, 1.0] | 0.89 |
| ChatResponse | request_id | UUID | "550e8400-..." |
| ChatResponse | answer | Non-empty string | "Kinematics is..." |

## Outcome

- ✅ Impact: Feature 005 implementation plan complete and ready for task generation. Comprehensive technical architecture with 3 planning artifacts (plan.md, research.md, data-model.md). All 8 architecture decisions researched and documented with rationale and alternatives. Constitution check passed (6/6 principles satisfied). Component structure designed, data models defined with TypeScript interfaces, validation rules specified. Plan covers all requirements from specification and user input (widget component, API client utilities, UI with text selection, layout plugin, backend integration).

- 🧪 Tests: Plan quality validated through:
  - ✅ Constitution check (all 6 principles pass)
  - ✅ Architecture decision documentation (8 decisions confirmed via research)
  - ✅ Risk analysis (5 key risks identified with mitigations)
  - ✅ Data model validation rules (all entities have constraints)
  - Ready for Phase 2 task generation

- 📁 Files: 3 artifacts created:
  - `specs/005-frontend-integration/plan.md` (550 lines): Technical context, constitution check, project structure, phase breakdown, success criteria
  - `specs/005-frontend-integration/research.md` (400 lines): 7 research findings, 8 architecture decisions with tables, risk analysis
  - `specs/005-frontend-integration/data-model.md` (350 lines): 6 entity definitions, component props, validation rules, examples

- 🔁 Next prompts: `/sp.tasks` to generate 150+ implementation tasks across 6 phases (Phase 1: setup, Phase 2: API client, Phase 3: widget core, Phase 4: UX/errors, Phase 5: text selection + integration, Phase 6: testing). Then `/sp.implement` to execute MVP implementation.

- 🧠 Reflection: Implementation plan successfully translates Feature 005 specification into actionable technical architecture. Architecture decisions are researched and justified (7 research findings, 8 decisions documented with alternatives). Component structure matches user requirements (RAGChatWidget, QueryInput, ResponseDisplay, SourceList, layout plugin). Data models are well-defined with TypeScript interfaces and validation rules. Constitution check confirms design aligns with project principles (education-first, practical, safe, testable, iterable). Plan is ready for detailed task generation and implementation execution.

## Evaluation notes (flywheel)

- Failure modes observed: None. Plan created without blockers. All architecture decisions confirmed through research. Constitution check passed (6/6 principles). No unresolved clarifications.

- Graders run and results (PASS/FAIL):
  - ✅ Technical Context: Complete (language, framework, dependencies, performance goals, constraints)
  - ✅ Constitution Check: All 6 principles pass (education-first, practical, safe, accurate, testable, iterable)
  - ✅ Project Structure: Clear directory layout, modular components, separation of concerns
  - ✅ Architecture Decisions: 8 decisions researched and documented with rationale + alternatives
  - ✅ Data Model: 6 entities defined, TypeScript interfaces, validation rules, constraints
  - ✅ Component Design: Props interfaces defined, state management clear, hooks patterns chosen
  - ✅ Research Findings: 7 areas researched (Docusaurus API, CSS theme, text selection, fetch patterns, hooks, responsive, accessibility)
  - ✅ Risk Analysis: 5 key risks identified with mitigations
  - ✅ Phase Breakdown: Clear phases (0: research, 1: design, 2: implementation with 6 sub-phases)
  - ✅ Success Criteria: All 12 SC from spec addressed in plan (latency, responsiveness, accessibility, etc.)

- Prompt variant (if applicable): null

- Next experiment: Run `/sp.tasks` to generate 150+ implementation tasks organized as:
  - Phase 1: Setup (10 tasks) - dependencies, TypeScript, test infrastructure
  - Phase 2: API Client (20 tasks) - fetch wrapper, error handling, validation
  - Phase 3: Widget Core (40 tasks) - ChatWidget, QueryInput, ResponseDisplay, SourceList, state management
  - Phase 4: UX/Errors (30 tasks) - LoadingState, ErrorState, empty results, accessibility, theme switching
  - Phase 5: Text Selection + Integration (30 tasks) - useTextSelection hook, Docusaurus layout plugin, global injection
  - Phase 6: Testing + Docs (20+ tasks) - unit tests, integration tests, E2E with backend, documentation

---

**Implementation Plan Status**: ✅ COMPLETE AND READY FOR TASK GENERATION

**Planning Artifacts**: 3 files, 1300+ lines
- plan.md: Technical architecture (550 lines)
- research.md: Architecture decisions (400 lines)
- data-model.md: Entities & validation (350 lines)

**Next Step**: `/sp.tasks` to generate 150+ implementation tasks

**Architecture Summary**:
- **Pattern**: Docusaurus layout swizzling with React hooks
- **Styling**: CSS Modules + Docusaurus theme variables
- **API**: Fetch with exponential backoff retry
- **State**: React hooks (useEffect + AbortController)
- **Accessibility**: WCAG AA semantic HTML + ARIA + keyboard nav
- **Responsive**: Mobile-first flex layout (320px+)
- **Error Handling**: User-friendly messages, retry logic, graceful degradation
- **Validation**: Client-side validation before backend call
- **Constitution**: ✅ All 6 principles satisfied

**Key Decisions Confirmed**:
- ✅ Layout swizzling (no per-page changes)
- ✅ CSS variables (theme inheritance, auto dark mode)
- ✅ Text selection API (native, no library)
- ✅ Fetch + retry (standard pattern)
- ✅ React hooks (minimal deps)
- ✅ Mobile-first (responsive)
- ✅ WCAG AA (semantic HTML)
- ✅ Ephemeral sessions (privacy-respecting)
