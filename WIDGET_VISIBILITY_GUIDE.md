# RAG Chat Widget - Visibility & Setup Guide

## ✅ Current Status

- **Dev Server**: ✅ Running on `http://localhost:3000/`
- **Docusaurus Compilation**: ✅ Successful (no errors)
- **TypeScript**: ✅ Zero errors
- **Widget Code**: ✅ Fully implemented and integrated
- **Button Styling**: ✅ Modern purple theme with glow & hover effects

## 🔍 Why the Widget Might Not Be Visible

### Issue 1: Browser Cache (Most Common)
Your browser is caching old content before the widget was fully integrated.

**Solution:**
1. **Hard Refresh**: Press **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (Mac)
2. Open **DevTools** (F12) → **Application** tab
3. Clear **Cookies and Cached Data** for `localhost:3000`
4. Refresh the page

### Issue 2: Backend API Not Running
The widget tries to connect to `http://localhost:8000/ask`, but the FastAPI backend isn't running. The widget will still render, but may show error states when you try to submit a query.

**To start the backend** (if you have Feature 004 set up):
```bash
# From the backend directory
python -m uvicorn src.api:app --reload
```

### Issue 3: Widget Hidden by Other Elements
The widget is positioned at `bottom-right` with `z-index: 1000`. It might be hidden behind other page elements.

**Check:**
1. Open **DevTools** (F12) → **Elements** tab
2. Inspect the bottom-right corner of the page
3. Search for `rag-chat-widget` in the DOM

## 🧪 Testing Steps

### Step 1: Verify the Dev Server is Running
```bash
curl http://localhost:3000/
```
Should return HTML content.

### Step 2: Check for JavaScript Errors
1. Open DevTools (F12)
2. Go to **Console** tab
3. Look for red error messages
4. If you see `Cannot find module '@site/src/components/RAGChatWidget'`, the layout swizzle isn't working

### Step 3: Inspect the Widget Element
1. Open DevTools → **Elements** tab
2. Press **Ctrl+F** (Cmd+F on Mac)
3. Search for: `rag-chat-widget`
4. If found, the widget is in the DOM but may be hidden

### Step 4: Check CSS Visibility
In DevTools Console, run:
```javascript
const widget = document.querySelector('[data-testid="rag-chat-widget"]');
console.log('Widget found:', widget);
console.log('Widget visible:', window.getComputedStyle(widget).display);
console.log('Widget position:', window.getComputedStyle(widget).position);
```

## 🎨 Widget Appearance

When visible, the widget should appear as:
- **Location**: Bottom-right corner of the page
- **Size**: ~400px wide, adaptive height
- **Button Style**:
  - **Color**: Purple gradient (#7c3aed → #8b5cf6)
  - **Text**: "💬 Ask" (header), "→ Ask" (submit button)
  - **Effects**: Subtle glow, hover animation, shimmer on hover
- **Header**: "💬 Ask" with minimize button

## 📋 Quick Fix Checklist

- [ ] Hard refresh browser (Ctrl+Shift+R)
- [ ] Clear browser cache for localhost:3000
- [ ] Check browser console for errors (F12 → Console)
- [ ] Verify dev server is running and showing no errors
- [ ] Check if widget element exists in DOM (F12 → Elements)
- [ ] Ensure no other page elements are blocking bottom-right corner
- [ ] Start backend API if testing query functionality (`http://localhost:8000/ask`)

## 🚀 Once Widget is Visible

### Test the Button Functionality
1. **Look for the purple "Ask" button** at bottom-right
2. **Click it** to expand the widget
3. **Type a question** like "What is this page about?"
4. **Click "Ask"** to submit
5. If backend is running, you'll see the response. If not, you'll see an error.

### Expected Button Behavior
- **Default State**: Purple gradient button with subtle glow
- **Hover**: Brighter gradient, lifted animation, shimmer effect
- **Loading**: Button shows "⊙ Thinking..." with spinner
- **Mobile**: Button adapts to responsive width (full screen on mobile)

## 💻 File Locations

| File | Purpose |
|------|---------|
| `book-docs/src/components/RAGChatWidget/index.tsx` | Main widget component |
| `book-docs/src/components/RAGChatWidget/QueryInput.tsx` | Input form with "Ask" button |
| `book-docs/src/components/RAGChatWidget/RAGChatWidget.module.css` | All styling (lines 414-566 for button) |
| `book-docs/src/theme/Layout/index.tsx` | Layout swizzle (global injection) |
| `book-docs/src/components/RAGChatLayout/RAGChatLayout.tsx` | Layout wrapper component |

## 🔧 Advanced Troubleshooting

### If widget isn't in DOM at all:
```bash
# 1. Clear Docusaurus cache
cd book-docs
rm -rf .docusaurus

# 2. Restart dev server
npm start
```

### If Layout swizzle isn't working:
1. Check `src/theme/Layout/index.tsx` imports
2. Verify `RAGChatLayout` component exists and exports default
3. Check Docusaurus version in `docusaurus.config.js`

### If CSS isn't loading:
```bash
# In DevTools → Elements → Computed tab
# Check if .widget, .submitButton classes are being applied
```

## ✨ Next Steps

Once the widget is visible and working:
1. Test text selection feature (select text on page)
2. Test on mobile viewport (DevTools mobile emulation)
3. Test dark mode toggle
4. Test error states (turn off backend, try submitting)

---

**Questions?** Check the implementation comments in:
- `src/components/RAGChatWidget/index.tsx` (main logic)
- `src/components/RAGChatWidget/QueryInput.tsx` (button implementation)
- `src/components/RAGChatWidget/RAGChatWidget.module.css` (styling details)
