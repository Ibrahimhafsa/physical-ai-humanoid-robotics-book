# RAG Chat Widget - Troubleshooting Guide

## Issue: Ask AI Button Not Returning Responses

This guide helps you debug why the "Ask AI" button isn't working and receiving responses from the FastAPI backend.

---

## Quick Diagnosis Checklist

- [ ] **Backend is running** on the configured API URL
- [ ] **API URL is correct** in `.env` (includes `/ask` path)
- [ ] **CORS headers** are properly configured on backend
- [ ] **Network request succeeds** (check browser Network tab)
- [ ] **Response format matches** expected structure
- [ ] **Console has no errors** (check browser DevTools)

---

## Diagnosis Steps (In Order)

### Step 1: Verify Backend is Running

The most common issue is that the backend isn't running or is on a different port.

**Check if backend is listening on port 8000:**

```bash
# On Linux/Mac
lsof -i :8000

# On Windows
netstat -ano | findstr :8000

# Using curl (any OS)
curl -v http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-14T10:30:00Z"
}
```

**If backend is not running:**
1. Navigate to the `backend/` directory
2. Activate your Python virtual environment: `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows)
3. Start the backend:
   ```bash
   python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
   ```
4. Wait for the message: `INFO:     Uvicorn running on http://0.0.0.0:8000`

---

### Step 2: Verify API URL Configuration

Check that your frontend knows where to find the backend.

**In your browser, open the DevTools Console and run:**

```javascript
// Check the API URL being used
console.log('API URL:', window.__RAG_API_URL__ || process.env.REACT_APP_API_URL)
```

**Expected output:**
```
API URL: http://localhost:8000
```

**Note:** The URL is the **base URL only** (no `/ask`). The widget's `apiClient.ts` automatically appends `/ask` when making requests.

**If the URL is wrong:**

1. Edit `book-docs/.env` and set the correct API URL (base URL only):
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

2. Stop and restart your dev server:
   ```bash
   # Stop: Ctrl+C
   npm run start  # or npm start
   ```

3. The browser may cache old values. Do a **hard refresh**:
   - Windows/Linux: `Ctrl+Shift+Delete`
   - Mac: `Cmd+Shift+Delete`

---

### Step 3: Monitor Network Request

Use the browser Network tab to see what's actually being sent and received.

**Steps:**
1. Open DevTools: `F12` (Windows/Linux) or `Cmd+Option+I` (Mac)
2. Click the **Network** tab
3. Type a question in the widget and click **Ask**
4. Look for a request to `/ask` (or your configured API URL)
5. Click on it to inspect:
   - **Request**: Method (POST), Headers, Body
   - **Response**: Status code, Headers, Body

**Common issues:**

| Status | Meaning | Fix |
|--------|---------|-----|
| **Pending / No response** | Backend not reachable | Start backend (Step 1) |
| **CORS error** | Cross-origin not allowed | Configure CORS on backend |
| **404** | Wrong endpoint path | Ensure URL includes `/ask` path |
| **400** | Validation error | Check request body format |
| **503** | Backend error | Check backend logs |

---

### Step 4: Check Console Logs

The widget logs debug info to help diagnose issues.

**In DevTools Console, look for messages like:**

```
[RAGChatWidget] Using injected API URL: http://localhost:8000/ask
[RAGChatWidget] Sending query request: {...}
[RAGChatWidget] Received response: {status: 200, ok: true}
```

**If you see network errors:**

```
[RAGChatWidget] Network error: {
  message: "Failed to fetch",
  apiUrl: "http://localhost:8000/ask",
  error: "TypeError: Failed to fetch"
}
```

**This usually means:**
- Backend is not running
- CORS is not configured
- API URL is incorrect

---

## Solution: Configuration for Different Environments

### Local Development

1. **Start backend:**
   ```bash
   cd backend
   python -m uvicorn src.api:app --reload
   ```

2. **Configure frontend `.env`:**
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```
   **Important:** Use the base URL only (no `/ask` suffix). The widget automatically appends `/ask`.

3. **Start frontend:**
   ```bash
   cd book-docs
   npm run start
   ```

4. **Test:** Open `http://localhost:3000`, try the Ask button

---

### Production Deployment (Vercel, GitHub Pages, etc.)

The backend must be deployed to a public URL accessible from your frontend domain.

**Option A: Using Environment Variables (Recommended)**

1. In your deployment platform (Vercel, GitHub Actions, etc.), set:
   ```
   REACT_APP_API_URL=https://rag-backend-fastapi.onrender.com
   ```
   **Important:** Use the base URL only (no `/ask` suffix). The widget automatically appends `/ask`.

2. During build:
   ```bash
   export REACT_APP_API_URL=https://rag-backend-fastapi.onrender.com
   npm run build
   ```

**Option B: Runtime Injection**

If you need to change the API URL without rebuilding, inject it into the HTML:

In `book-docs/docusaurus.config.js`, modify the HTML template to inject:
```html
<script>
  window.__RAG_API_URL__ = "https://rag-backend-fastapi.onrender.com";
</script>
```
**Note:** Again, use base URL only (no `/ask`).

---

## CORS Configuration

If you see a **CORS error** in the browser console, the backend needs to be configured to accept requests from your frontend domain.

