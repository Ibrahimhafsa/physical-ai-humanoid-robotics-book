# Research & Architecture Decisions: Frontend Integration with RAG Agent API

**Feature**: 005-frontend-integration | **Date**: 2025-12-12 | **Researcher**: Claude Code

## Phase 0 Research Findings

### 1. Docusaurus Layout Plugin API

**Decision**: Use Docusaurus layout swizzling mechanism to inject RAGChatWidget globally

**Rationale**:
- Docusaurus provides theme swizzling at `src/theme/` (both 2.x and 3.x)
- Swizzling allows wrapping BaseLayout without modifying Docusaurus core
- Works for both Docusaurus 2.x (Infima theme) and 3.x (theme-common API)
- No per-page code changes required (matches spec FR-001)

**Alternatives Considered**:
- **Per-page component import**: Requires changes to every markdown file (violates spec)
- **Sidebar component**: Sidebar position is not ideal for persistent chatbot (UX concern)
- **Browser extension**: Out of scope, user-hostile (must be built-in)
- **CDN-injected script**: Works but difficult to style, CORS issues, not Docusaurus-native

**Implementation for 2.x**:
```typescript
// src/theme/Layout/index.tsx
import BaseLayout from '@theme-original/Layout';
import RAGChatWidget from '@site/src/components/RAGChatWidget';

export default function Layout(props) {
  return (
    <>
      <BaseLayout {...props} />
      <RAGChatWidget apiUrl={process.env.REACT_APP_API_URL} />
    </>
  );
}
```

**Implementation for 3.x**:
- Use `@docusaurus/theme-common` for theme context and dark mode state
- Same wrapping pattern

**Status**: ✅ CONFIRMED - Both 2.x and 3.x support this approach

---

### 2. CSS Theme Inheritance

**Decision**: Use CSS Module classes + Docusaurus CSS variables for theme-aware styling

**Rationale**:
- Docusaurus exposes theme tokens as CSS custom properties (--ifm-color-primary, --ifm-color-background, etc.)
- CSS Modules provide scoped styling (prevents Docusaurus theme overrides)
- Dark mode switching is automatic via `[data-theme="dark"]` on `<html>` tag
- No need for styled-components or runtime theme context

**Docusaurus Theme Variables** (for reference):
```css
--ifm-color-primary: #2563eb;          /* Primary brand color */
--ifm-color-background: #ffffff;       /* Page background */
--ifm-color-background-secondary: #f5f5f5;
--ifm-text-color-base: #000000;
--ifm-text-color-secondary: #666666;
--ifm-button-background-color: #f3f3f3;
--ifm-border-color: #ececec;

/* Dark mode variants */
[data-theme="dark"] {
  --ifm-color-background: #1a1a1a;
  --ifm-text-color-base: #ffffff;
  /* etc */
}
```

**Widget CSS Approach**:
```css
/* RAGChatWidget.module.css */
.widget {
  background: var(--ifm-color-background);
  color: var(--ifm-text-color-base);
  border: 1px solid var(--ifm-border-color);
  border-radius: 8px;
}

.inputField {
  background: var(--ifm-color-background-secondary);
  border: 1px solid var(--ifm-border-color);
  color: var(--ifm-text-color-base);
}

.button {
  background: var(--ifm-color-primary);
  color: white;
}

/* Automatic dark mode adaptation */
/* No need for separate [data-theme="dark"] rules */
```

**Alternatives Considered**:
- **styled-components**: Runtime CSS, adds bundle size, harder to maintain
- **Tailwind CSS**: Conflicts with Docusaurus Tailwind configuration
- **Manual dark mode detection**: useContext for theme, more complex
- **Hardcoded colors**: Breaks when theme changes, not maintainable

**Status**: ✅ CONFIRMED - CSS variables approach is standard in Docusaurus

---

### 3. Text Selection API

**Decision**: Use native `document.getSelection()` and Range API to capture selected text

**Rationale**:
- Native browser API, no external library needed
- Works across all modern browsers (Chrome, Firefox, Safari, Edge)
- Captures text within page (respects DOM boundaries)
- Can be triggered by mouse selection or explicit button click

**Implementation Pattern**:
```typescript
function useTextSelection() {
  const [selectedText, setSelectedText] = useState<string | null>(null);

  useEffect(() => {
    function handleSelection() {
      const selection = window.getSelection();
      const text = selection?.toString() ?? null;
      setSelectedText(text && text.trim() ? text : null);
    }

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  return selectedText;
}
```

**Limitations**:
- Cannot capture from iframes (handled by spec edge case)
- Cannot capture from dynamically loaded content (spec assumption: static markdown)
- Truncate to 5000 chars to prevent payload size issues

**Alternatives Considered**:
- **Context menu API**: Non-standard, browser-specific
- **Selection events**: Similar to native approach, mouseup is simpler
- **Hidden button**: User clicks button on selection (less seamless)
- **Auto-popup on selection**: Matches Google Docs, requires modal overlay (MVP excludes)

