# 🚀 Quick Start - Both Services

## Two Terminal Windows

### Terminal 1: Backend
```bash
cd F:\humanoid-robotics\ai-physical-robotics-book
python start_backend.py
```

Wait for: `INFO: Application startup complete`

### Terminal 2: Frontend
```bash
cd F:\humanoid-robotics\ai-physical-robotics-book\book-docs
npm run start
```

Wait for: `[SUCCESS] Docusaurus website is running at: http://localhost:3000/`

---

## Access in Browser

- **Book**: http://localhost:3000/
- **Ask Button**: Bottom-right corner
- **Backend Health**: http://localhost:8000/health

---

## Test Ask Feature

1. Click "💬 Ask" button
2. Type: "What is physical AI?"
3. Click "Ask"
4. Wait 1-3 seconds for response with sources

---

## Status

| Service | Port | Status |
|---------|------|--------|
| Frontend | 3000 | ✅ Running |
| Backend | 8000 | ✅ Running |
| Integration | - | ✅ Working |

---

Done! Both services are ready to use.