**Backend CORS is already configured** in `backend/src/api.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production, restrict CORS to your domain:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Request/Response Format

Make sure the frontend is sending the correct format and the backend is responding correctly.

**Frontend sends (POST /ask):**
```json
{
  "query": "What is physical AI?",
  "top_k": 5,
  "similarity_threshold": 0.5,
  "context": "optional selected text",
  "session_id": "optional"
}
```

**Backend responds (200 OK):**
```json
{
  "request_id": "uuid",
  "answer": "Physical AI refers to...",
  "sources": [
    {
      "chunk_id": "chunk_123",
      "text": "relevant excerpt...",
      "similarity_score": 0.87,
      "source_url": "/docs/page",
      "section_title": "Section Title",
      "rank": 1
    }
  ],
  "context_used": 3,
  "tokens_used": 487,
  "response_time_ms": 1850,
  "timestamp": "2025-12-14T10:30:00Z"
}
```

**If the response format doesn't match, the widget won't display it.** Check `backend/src/models/chat.py` for the exact structure.

---

## Backend Logs

Check the backend logs to see if the request even reaches the server.

**You should see entries like:**
```
INFO:     POST /ask HTTP/1.1
INFO:     [request-id-uuid] Query: What is physical AI?...
INFO:     [request-id-uuid] Response: 456 chars, 487 tokens, 1850ms, 3 sources
```

**If you see errors:**
```
ERROR:     [request-id-uuid] Processing error: Connection refused
```

This means the backend encountered an error (e.g., Qdrant is not reachable).

---

## Common Issues & Solutions

### Issue: "Unable to reach server"

**Cause:** Backend is not running or API URL is wrong

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `.env` file has correct `REACT_APP_API_URL`
3. Restart frontend dev server

---

### Issue: CORS error in console

**Cause:** Backend doesn't allow requests from frontend domain

**Solution:**
1. Check backend CORS config in `backend/src/api.py`
2. For development, `allow_origins=["*"]` is fine
3. For production, whitelist your frontend domain

---

### Issue: "Service temporarily unavailable" (503)

**Cause:** Backend is running but encountered an error (e.g., Qdrant not reachable)

**Solution:**
1. Check backend logs for detailed error
2. Verify Qdrant is running and accessible
3. Verify Cohere API key is set in `.env`

---

### Issue: "Request took too long"

**Cause:** Backend processing took >30 seconds

**Solution:**
1. Check backend logs for slow operations
2. Increase timeout in `book-docs/src/utils/apiClient.ts` (if needed)
3. Optimize backend query processing

---

### Issue: Widget shows empty response

**Cause:** Backend returned 0 sources (no matches found)

**Solution:**
1. Try a different query that's more likely to match book content
2. Check `similarity_threshold` in request (lower it to get more matches)
3. Verify Qdrant collection has embeddings loaded

---

## Advanced Debugging

### Enable Request Logging

To see detailed logs, open the browser console while running in development mode:

```javascript
// Check environment
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('API URL:', process.env.REACT_APP_API_URL);
console.log('Window injection:', window.__RAG_API_URL__);
```

### Test API Endpoint Directly

Use curl or Postman to test the backend directly:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is physical AI?",
    "top_k": 5,
    "similarity_threshold": 0.5
  }'
```

**Expected response (200 OK):**
```json
{
  "request_id": "...",
  "answer": "...",
  "sources": [...],
  ...
}
```

---

## Getting Help

If the widget still doesn't work:

1. **Check the logs:**
   - Browser console (DevTools F12)
   - Backend logs (terminal where you started the backend)

2. **Verify each step:**
   - Backend running on the right port
   - API URL in `.env` is correct
   - Network request shows successful response

3. **Report the issue with:**
   - Browser console output (copy entire error)
   - Backend logs (copy relevant error messages)
   - Network tab screenshot (show the failed request)
   - Your `.env` file (API URL)

---

## Configuration Reference

### Frontend (.env)

```env
# REQUIRED: Backend API base URL (no /ask suffix)
# The widget automatically appends /ask when making requests
REACT_APP_API_URL=https://rag-backend-fastapi.onrender.com

# OPTIONAL: Widget settings
REACT_APP_WIDGET_POSITION=bottom-right
REACT_APP_WIDGET_MAX_MESSAGES=50
REACT_APP_ENABLE_TEXT_SELECTION=true
```

### Backend (backend/.env)

```env
# Cohere for embeddings
COHERE_API_KEY=your-api-key
COHERE_MODEL=embed-3-large

# Qdrant for vector search
QDRANT_URL=https://your-qdrant-instance.com:6333
QDRANT_API_KEY=your-api-key
QDRANT_COLLECTION=book_embeddings

# Configuration
SIMILARITY_THRESHOLD=0.5
TOP_K=5
MAX_CONTEXT_TOKENS=6000
LOG_LEVEL=INFO
```

---

## Summary

The Ask AI button requires:

1. ✅ **Backend running** on the configured port
2. ✅ **API URL correct** in `.env` (base URL only, no `/ask`)
   - Example: `REACT_APP_API_URL=https://rag-backend-fastapi.onrender.com`
   - The widget's `apiClient.ts` automatically appends `/ask`
3. ✅ **CORS configured** on backend
4. ✅ **Network request succeeds** (see Network tab)
5. ✅ **Response format matches** expected structure

If all these are correct, the widget will display the response. Use the debugging steps above to identify which step is failing.
