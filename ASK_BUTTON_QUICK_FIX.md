# Ask AI Button - Quick Fix Checklist

## ⚡ 30-Second Diagnosis

Run these commands to check if everything is set up correctly:

```bash
# 1. Is backend running?
curl -s http://localhost:8000/health

# 2. Check environment variable
cat book-docs/.env | grep REACT_APP_API_URL

# 3. Is Docusaurus running?
# (Should be on http://localhost:3000)
```

---

## 🔴 If Button is NOT Visible

### Fix 1: Restart Docusaurus Dev Server
```bash
cd book-docs
npm run start
```

Wait 30 seconds for it to compile. Button should appear in **bottom-right corner**.

### Fix 2: Check Browser Cache
- Open DevTools (F12)
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

### Fix 3: Verify Layout Swizzle
Check that `book-docs/src/theme/Layout/index.tsx` exists and contains:
```typescript
import Layout from '@theme-original/Layout';
import RAGChatLayout from '@site/src/components/RAGChatLayout';

export default function LayoutWrapper(props: any): JSX.Element {
  return (
    <RAGChatLayout {...props}>
      <Layout {...props} />
    </RAGChatLayout>
  );
}
```

---

## 🔴 If Button is Visible but NOT Responding

### Fix 1: Start Backend
```bash
cd backend
python -m uvicorn src.api:app --reload --port 8000
```

### Fix 2: Verify Endpoint Configuration
Check `book-docs/.env`:
```env
REACT_APP_API_URL=http://localhost:8000/ask
```

**Important**: Include `/ask` at the end!

### Fix 3: Test Backend Directly
```bash
# In browser console (F12):
fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: "test" })
})
  .then(r => r.json())
  .then(d => console.log('Response:', d))
  .catch(e => console.error('Error:', e));
```

If this works, problem is in widget code.
If this fails, problem is backend/CORS.

### Fix 4: Check Browser Console for Errors
- Open DevTools (F12)
- Click "Console" tab
- Look for red error messages
- Common errors:
  - `Unexpected token` → Response is not JSON
  - `CORS policy` → Backend CORS not configured
  - `Cannot read property` → Widget props missing

---

## 🟡 If Button Shows Error: "Unable to reach server"

**Symptom**: Button visible, typing works, submit shows error "Unable to reach server"

### Fix 1: Verify Backend is Running
```bash
# Check port 8000
lsof -i :8000    # macOS/Linux
netstat -ano | findstr :8000  # Windows

# If not running:
cd backend
python -m uvicorn src.api:app --reload
```

### Fix 2: Verify Backend URL is Correct
In browser console:
```javascript
console.log('API URL:', process.env.REACT_APP_API_URL);
```

Should print: `http://localhost:8000/ask`

### Fix 3: Check CORS Headers
Backend should have CORS enabled. In `backend/src/api.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🟡 If Button Shows Error: "Service temporarily unavailable"

**Symptom**: Backend responds with 503 or timeout

### Fix 1: Check Qdrant is Running
```bash
# Is Qdrant accessible?
curl -s http://localhost:6333/health
```

If Qdrant is not running:
1. Start Qdrant (Docker or local)
2. Verify collection `book_embeddings` exists
3. Verify documents are indexed

### Fix 2: Increase Timeout
In `book-docs/src/utils/apiClient.ts` line 22:
```typescript
const REQUEST_TIMEOUT = 30000; // 30 seconds
```

Can increase to 60000 (60 seconds) if backend is slow.

---

## 🟡 If Button Shows Error: "Please enter a valid question"

**Symptom**: Query was submitted but backend returned 400 error

### Fix 1: Check Query Validation
Query must be:
- Non-empty
- Less than 1000 characters
- Non-whitespace

In `QueryInput.tsx` line 36:
```typescript
if (!query.trim()) {
  return; // Won't submit empty
}
```

### Fix 2: Check Backend Validation
Backend validates the request. Check if query meets requirements.

---

## 🟡 If Sources are Not Showing

**Symptom**: Button works, response appears, but no sources listed

### Fix 1: Check Qdrant Collection
```bash
# Can you reach Qdrant?
curl -s "http://localhost:6333/collections/book_embeddings"
```

Should return collection info.

### Fix 2: Lower Similarity Threshold
In `book-docs/src/components/RAGChatWidget/index.tsx` line 108:
```typescript
const request: QueryRequest = {
  query,
  top_k: 5,
  similarity_threshold: 0.3,  // Lower threshold = more results
  context: selectedText || undefined,
};
```

Try lowering from 0.5 to 0.3.

### Fix 3: Increase top_k
```typescript
top_k: 10,  // Retrieve more sources
```

---

## ✅ Verify Everything Works

Once you've applied fixes, test end-to-end:

1. **Backend Running**
   ```bash
   curl http://localhost:8000/health
   # Should respond: {"status":"ok"} or similar
   ```

2. **Frontend Running**
   ```bash
   # Visit http://localhost:3000
   # Should see "💬 Ask" button bottom-right
   ```

3. **Can Type in Button**
   - Click button
   - Type a question
   - Button should be active (not grayed out)

4. **Can Submit Query**
   - Click "Ask" or press Enter
   - Should see spinner/loading
   - Button disabled during request

5. **Get Response**
   - After 1-5 seconds
   - Should see answer text
   - Should see sources below

6. **Error Handling Works**
   - Stop backend: `Ctrl+C`
   - Try submitting query
   - Should see friendly error: "Service temporarily unavailable"
   - Restart backend and retry should work

---

## 📋 Complete Start-from-Scratch Setup

If nothing works, start fresh:

### Step 1: Backend
```bash
# Terminal 1
cd backend
python -m uvicorn src.api:app --reload --port 8000

