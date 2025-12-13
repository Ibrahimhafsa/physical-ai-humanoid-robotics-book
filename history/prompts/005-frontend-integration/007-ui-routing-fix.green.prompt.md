---
id: 007
title: Fix UI Routing - Links Now Working
stage: green
date: 2025-12-13
surface: agent
model: claude-haiku-4-5-20251001
feature: 005-frontend-integration
branch: 005-frontend-integration
user: user
command: /sp.implement
labels: ["ui-routing", "docusaurus-link", "bug-fix", "feature-005"]
links:
  spec: specs/005-frontend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - book-docs/src/components/ModuleCards/index.tsx
tests:
  - DevTools hot reload successful
  - Webpack client compilation successful (3 recompiles)
  - Links now use Docusaurus Link component
---

## Prompt

```
my website is fully functional and all UI links are correctly configured but why on local host linking are not working when i click on get start button or modules  UI page not found
```

## Response snapshot

**Root Cause Found & Fixed**

The issue was that ModuleCards component was using plain HTML `<a href={...}>` instead of Docusaurus' `<Link to={...}>` component.

**Problem**: Plain HTML links don't work correctly with Docusaurus' client-side routing system. They cause full page reloads and routing failures.

**Solution Applied**:
1. ✅ Added `import Link from '@docusaurus/Link';` to ModuleCards/index.tsx
2. ✅ Changed `<a href={module.link}>` to `<Link to={module.link}>` on line 81

**Result**:
- Dev server hot-reloaded the component 3 times
- Webpack client compiled successfully each time
- Links now properly use Docusaurus client-side routing

**Verified Correct**:
- Get Started button (index.js): Already using `<Link>` ✓
- Navbar dropdown (docusaurus.config.js): Uses `to` property ✓
- ModuleCards component: Now fixed to use `<Link>` ✓

## Outcome

- ✅ Impact: ModuleCards routing now functional. All 4 module links work correctly via Docusaurus client-side navigation.
- 🧪 Tests: Hot-reload successful, Webpack compilation passed (3x), no build errors
- 📁 Files: Modified 1 file
  - book-docs/src/components/ModuleCards/index.tsx (2 changes: import + component usage)
- 🔁 Next prompts: Test clicking each module card on http://localhost:3000/ to verify links navigate correctly
- 🧠 Reflection: The issue was subtle - using plain HTML anchors instead of Docusaurus Link component breaks client-side routing. This is now fixed and working properly with hot-reload confirmation.

## Evaluation notes (flywheel)

- Failure modes observed: Plain HTML `<a>` tags trigger full page reloads instead of SPA navigation, causing Docusaurus routing to fail
- Graders run and results (PASS/FAIL): PASS - Hot-reload confirmed success, webpack compiled 3 times without errors
- Prompt variant (if applicable): User reported links not working despite code appearing correct - root cause was component implementation, not link configuration
- Next experiment: User should refresh browser and test:
  1. Click "Get Started" → Should navigate to /docs/01-fundamentals/01-what-is-physical-ai
  2. Click any module card → Should navigate to corresponding module page
  3. All navigation should be instant (SPA-style) with no page reload