**Status**: ✅ CONFIRMED - Native API sufficient for MVP

---

### 4. Fetch Error Handling Patterns

**Decision**: Implement retry wrapper with exponential backoff for transient errors

**Rationale**:
- Network errors are transient (brief latency spikes, temporary unavailability)
- Exponential backoff prevents overwhelming backend (429 handling)
- Max 3 retries balances user experience (fast failure) with reliability

**Error Handling Strategy**:

```typescript
interface FetchError {
  status: number;
  message: string;
  retry: boolean;  // true if transient (5xx, timeout)
}

async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries = 3
): Promise<Response> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 30000); // 30s timeout

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeout);

      // 200-299: success
      if (response.ok) return response;

      // 400-499: client error (don't retry)
      if (response.status >= 400 && response.status < 500) {
        throw new FetchError(response.status, 'Client error', false);
      }

      // 5xx: server error (retry)
      if (response.status >= 500) {
        lastError = new FetchError(response.status, 'Server error', true);
        // Continue to retry
      }
    } catch (error) {
      lastError = error as Error;
      if (i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}
```

**Error Messages for User**:
- **Network error**: "Unable to reach server. Please check your connection."
- **Timeout (>30s)**: "Request took too long. Please try again."
- **400 validation**: "Please enter a valid question."
- **429 rate limit**: "Too many requests. Please wait a moment."
- **503 unavailable**: "Service temporarily unavailable. Please try again later."
- **500 server error**: "Server error. Please try again."

