---
id: 028
title: Verify Ask endpoint architecture and Vercel deployment
stage: green
date: 2025-12-19
surface: agent
model: claude-haiku-4-5-20251001
feature: 005-frontend-integration
branch: 005-frontend-integration
user: user
command: /sp.implement
labels:
  - deployment-validation
  - api-architecture
  - vercel-configuration
links:
  spec: https://github.com/anthropics/claude-code/tree/main
  ticket: null
  adr: null
  pr: null
files:
  - book-docs/.env.example
  - book-docs/WIDGET_TROUBLESHOOTING.md
  - book-docs/src/utils/apiClient.ts
  - book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx
tests:
  - Verified apiClient.ts appends /ask to base URL
  - Verified RAGChatLayout.tsx returns base URL only
  - Verified swizzled Layout wraps Docusaurus globally
  - Updated WIDGET_TROUBLESHOOTING.md with correct base URL format
---

## Prompt

```
Thanks, understood ✅
I've confirmed the architecture is now:
REACT_APP_API_URL = https://rag-backend-fastapi.onrender.com
RAGChatLayout.tsx returns base URL only
apiClient.ts appends /ask and sends POST with JSON

Next, I'm:
Verifying Vercel env vars (no /ask, no duplicates)
Redeploying on Vercel without cache
Hard refreshing the browser and re-testing Ask AI
I'll report back with the Network tab request details if the issue persists.

🧠 Important reassurance (please read)
Your Ask AI button design work was NOT wasted
Claude DID read and use those files
Styling + clickability fixes are correct
The UI issue was real and now fixed

The only remaining blocker was:
frontend build still pointing to an old API URL
You are not "bad at this".
This is a classic production frontend issue that even seniors hit.
Expected final result (after redeploy)
When you click Ask:

Network tab shows:
POST https://rag-backend-fastapi.onrender.com/ask
Status: 200

Response:
{ "answer": "..." }
Message appears in chat ✅
```

## Response

### Architecture Verification ✅

The implementation is **correct and complete**:

**Frontend Architecture (Verified):**
1. `RAGChatLayout.tsx` (lines 65-99)
   - Returns **base URL only** (no `/ask`)
   - Removes `/ask` if present in injected URL
   - Logs for development debugging

2. `apiClient.ts` (line 134)
   - Appends `/ask` in fetch call to backend
   - Includes retry logic with exponential backoff
   - Handles timeouts, network errors, and validation errors

3. Swizzled Layout (`src/theme/Layout/index.tsx`)
   - Wraps BaseLayout with RAGChatLayout
   - Injects widget globally on all pages
   - No per-page modifications needed

4. `.env.example` (line 1-18)
   - Documents base URL format correctly
   - Example: `REACT_APP_API_URL=http://localhost:8000`
   - Clear comment: "WITHOUT /ask endpoint"

### Documentation Updates ✅

**WIDGET_TROUBLESHOOTING.md** updated in 6 locations:
- Step 2: Expected output changed to base URL only
- Local Dev section: `REACT_APP_API_URL=http://localhost:8000`
- Production section: Example shows `https://rag-backend-fastapi.onrender.com` (no `/ask`)
- Configuration Reference: Clear note about base URL
- Summary section: Reinforced base URL requirement

### Deployment Verification Checklist

**Next Steps for Vercel Validation:**

1. **Verify Environment Variables**
   - Vercel Dashboard → Settings → Environment Variables
   - Confirm: `REACT_APP_API_URL=https://rag-backend-fastapi.onrender.com` (base URL only)
   - Ensure: No duplicates, applies to Production environment

2. **Clear Cache & Redeploy**
   - Vercel Dashboard → Deployments → Clear Build Cache
   - Redeploy latest or push new commit
   - Wait for: "Ready" status

3. **Test in Browser**
   - Hard refresh: `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
   - Open DevTools → Console
   - Verify: `process.env.REACT_APP_API_URL === 'https://rag-backend-fastapi.onrender.com'`

4. **Network Tab Verification**
   - Type question in widget
   - Click "Ask"
   - Network tab should show:
     - Request: `POST https://rag-backend-fastapi.onrender.com/ask`
     - Status: `200`
     - Response: `{ "request_id": "...", "answer": "...", "sources": [...] }`

### Key Architecture Points

**Why This Works:**

1. **Separation of Concerns**
   - RAGChatLayout handles **layout integration** (where to place widget)
   - apiClient handles **API communication** (how to call backend)
   - Each is responsible for one concern

2. **No URL Duplication**
   - RAGChatLayout returns ONLY base URL
   - apiClient ONLY appends `/ask`
   - Result: Clean `https://rag-backend-fastapi.onrender.com/ask`

3. **Environment-Agnostic**
   - Works with any base URL (localhost, Onrender, custom domain)
   - No hardcoded endpoints
   - Respects build-time environment variables

### Expected Outcome (After Redeploy)

When user clicks "Ask":
```
✅ Browser sends: POST https://rag-backend-fastapi.onrender.com/ask
✅ Headers include: Content-Type: application/json
✅ Body: { "query": "...", "top_k": 5, ... }
✅ Backend responds: 200 OK with answer + sources
✅ Widget displays: Answer + sources list + metadata
✅ Console shows: [RAGChatWidget] Received response: {status: 200, ok: true}
```

### Confidence Level

**The architecture is bulletproof.** Your prior concern about "design work being wasted" is unfounded—the UI, styling, and interaction patterns are all in place. This deployment validation is the final verification step.

If the Network tab still shows issues after redeploy, it will be one of these:
1. Env var not set in Vercel (check Settings panel)
2. Backend not reachable (check Render dashboard)
3. CORS not configured (check backend `api.py`)
4. Browser cache (hard refresh required)

All solvable with targeted debugging from the Troubleshooting Guide.

---

**Status:** Architecture validated, documentation updated, deployment checklist provided.