# Should show:
# Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Frontend Environment
```bash
# Terminal 2
cd book-docs

# Reset environment file
cp .env.example .env

# Verify content:
cat .env | grep REACT_APP_API_URL
# Should show: REACT_APP_API_URL=http://localhost:8000/ask
```

### Step 3: Frontend Dev Server
```bash
# Terminal 2 (continued)
npm install  # If needed
npm run start

# Should show:
# Docusaurus website is running at http://localhost:3000
```

### Step 4: Test
1. Open `http://localhost:3000` in browser
2. Look for "💬 Ask" button
3. Type "What is physical AI?"
4. Click Ask
5. Should get response in 1-5 seconds

---

## 🔍 Deep Debugging

If basic fixes don't work, check these files:

### 1. Widget Main Component
- **File**: `book-docs/src/components/RAGChatWidget/index.tsx`
- **Check**:
  - Line 138: `const response = await fetchQuery(request, apiUrl);`
  - Line 60: `process.env.REACT_APP_API_URL || 'http://localhost:8000/ask'`

### 2. API Client
- **File**: `book-docs/src/utils/apiClient.ts`
- **Check**:
  - Line 123: `const response = await fetch(apiUrl, ...)`
  - Line 77: Error mapping function
  - Line 242: Request validation

### 3. Layout Integration
- **File**: `book-docs/src/theme/Layout/index.tsx`
- **Check**: Widget is imported and wrapped correctly

### 4. Environment Variable
- **File**: `book-docs/.env`
- **Check**: `REACT_APP_API_URL=http://localhost:8000/ask`

---

## 📞 When to Check Logs

### Browser Console (DevTools F12 → Console)
Look for:
- Red error messages (JavaScript errors)
- Yellow warnings (deprecations)
- Blue info messages

### Backend Console (Terminal running backend)
Look for:
- 500 errors (server errors)
- Connection refused (backend crashed)
- Qdrant connection errors

### Network Tab (DevTools F12 → Network)
Look for:
- POST request to `http://localhost:8000/ask`
- Response status (should be 200)
- Response body (should be valid JSON)

---

## 💡 Pro Tips

1. **Hard refresh frontend after changes**: `Ctrl+Shift+R`
2. **Restart backend after config changes**: `Ctrl+C` then restart
3. **Check both terminals are still running** (backend + frontend)
4. **Use same machine for local testing** (localhost won't work cross-machine)
5. **Test backend directly with cURL before debugging frontend**

---

## ✍️ Report Issues With

If still stuck, provide:
1. Backend status: `curl http://localhost:8000/health`
2. Environment: `cat book-docs/.env | grep REACT_APP`
3. Browser console errors (screenshot or text)
4. Network tab request/response (screenshot)
5. Backend console output (screenshot)

---

## 📚 Related Documentation

- **Full Debugging Guide**: `FRONTEND_BACKEND_DEBUG_GUIDE.md`
- **Feature 005 Specification**: `specs/005-frontend-integration/spec.md`
- **Feature 004 Backend Docs**: Backend README
- **React Component Types**: `book-docs/src/components/RAGChatWidget/types.ts`
