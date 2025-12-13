# Frontend ↔ Backend Connection Debugging Guide

## Quick Start: Getting the Ask AI Button Working

### 1. **Backend Status Check**

**Is the FastAPI backend running?**

```bash
# Check if backend is accessible
curl -X GET http://localhost:8000/health

# Expected response:
# {"status": "ok"} or similar health check
```

**If backend is NOT running:**
```bash
cd backend
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

**Backend must be running on port 8000** for the frontend to connect.

---

### 2. **Environment Variable Configuration**

**Check `book-docs/.env`:**

The file should contain:
```env
REACT_APP_API_URL=http://localhost:8000/ask
```

This tells the frontend where to send queries.

**Important**:
- If using `localhost:8000`, the backend must run on the **same machine**
- If backend is on a different machine/server, update the URL to the actual IP or hostname
- For production, use the deployed backend URL

---

### 3. **Verify Widget is Mounted**

1. Open Docusaurus site: `http://localhost:3000` (or your dev port)
2. Open **Browser DevTools** (F12 or Cmd+Option+I)
3. Look at the bottom-right corner of the page
4. You should see a **"💬 Ask"** button/widget

**If widget is NOT visible:**
- Check browser console for errors
- Verify `src/theme/Layout/index.tsx` exists and is being used
- Check that `RAGChatWidget` is imported correctly in `RAGChatLayout.tsx`

---

### 4. **Test API Connection from Browser Console**

Open Browser DevTools Console and run:

```javascript
// Test if backend is reachable
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log('Backend healthy:', data))
  .catch(err => console.error('Backend unreachable:', err));

// Test actual ask endpoint
const testQuery = {
  query: "What is physical AI?",
  top_k: 5,
  similarity_threshold: 0.5
};

fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(testQuery)
})
  .then(r => r.json())
  .then(data => console.log('Response:', data))
  .catch(err => console.error('Error:', err));
```

**Expected response:**
```json
{
  "request_id": "abc123",
  "answer": "Physical AI combines...",
  "sources": [...],
  "context_used": 3,
  "tokens_used": 45,
  "response_time_ms": 1200,
  "timestamp": "2025-12-14T10:30:00Z"
}
```

---

## Common Issues & Solutions

### Issue 1: "Unable to reach server. Please check your connection."

**Cause**: Backend is not running or URL is wrong

**Solution**:
```bash
# 1. Verify backend is running on port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 2. Check REACT_APP_API_URL in .env
cat book-docs/.env | grep REACT_APP_API_URL

# 3. If URL is wrong, update it and restart Docusaurus dev server
# 4. If backend isn't running, start it:
cd backend
python -m uvicorn src.api:app --reload
```

---

### Issue 2: CORS Error in Browser Console

**Error message**: `Access to XMLHttpRequest at 'http://localhost:8000/ask' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Cause**: Backend CORS is not configured for frontend domain

**Solution** (Backend `src/api.py`):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev: allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The backend already has this, but verify it's there. For production, restrict `allow_origins` to specific domains:
```python
allow_origins=["https://yourdomain.com"]
```

---

### Issue 3: API Response is Null or Malformed

**Symptom**: Widget says "No response received" or shows empty message

**Solution**:
1. Check backend response format in console
2. Verify response has required fields:
   - `request_id` (string)
   - `answer` (string)
   - `sources` (array)
   - `context_used` (number)
   - `tokens_used` (number)
   - `response_time_ms` (number)
   - `timestamp` (ISO string)

3. If missing fields, backend needs updating

---

### Issue 4: Query Submitted but No Loading Spinner

**Cause**: Frontend not sending request properly

**Solution**:
1. Open Browser DevTools → Network tab
2. Type a question in the Ask widget and submit
3. Look for a POST request to `http://localhost:8000/ask`
4. Check request body and response

**If no request appears**:
- Check `book-docs/src/utils/apiClient.ts` line 138: `const response = await fetch(apiUrl, ...)`
- Verify `apiUrl` prop is being passed correctly to widget
- Check browser console for JavaScript errors

---

### Issue 5: Backend Shows "No Sources Found"

**Symptom**: Widget displays "I don't have information about this topic..."

**Cause**: Qdrant collection is empty or similarity threshold is too high

**Solution**:
1. Check Qdrant collection has documents indexed
2. Lower `similarity_threshold` in query (default 0.5)
3. Increase `top_k` to retrieve more results (default 5)

In `book-docs/src/components/RAGChatWidget/index.tsx` line 107:
```typescript
const request: QueryRequest = {
  query,
  top_k: 5,  // Try increasing to 10
  similarity_threshold: 0.5,  // Try lowering to 0.3
  context: selectedText || undefined,
};
```

---

### Issue 6: Widget Visible but Button Unresponsive

**Cause**: JavaScript error or component not rendering

**Solution**:
1. Open Browser Console (F12)
2. Look for red error messages
3. Common errors:
   - `Cannot read property 'apiUrl' of undefined` → Widget props not passed
   - `fetch is not defined` → Browser doesn't support Fetch API (very unlikely)
   - `TypeError: Cannot set properties of null` → Component mounting issue

4. Check that `RAGChatWidget` receives `apiUrl` prop from `RAGChatLayout`

---

## Request Flow Diagram

