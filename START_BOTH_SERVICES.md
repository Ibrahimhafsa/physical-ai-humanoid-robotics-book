# Start Both Services - Complete Guide

## Quick Start (2 Terminal Windows)

### Terminal 1: Start Backend (FastAPI)
```bash
cd backend
python -m uvicorn src.api:app --reload --port 8000 --host 0.0.0.0
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start Frontend (Docusaurus)
```bash
cd book-docs
npm run start
```

**Expected Output:**
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

---

## Verification Checklist

Once both services are running:

- [ ] Backend: Open http://localhost:8000/health in browser → Should show status OK
- [ ] Frontend: Open http://localhost:3000 in browser → Should show book website
- [ ] Ask Button: Look for "💬 Ask" button in bottom-right corner
- [ ] Widget Ready: Click the Ask button and type a question

---

## Full Step-by-Step Instructions

### Step 1: Start Backend Service

Open your first terminal window and run:

```bash
# Navigate to backend directory
cd F:\humanoid-robotics\ai-physical-robotics-book\backend

# Start FastAPI development server
python -m uvicorn src.api:app --reload --port 8000 --host 0.0.0.0
```

**What this does:**
- `python -m uvicorn` - Starts Uvicorn ASGI server
- `src.api:app` - Loads the FastAPI application from src/api.py
- `--reload` - Auto-reloads on code changes (development mode)
- `--port 8000` - Runs on port 8000
- `--host 0.0.0.0` - Makes it accessible from any IP

**Wait for message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Start Frontend Service

Open a second terminal window and run:

```bash
# Navigate to frontend directory
cd F:\humanoid-robotics\ai-physical-robotics-book\book-docs

# Start Docusaurus development server
npm run start
```

**What this does:**
- `npm run start` - Runs the start script in package.json
- Starts Docusaurus development server on port 3000
- Enables hot module reload for changes

**Wait for message:**
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

### Step 3: Access Both Services

Open your web browser and visit:

1. **Frontend (Book Website)**: http://localhost:3000/
   - You should see the Docusaurus book with chapters
   - Look for "💬 Ask" button in bottom-right corner

2. **Backend Health Check**: http://localhost:8000/health
   - Should return JSON status response

### Step 4: Test the Ask Button

1. Go to http://localhost:3000/
2. Click the "💬 Ask" button (bottom-right corner)
3. Type a question: "What is physical AI?"
4. Click "Ask" button
5. Wait 1-5 seconds for response
6. Should see answer with sources

---

## Configuration Details

### Backend (FastAPI)
- **Port**: 8000
- **Host**: 0.0.0.0 (accessible from any interface)
- **Endpoint**: POST /ask
- **CORS**: Enabled for all origins (development mode)
- **Environment**: Uses .env file for Cohere API key and Qdrant configuration

### Frontend (Docusaurus)
- **Port**: 3000
- **API URL**: Configured in book-docs/.env → REACT_APP_API_URL=http://localhost:8000/ask
- **Hot Reload**: Enabled
- **Theme**: Auto-detects Docusaurus theme (light/dark)

---

## Troubleshooting

### Backend Won't Start

**Error**: "Address already in use"
```bash
# Solution: Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Error**: "No module named 'backend.src'"
```bash
# Solution: Run from repo root, not from backend/ directory
cd F:\humanoid-robotics\ai-physical-robotics-book
python -m uvicorn backend.src.api:app --reload --port 8000
```

**Error**: "COHERE_API_KEY not set"
```bash
# Solution: Check backend/.env has API keys
cat backend/.env | grep COHERE_API_KEY

# If missing, add it:
echo 'COHERE_API_KEY=your_key_here' >> backend/.env
```

### Frontend Won't Start

**Error**: "Port 3000 already in use"
```bash
# Solution: Kill process on port 3000
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

**Error**: "npm ERR! code ENOENT"
```bash
# Solution: Ensure node_modules are installed
cd book-docs
npm install
npm run start
```

**Error**: "Cannot find module '@docusaurus'"
```bash
# Solution: Reinstall dependencies
cd book-docs
rm -rf node_modules package-lock.json
npm install
npm run start
```

### Connection Issues

**Ask Button Shows "Unable to reach server"**
```
Cause: Backend not running on port 8000
Solution: Verify backend is running:
  curl http://localhost:8000/health
```

**CORS Error in Browser Console**
```
Cause: Frontend can't reach backend
Solution: Ensure CORS is enabled in backend/src/api.py
Check that FastAPI is running with --host 0.0.0.0
```

---

## Monitoring Both Services

### Check Backend Status
```bash
curl -s http://localhost:8000/health | jq .
```

### Check Frontend Status
```bash
curl -s http://localhost:3000 | head -20
```

### View Backend Logs
- Terminal 1 will show all requests and responses
- Look for POST /ask requests

### View Frontend Logs
- Terminal 2 will show webpack compilation and hot reload
- Check browser console (F12) for client-side errors

---

## Development Workflow

### Making Changes

**Frontend (Docusaurus)**
- Edit files in `book-docs/docs/`, `book-docs/src/`
- Changes automatically reload in browser
- No restart needed

**Backend (FastAPI)**
- Edit files in `backend/src/`
- With `--reload` flag, changes automatically restart server
- No manual restart needed

### Testing Changes

1. Make code changes
2. Services auto-reload
3. Test in browser
4. Check terminal logs for errors

---

## Stopping Services

### Stop Backend (Terminal 1)
```
Press Ctrl+C
```

### Stop Frontend (Terminal 2)
```
Press Ctrl+C
```

Both services will cleanly shutdown.

---

## Advanced: Running Both in One Terminal

If you want to run both in a single terminal, use parallel execution:

### Windows (PowerShell)
```powershell
# Start both in background
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd backend && python -m uvicorn src.api:app --reload --port 8000"
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd book-docs && npm run start"
```

### macOS/Linux (Bash)
```bash
# Start backend in background
(cd backend && python -m uvicorn src.api:app --reload --port 8000) &
# Start frontend in foreground
cd book-docs && npm run start
```

---

## Integration Summary

| Service | Port | URL | Command |
|---------|------|-----|---------|
| **Frontend** | 3000 | http://localhost:3000 | `npm run start` (from book-docs/) |
| **Backend** | 8000 | http://localhost:8000 | `python -m uvicorn src.api:app --reload --port 8000` (from backend/) |
| **Health Check** | 8000 | http://localhost:8000/health | GET request |
| **Ask Endpoint** | 8000 | http://localhost:8000/ask | POST request with query |

---

## Next Steps

1. ✅ Open two terminal windows
2. ✅ Follow "Quick Start" section above
3. ✅ Visit http://localhost:3000/ in browser
4. ✅ Test Ask button
5. ✅ Check both services in terminals for logs

Your complete RAG system will be running with:
- ✅ Docusaurus book website
- ✅ Ask AI button (globally integrated)
- ✅ FastAPI backend with RAG pipeline
- ✅ Cohere embeddings + Qdrant retrieval
- ✅ Full request/response flow working

**Everything is ready to go!**