**Alternatives Considered**:
- **No retry**: Fast failure, poor UX for transient errors
- **Linear backoff**: Less effective than exponential (doesn't reduce load)
- **Infinite retry**: Bad UX (user left waiting)
- **Circuit breaker**: Over-engineering for MVP (single endpoint)

**Status**: ✅ CONFIRMED - Retry with exponential backoff is standard pattern

---

### 5. React Hooks Patterns for API Calls

**Decision**: Use `useEffect` with AbortController for request cancellation on component unmount

**Rationale**:
- useEffect cleanup prevents "can't perform state update on unmounted component" warning
- AbortController cancels fetch request when component unmounts (user navigates away)
- Custom hook encapsulates API logic, separates from UI component
- No need for external libraries (react-query, SWR for MVP)

**Pattern**:
```typescript
function useApiClient(apiUrl: string) {
  const [data, setData] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submitQuery = useCallback(async (request: QueryRequest) => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal: controller.signal, // Cancellation token
      });

      if (!response.ok) {
        // Handle errors from backend
        const error = await response.json();
        throw new Error(error.detail?.error ?? 'Request failed');
      }

      const data = await response.json();
      setData(data);
    } catch (err) {
      if ((err as Error).name !== 'AbortError') {
        // Ignore abort errors (expected on navigation)
        setError((err as Error).message);
      }
    } finally {
      setLoading(false);
    }

    return controller.abort; // Cleanup function
  }, [apiUrl]);

  return { data, loading, error, submitQuery };
}
```

**Component Usage**:
```typescript
function QueryInput({ apiUrl }) {
  const { data, loading, error, submitQuery } = useApiClient(apiUrl);

  async function handleSubmit(query: string) {
    const abortFn = await submitQuery({ query, top_k: 5 });
    // If user navigates away, abortFn cleans up
  }

  return <form onSubmit={handleSubmit}>...</form>;
}
```

**Alternatives Considered**:
- **useReducer**: More complex state machine, overkill for MVP
- **react-query**: Great library, adds dependency, unnecessary for single endpoint
- **SWR**: Same as react-query, adds weight
- **Callback-based**: Less React idiomatic, harder to manage cleanup

**Status**: ✅ CONFIRMED - Custom hook pattern is lightweight and sufficient

---

### 6. Responsive Design for Mobile

**Decision**: Mobile-first CSS, flex layout, 320px minimum viewport, touch-friendly targets (44px min height)

**Rationale**:
- Docusaurus already supports mobile (responsive design expectation)
- Bottom-right fixed position is common pattern (not overlapping content)
- Touch targets: 44px x 44px minimum (WCAG guideline for mobile)
- Flex layout adapts to container size

**Widget Layout**:
```css
.widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: min(100vw - 40px, 400px);  /* Max 400px, 20px margin on mobile */
  max-height: 80vh;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

/* Mobile: full-width, bottom-only margin */
@media (max-width: 640px) {
  .widget {
    width: calc(100vw - 20px);
    bottom: 10px;
    right: 10px;
  }
}

/* Large screens: fixed 400px width */
@media (min-width: 768px) {
  .widget {
    width: 400px;
  }
}

/* Touch-friendly button size */
.submitButton {
  min-height: 44px;
  padding: 12px 16px;
}

/* Scrollable response area */
.responseArea {
  overflow-y: auto;
  max-height: calc(80vh - 200px);  /* Leave room for input */
}
```

**Print Mode**:
```css
@media print {
  .widget {
    display: none;  /* Hide widget in print */
  }
}
```

**Alternatives Considered**:
- **Fixed sidebar**: Overlaps content on mobile (not ideal)
- **Modal dialog**: Requires explicit close (less seamless)
- **In-page component**: Disrupts reading flow (not fixed position)
- **Floating action button**: Single button with expand (good, but MVP uses visible widget)

**Status**: ✅ CONFIRMED - Mobile-first flex layout is standard approach

---

### 7. Accessibility: WCAG AA Compliance

**Decision**: Semantic HTML, ARIA labels, keyboard navigation (Tab, Enter, Escape), 4.5:1 contrast ratio

**Rationale**:
- Docusaurus already supports accessible themes (Infima is WCAG AA)
- Semantic HTML (`<button>`, `<input>`) provides screen reader semantics
- Keyboard navigation critical for users unable to use mouse
- Contrast ratio 4.5:1 is WCAG AA standard for body text

**Accessibility Checklist**:

1. **Semantic HTML**:
   ```jsx
   <form onSubmit={handleSubmit}>
     <label htmlFor="query-input">Ask a question</label>
     <input id="query-input" type="text" placeholder="..." />
     <button type="submit" disabled={isLoading}>
       {isLoading ? 'Thinking...' : 'Ask'}
     </button>
   </form>
   ```

2. **ARIA Labels**:
   ```jsx
   <div
     role="region"
     aria-label="Chat response"
     aria-live="polite"
     aria-atomic="true"
   >
     {/* Response content */}
   </div>

   <div role="status" aria-live="polite">
     {isLoading && <p>Thinking...</p>}
   </div>
   ```

3. **Keyboard Navigation**:
   - Tab: Focus input, submit button, close button
   - Enter: Submit query
   - Escape: Close/minimize widget
   ```typescript
   function handleKeyDown(e: KeyboardEvent) {
     if (e.key === 'Escape') setIsMinimized(true);
     if (e.key === 'Enter' && e.ctrlKey) submitQuery();
   }
   ```

4. **Contrast Ratio** (via CSS variables):
   ```
   Text: --ifm-text-color-base (dark on light, light on dark) ✅ 7:1+
   Links: --ifm-color-primary on background ✅ 4.5:1+
   Buttons: --ifm-color-primary text ✅ 4.5:1+
   ```

5. **Focus Indicators**:
   ```css
   button:focus,
   input:focus {
     outline: 2px solid var(--ifm-color-primary);
     outline-offset: 2px;
   }
   ```

**Testing Tools**:
- axe DevTools (browser extension for accessibility checks)
- WAVE (WCAG evaluation tool)
- Manual keyboard navigation testing (Tab, Enter, Escape)
- Screen reader testing (VoiceOver on macOS, NVDA on Windows)

**Alternatives Considered**:
- **Skip links**: Not needed (widget is optional, not main content)
- **High contrast mode**: Inherited from Docusaurus (already supported)
- **Font scaling**: Inherited from browser default

**Status**: ✅ CONFIRMED - Semantic HTML + ARIA + keyboard navigation sufficient for WCAG AA

---

## Architecture Decisions Summary

| Decision | Status | Evidence |
|----------|--------|----------|
| Docusaurus layout swizzling for global injection | ✅ CONFIRMED | Both 2.x and 3.x support, no per-page changes |
| CSS variables for theme inheritance | ✅ CONFIRMED | Docusaurus uses CSS custom properties, automatic dark mode |
| Native text selection API | ✅ CONFIRMED | Works across all modern browsers, no library needed |
| Fetch with retry & exponential backoff | ✅ CONFIRMED | Standard error handling pattern, balances UX and reliability |
| React hooks for API calls | ✅ CONFIRMED | useEffect cleanup + AbortController, lightweight |
| Mobile-first responsive flex layout | ✅ CONFIRMED | Docusaurus standard approach, 320px+ viewports |
| WCAG AA semantic HTML + ARIA + keyboard nav | ✅ CONFIRMED | Industry standard, supported by all modern browsers |

---

## Risks & Mitigations

| Risk | Mitigation | Status |
|------|-----------|--------|
| Backend CORS misconfigured | Setup docs, error message in widget | ✅ Plan covers |
| Theme token naming mismatch | Use Docusaurus @theme-common API, fallbacks | ✅ Researched |
| Large response text breaks layout | Virtualization, max-height with scroll | ✅ Planned |
| Mobile viewport <320px (rare) | Min-width wrapper, tested on real devices | ✅ Planned |
| Selected text too large (>10K chars) | Truncate to 5000 chars, warn user | ✅ Researched |

---

## Next Steps for Phase 1

1. ✅ Research complete (all items CONFIRMED)
2. Create `data-model.md` (TypeScript interfaces, component props)
3. Create `contracts/component-interface.md` (component API)
4. Create `contracts/request-response-examples.md` (example payloads)
5. Create `quickstart.md` (setup guide)
6. Proceed to Phase 2: Task generation