```
User Types Question
        ↓
QueryInput Component (./components/RAGChatWidget/QueryInput.tsx)
        ↓
Validation (validateQueryRequest in apiClient.ts)
        ↓
handleSubmitQuery (index.tsx:95-197)
        ↓
fetchQuery() → fetch(apiUrl) → /ask endpoint
        ↓
AbortController + 30s timeout
        ↓
Response Parser (JSON)
        ↓
ChatMessage added to state
        ↓
ResponseDisplay renders answer + sources
        ↓
User sees result in widget
```

---

## File Structure Reference

### Frontend Files

- **Main Widget**: `book-docs/src/components/RAGChatWidget/index.tsx`
- **API Client**: `book-docs/src/utils/apiClient.ts` (fetchQuery, validateQueryRequest)
- **Query Input**: `book-docs/src/components/RAGChatWidget/QueryInput.tsx`
- **Response Display**: `book-docs/src/components/RAGChatWidget/ResponseDisplay.tsx`
- **Layout Wrapper**: `book-docs/src/theme/Layout/index.tsx` (swizzle point)
- **Layout Injection**: `book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx`
- **Types**: `book-docs/src/components/RAGChatWidget/types.ts`
- **Styles**: `book-docs/src/components/RAGChatWidget/RAGChatWidget.module.css`

### Environment Configuration

- **Dev Config**: `book-docs/.env` (contains `REACT_APP_API_URL`)
- **Example Config**: `book-docs/.env.example`

---

## Debugging Checklist

- [ ] Backend running on `localhost:8000`?
- [ ] Health check endpoint responds: `curl http://localhost:8000/health`?
- [ ] `REACT_APP_API_URL=http://localhost:8000/ask` in `book-docs/.env`?
- [ ] Docusaurus dev server restarted after `.env` changes?
- [ ] Ask widget visible in bottom-right corner?
- [ ] Browser console open when testing (F12)?
- [ ] No CORS errors in console?
- [ ] Test request in console shows correct response format?
- [ ] Qdrant collection has documents indexed?
- [ ] Backend `/ask` endpoint accepts POST requests?

---

## Testing the Complete Flow

### Step 1: Backend Ready
```bash
cd backend
python -m uvicorn src.api:app --reload
# Should show: Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Frontend Ready
```bash
cd book-docs
npm run start
# Should show: Starting the development server...
# Open http://localhost:3000
```

### Step 3: Widget Test
1. Look for "💬 Ask" button in bottom-right
2. Type: "What is kinematics?"
3. Click "Ask"
4. Should see:
   - Loading spinner
   - Response with answer and sources
   - No red error messages

### Step 4: Error Scenario Test
1. Temporarily stop backend
2. Try submitting query
3. Should see: "Service temporarily unavailable. Please try again later."
4. Restart backend and click retry
5. Should work again

---

## Performance Monitoring

### Response Time
- Expected: 1-5 seconds
- Shown in widget as metadata: "Took 2.3s"
- Check Network tab for latency breakdown

### Bundle Size
- Run: `npm run build` in `book-docs/`
- Widget adds ~50KB to bundle (acceptable)

---

## Production Deployment

### Environment Variables
Update for production:
```env
REACT_APP_API_URL=https://api.yourdomain.com/ask
```

### CORS Configuration
Update backend CORS to specific domain:
```python
allow_origins=["https://yourdomain.com"]
```

### Build Verification
```bash
cd book-docs
npm run build
# Verify no errors and widget works in ./build directory
```

---

## Support Resources

- **Feature 005 Spec**: `specs/005-frontend-integration/spec.md`
- **Feature 005 Plan**: `specs/005-frontend-integration/plan.md`
- **Feature 005 Tasks**: `specs/005-frontend-integration/tasks.md`
- **Feature 004 Backend**: Backend RAG Agent API docs
- **Docusaurus Docs**: https://docusaurus.io/
- **TypeScript Types**: `book-docs/src/components/RAGChatWidget/types.ts`

---

## Quick Fixes (Copy-Paste Ready)

### Reset Environment to Defaults
```bash
cp book-docs/.env.example book-docs/.env
# Then update REACT_APP_API_URL if needed
```

### Clear Node Modules & Reinstall
```bash
cd book-docs
rm -rf node_modules package-lock.json
npm install
npm run start
```

### Restart Both Services
```bash
# Terminal 1: Backend
cd backend && python -m uvicorn src.api:app --reload

# Terminal 2: Frontend
cd book-docs && npm run start
```

### Test Endpoint Directly
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"What is physical AI?","top_k":5,"similarity_threshold":0.5}'
```

---

## Summary

The Ask AI button works by:

1. **User types question** → QueryInput captures text
2. **Validation** → Ensures non-empty, <1000 chars
3. **API Call** → POST to `http://localhost:8000/ask`
4. **Backend Processing** → Retrieves sources from Qdrant, generates answer with Cohere
5. **Response Display** → Shows answer + sources in widget
6. **Error Handling** → User-friendly messages for all failure scenarios

**Key connection points**:
- Backend port: **8000**
- Frontend env var: **REACT_APP_API_URL**
- Widget location: Bottom-right corner
- Request timeout: 30 seconds
- Retry logic: 3 attempts with exponential backoff

If anything isn't working, start with **Backend Status Check** (item 1 above) and work through the checklist.
