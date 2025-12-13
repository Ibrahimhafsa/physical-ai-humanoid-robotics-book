# 🔧 Ask AI Button - Debug & Troubleshooting Guide

## Issue
The Ask AI button is not returning answers / not responding to queries.

## Root Cause Analysis

### Potential Issues

1. **API URL Not Configured** ❌ FIXED
   - Location: `book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx` (line 58)
   - Problem: Hardcoded to `'http://localhost:8000/ask'`
   - Solution: Now reads from `process.env.REACT_APP_API_URL`

2. **Backend Server Not Running** ⚠️ NEEDS CHECK
   - Expected: FastAPI backend on `http://localhost:8000`
   - Status: Not responding to health check
   - Solution: Start backend before using widget

3. **CORS Issues** ⚠️ NEEDS CHECK
   - Frontend: `http://localhost:3002` (Docusaurus)
   - Backend: `http://localhost:8000` (FastAPI)
   - Solution: Backend must allow CORS from frontend origin

4. **Environment Variable Not Loaded** ⚠️ NEEDS CHECK
   - File: `book-docs/.env`
   - Value: `REACT_APP_API_URL=http://localhost:8000/ask`
   - Note: Requires server restart to load `.env` changes

---

## Fix Applied

### Change 1: Environment Variable Support
**File**: `book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx`

**Before**:
```typescript
const apiUrl = 'http://localhost:8000/ask';
```

**After**:
```typescript
const apiUrl =
  typeof window !== 'undefined'
    ? process.env.REACT_APP_API_URL || 'http://localhost:8000/ask'
    : 'http://localhost:8000/ask';
```

**Reason**: Allows dynamic configuration via `.env` file while maintaining fallback.

---

## Checklist to Fix Ask Button

### Step 1: Verify Environment Configuration
```bash
# Check .env file exists
cat book-docs/.env

# Expected output:
# REACT_APP_API_URL=http://localhost:8000/ask
```

### Step 2: Restart Frontend Server
```bash
# Kill any running servers
pkill -f npm
pkill -f node

# Wait 2 seconds
sleep 2

# Start fresh with environment variables
cd book-docs
PORT=3002 npm run start
```

### Step 3: Verify Backend is Running
```bash
# In a new terminal, check if backend is running
curl http://localhost:8000/health

# Expected output:
# {"status":"ok"} or similar
```

### Step 4: Test API Endpoint
```bash
# Test the /ask endpoint directly
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AI?", "top_k": 5, "similarity_threshold": 0.5}'

# Should receive:
# {"answer": "...", "sources": [...], ...}
```

### Step 5: Open Browser and Test
```
1. Visit http://localhost:3002/
2. Navigate to any documentation page
3. Look for chat widget (bottom-right)
4. Type a question: "What is robotics?"
5. Click "Ask" button
6. Wait for response (should appear in 2-10 seconds)
```

---

## Debugging Checklist

### Browser DevTools (F12)

#### Console Tab
```javascript
// Check if API URL is loaded
console.log(process.env.REACT_APP_API_URL)
// Should output: http://localhost:8000/ask

// Check for errors
// Look for any red error messages
// Common errors:
// - "Failed to fetch" = Backend not running
// - "CORS error" = Backend doesn't allow CORS
// - "ERR_EMPTY_RESPONSE" = Backend crashed
```

#### Network Tab
```
1. Open Network tab
2. Click "Ask" button in widget
3. Look for POST request to "http://localhost:8000/ask"
4. Check response:
   - Green (200): Success - check response body
   - Red (404/500): Backend error
   - No request: Frontend not sending
```

#### Application Tab
```
1. Go to Storage → Cookies
2. Check if any CORS-related cookies
3. Go to Local Storage
4. Look for any widget configuration
```

---

## Error Messages & Solutions

### Error: "Unable to reach server. Please check your connection."
```
Cause: Backend not running or unreachable
Solution:
1. Check backend process: ps aux | grep python
2. Start backend: python -m uvicorn src.api:app --reload
3. Verify: curl http://localhost:8000/health
```

### Error: "CORS error: Access-Control-Allow-Origin"
```
Cause: Backend doesn't allow requests from Docusaurus domain
Solution:
1. Check backend CORS config
2. Add frontend origin to CORS allowed list
3. Restart backend
4. Test again
```

### Error: "Service temporarily unavailable (503)"
```
Cause: Backend overloaded or Qdrant not responding
Solution:
1. Check backend logs for errors
2. Verify Qdrant is running: curl http://localhost:6333/health
3. Restart both backend and Qdrant
```

### Error: "Request took too long (timeout)"
```
Cause: Backend processing took >30 seconds
Solution:
1. Check backend performance
2. Optimize Qdrant query
3. Check if similarity_threshold is too low (more results)
4. Increase REQUEST_TIMEOUT in apiClient.ts if needed
```

### Error: "Please enter a valid question"
```
Cause: Query validation failed
Solution:
1. Check query is not empty
2. Check query is <1000 characters
3. Check selected text is <5000 characters
4. Try simpler question
```

---

## Quick Test Script

Create `test-api.sh`:

```bash
#!/bin/bash

# Test API endpoint
echo "Testing backend health..."
curl -s http://localhost:8000/health

echo -e "\n\nTesting /ask endpoint..."
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "top_k": 5,
    "similarity_threshold": 0.5
  }' \
  | python -m json.tool

echo -e "\n\nDone!"
```

Run with:
```bash
bash test-api.sh
```

---

## Configuration Files

### .env (Frontend)
```
REACT_APP_API_URL=http://localhost:8000/ask
```

**Location**: `book-docs/.env`

**Notes**:
- Must be in `book-docs` directory (not root)
- Requires server restart to load changes
- Used only in development
- For production, set via CI/CD or Docker

### FastAPI Backend
```python
# Should have CORS enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Request/Response Flow

### 1. Frontend Sends Request
```
User clicks "Ask" button
↓
QueryInput validates query
↓
RAGChatWidget.handleSubmitQuery() called
↓
fetchQuery() in apiClient.ts
↓
POST http://localhost:8000/ask
```

### 2. Backend Processes
```
FastAPI receives request
↓
Validates QueryRequest schema
↓
Queries Qdrant for similar documents
↓
Passes to RAG agent
↓
Returns ChatResponse with answer + sources
```

### 3. Frontend Displays Response
```
fetchQuery() receives response
↓
parseJSON() extracts answer + sources
↓
RAGChatWidget.handleSubmitQuery() updates state
↓
ResponseDisplay renders answer
↓
SourceList renders sources
```

---

## Performance Considerations

### Expected Timing
- **Request send**: <100ms
- **Backend processing**: 2-10 seconds (depends on Qdrant)
- **Response render**: <500ms
- **Total**: 2-11 seconds

### If Slow
1. Check Qdrant performance
2. Increase similarity_threshold (fewer results to process)
3. Reduce top_k (currently 5, could lower to 3)
4. Check backend logs for bottlenecks

---

## Next Steps

1. ✅ Fixed environment variable reading
2. ⏳ Restart Docusaurus dev server
3. ⏳ Verify backend is running
4. ⏳ Test API endpoint directly
5. ⏳ Open browser and test widget
6. ⏳ Check browser console for errors

---

## Files Modified

**Only frontend changes (no backend changes)**:
- `book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx` (line 58-61)

**No changes to**:
- FastAPI backend
- Qdrant database
- RAG logic
- API contracts
- Request/response schemas

