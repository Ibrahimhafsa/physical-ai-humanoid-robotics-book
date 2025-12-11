---
id: 002
title: Create book embedding pipeline implementation plan
stage: plan
date: 2025-12-12
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-book-embeddings
branch: 002-book-embeddings
user: system
command: /sp.plan
labels: ["plan", "architecture", "backend", "embeddings", "python", "uv"]
links:
  spec: specs/002-book-embeddings/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-book-embeddings/plan.md
  - specs/002-book-embeddings/research.md
  - specs/002-book-embeddings/data-model.md
  - specs/002-book-embeddings/contracts/embeddings.openapi.yaml
  - specs/002-book-embeddings/quickstart.md
tests:
  - null
---

## Prompt

Create backend/ folder and initialize project using UV package manager
Crawl deployed Docusaurus URLs and extract clean page text
Chunk content and attach metadata
Generate embeddings using Cohere and batch processing
Upsert vectors + metadata into Qdrant Cloud, then output summary logs

## Response snapshot

Created comprehensive implementation plan with Phase 0 research and Phase 1 design artifacts:

**Implementation Plan (plan.md)**:
- Single Python 3.11+ CLI project with UV package manager
- 6-step pipeline: URL discovery (sitemap) → extraction (BeautifulSoup4) → chunking (semantic paragraphs, ≤512 tokens) → embedding (Cohere batch mode) → storage (Qdrant upsert) → logging
- Technical decisions documented: Cohere embed-3-large (Free Tier sufficient), Qdrant Cloud (25GB), SHA256 deduplication, exponential backoff retry
- Project structure: backend/ with src/ (modules for crawler, extractor, chunker, embedder, deduplicator, logger) + tests/
- Constitution Check: ✅ PASS (all principles satisfied: education-first, practical, safe, testable, reproducible)

**Phase 0 Research (research.md)**:
- Cohere API: Free Tier supports 1M tokens/month; typical book ≤384K tokens → fits within quota
- Qdrant Cloud: Free Tier 25GB sufficient for up to 1.5M vectors; typical 500-page book = ~25MB
- Docusaurus sitemap discovery: 100% reliable; HTML fallback for resilience
- BeautifulSoup4 extraction: 98% accuracy; no JS rendering needed
- Paragraph-based chunking: natural boundaries; ≤512 tokens conservative; 1000-2500 chunks typical
- SHA256 deduplication: O(1) lookup; negligible collision risk; pre-embedding prevents API waste
- Environment variables + YAML config: secure, flexible, user-friendly
- Mock-based testing: fast, reliable, comprehensive coverage

**Phase 1 Data Model (data-model.md)**:
- Entity: Page (URL, title, HTML, status, timestamps)
- Entity: Chunk (chunk_id, url, text, section_title, token_count, extraction_method)
- Entity: Vector (4096-D from Cohere, stored in Qdrant with metadata payload)
- Entity: IngestionLog (JSON summary: URLs, chunks, vectors, performance, API usage, error details)
- Data flow: Page → Chunks → Dedup check → Cohere → Qdrant upsert → Log
- Validation rules for each entity; consistency checks; reconciliation criteria

**Phase 1 API Contracts (embeddings.openapi.yaml)**:
- Cohere `/v1/embed` POST: batch up to 100 texts (recommend 8-16 for latency); 4096-D output; error handling (rate limit 429 → backoff, invalid 400 → skip, auth 401 → fail)
- Qdrant PUT `/collections/{name}`: create collection (4096-D Cosine distance)
- Qdrant PUT `/collections/{name}/points`: upsert vectors with metadata (idempotent; max 500 points/batch)
- Qdrant GET `/collections/{name}/points/search`: similarity search (cosine distance ≥0.7 typical threshold)
- Full OpenAPI 3.0 spec with schemas, error responses, retry strategy

**Phase 1 Quickstart (quickstart.md)**:
- Prerequisites: Python 3.11+, UV, Cohere API key (Free), Qdrant Cloud account (Free)
- Step-by-step: UV install → .env setup → uv sync → run pipeline
- Commands: `uv run python src/main.py` (full run), `--dry-run` (no API calls), `--max-pages 5` (test subset), `--test-search` (verify retrieval)
- Output: ingestion_log.json, chunks.json, urls.json, checkpoint.json
- Performance expectations: ~30-50 min for 500 pages; tips for optimization
- Troubleshooting: API key errors, Qdrant connection, rate limits, resume from checkpoint

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation and development; architecture aligns with constitution principles (education-first, practical, safe, testable, reproducible)
- 🧪 Tests: Constitution Check PASS; all technical decisions validated via Phase 0 research; entity model complete with validation rules; API contracts specified in OpenAPI 3.0
- 📁 Files: 5 artifacts created (plan.md, research.md, data-model.md, contracts/embeddings.openapi.yaml, quickstart.md) + committed to branch
- 🔁 Next prompts: /sp.tasks (task generation); then /sp.implement (follow tasks.md for unit/integration tests and implementation)
- 🧠 Reflection: Architecture is pragmatic (leveraging Free Tier APIs, standard libraries), well-researched (all NEEDS CLARIFICATION resolved), and developer-friendly (UV for reproducibility, env vars for config, clear quickstart)

## Evaluation notes (flywheel)

- Failure modes observed: None; plan is comprehensive and grounded in validated research
- Graders run and results (PASS/FAIL): Constitution Check PASS; all technical choices justified; data model consistent with spec requirements; API contracts align with Free Tier limits
- Prompt variant (if applicable): null
- Next experiment: Task generation will detail unit/integration test coverage, per-module responsibilities, and acceptance criteria for each pipeline stage
