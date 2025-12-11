# Tasks: Book Embedding Pipeline

**Feature**: 002-book-embeddings | **Date**: 2025-12-12

**Input**: Feature specification and implementation plan from `/specs/002-book-embeddings/`

**Organization**: Tasks grouped by user story priority (P1, P2, P3) to enable independent implementation and testing. Each story is independently testable and deployable.

**Implementation Strategy**: MVP-first approach (User Story 1) with incremental delivery of quality and reproducibility features (Stories 2 & 3).

---

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Parallelizable (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, US3) for traceability
- **Checklist**: All tasks use strict checkbox format `- [ ] T###`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization with UV package manager and basic directory structure

**Duration**: ~30 minutes

### Setup Tasks

- [ ] T001 Create `backend/` directory structure with `src/`, `tests/`, and `examples/` subdirectories
- [ ] T002 Initialize UV project: run `uv init` in `backend/` to create `pyproject.toml` with project metadata (name: "book-embeddings", version: "0.1.0")
- [ ] T003 [P] Add core dependencies to `backend/pyproject.toml`: httpx (HTTP), beautifulsoup4 (HTML parsing), lxml (XML parser), cohere (embeddings), qdrant-client (vector DB), pydantic (validation), python-dotenv (config), pytest (testing)
- [ ] T004 [P] Create `.env.example` in `backend/` with template environment variables: COHERE_API_KEY, COHERE_MODEL, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION, BOOK_ROOT_URL, LOG_LEVEL, OUTPUT_DIR
- [ ] T005 [P] Create `backend/src/config.py` with Pydantic ConfigModel to load and validate environment variables (all required fields, type hints, defaults)
- [ ] T006 [P] Create `backend/src/models.py` with Pydantic data models: Page, Chunk, Vector, IngestionLog (per data-model.md)
- [ ] T007 [P] Create `backend/src/logger.py` with logging setup (INFO level, file + stdout, JSON format for logs)
- [ ] T008 Run `uv sync` to lock dependencies in `backend/uv.lock`
- [ ] T009 Create `backend/.gitignore` to exclude `.env`, `*.pyc`, `__pycache__`, `uv.lock` backup, `embeddings_output/`

**Checkpoint**: Project structure ready; dependencies locked; configuration framework in place

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities that ALL user stories depend on

**Duration**: ~1.5 hours

**⚠️ CRITICAL**: No user story work can begin until this phase completes

### Foundational Tasks

- [ ] T010 [P] Create `backend/src/crawler.py` with `DocosaurusCrawler` class: discover URLs via sitemap.xml parsing and HTML link discovery fallback (methods: `_fetch_sitemap()`, `_parse_sitemap()`, `_discover_urls()`, returns: list of URLs with titles extracted from page `<title>` tags)
- [ ] T011 [P] Create `backend/src/extractor.py` with `TextExtractor` class: extract clean text from HTML (methods: `extract_text(html: str) -> str`, targets: `<article>`, `<main>`, excludes: `<nav>`, `<header>`, `<footer>`, `<script>`, `<style>`)
- [ ] T012 [P] Create `backend/src/chunker.py` with `TextChunker` class: split text into semantic chunks (methods: `chunk_text(text: str, url: str) -> List[Chunk]`, paragraph-based, max 512 tokens, preserves headers as chunk context, validates no empty chunks)
- [ ] T013 [P] Create `backend/src/deduplicator.py` with `Deduplicator` class: detect duplicates via SHA256 content hash (methods: `compute_hash(text: str) -> str`, `is_duplicate(chunk_id: str) -> bool`, stores seen hashes in memory or local JSON)
- [ ] T014 [P] Create `backend/src/retry_policy.py` with exponential backoff retry logic: `retry_with_backoff()` function for transient failures (max 3 retries, 1s initial delay, 2.0 multiplier, capped at 60s)
- [ ] T015 Create `backend/src/checkpoint.py` with checkpoint persistence: `CheckpointManager` class to save/load progress (methods: `save_checkpoint()`, `load_checkpoint()`, stores processed URLs and chunk IDs in JSON)

**Checkpoint**: All foundational utilities ready; user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Embedded Book for RAG Chatbot (Priority: P1) 🎯 MVP

**Goal**: Build complete end-to-end pipeline that crawls a Docusaurus book, extracts text, generates embeddings via Cohere, and stores vectors in Qdrant Cloud

**Independent Test**: Run `uv run python src/main.py` with environment variables configured (pointing to test book); verify:
- All pages crawled and listed in output
- Chunks created with valid text
- Vectors generated (4096-D)
- Vectors stored in Qdrant with metadata
- Ingestion log generated with summary stats

**Value Delivered**: MVP pipeline ready for RAG chatbot integration; complete end-to-end workflow validated

### Implementation for User Story 1

- [ ] T016 [P] Create `backend/src/embedder.py` with `CohereEmbedder` class: call Cohere embed endpoint (methods: `embed_batch(texts: List[str], batch_size: 8)`, handles rate limiting with `retry_policy.py`, returns: list of 4096-D vectors with timestamps)
- [ ] T017 [P] Create `backend/src/storage.py` with `QdrantStorage` class: upsert vectors to Qdrant Cloud (methods: `create_collection_if_needed()`, `upsert_vectors(vectors: List[Vector])`, uses Qdrant client SDK, validates vector dimension before upsert, stores metadata payload with each point)
- [ ] T018 Create `backend/src/pipeline.py` with `EmbeddingPipeline` orchestrator class (methods: `run()` - main entry point, coordinates all modules in order: crawl → extract → chunk → deduplicate → embed → store, handles errors gracefully, logs progress)
- [ ] T019 Create `backend/src/main.py` CLI entry point (parses arguments: `--dry-run`, `--max-pages`, `--test-search`, `--resume`, loads config from `.env`, instantiates `EmbeddingPipeline`, runs and reports summary)
- [ ] T020 Create `backend/src/log_generator.py` with `IngestionLogGenerator` class: generate final JSON log (per data-model.md) with summary stats (URLs discovered, chunks created, vectors stored, API usage, error details, per-page statistics)
- [ ] T021 Create `backend/examples/run_embedding_pipeline.sh`: shell script to load `.env` and run pipeline with standard configuration
- [ ] T022 Update `backend/README.md` or `../quickstart.md` section with example usage for User Story 1

**Implementation Notes**:
- All modules work with Pydantic models (Page, Chunk, Vector) from T006
- Configuration from T005 (config.py)
- Logging from T007 (logger.py)
- Retry logic from T014 (retry_policy.py)
- Checkpoint from T015 (checkpoint.py)
- URL discovery via T010 (crawler.py)
- Text extraction via T011 (extractor.py)
- Chunking via T012 (chunker.py)
- Deduplication via T013 (deduplicator.py)

**Checkpoint**: User Story 1 fully functional - pipeline can crawl, extract, embed, store, and log; MVP ready for testing

---

## Phase 4: User Story 2 - Verify Data Quality & Prevent Duplicates (Priority: P2)

**Goal**: Ensure pipeline output is trustworthy through comprehensive logging, deduplication validation, and data quality checks

**Independent Test**: Run pipeline on sample book with duplicate content (e.g., home page appears in multiple URLs); verify:
- Ingestion log shows all URLs processed
- Deduplication log shows duplicates skipped
- Empty/whitespace chunks excluded from embedding
- Log total vectors match Qdrant collection count (±0.1% variance)
- Timestamps accurate and chronological

**Value Delivered**: Full visibility into pipeline execution; confidence in data quality and deduplication accuracy

### Implementation for User Story 2

- [ ] T023 [P] Enhance `backend/src/extractor.py` to log extraction failures per page: add method `extract_text_with_fallback()` that tries semantic extraction, falls back to raw HTML, logs method used and any errors
- [ ] T024 [P] Enhance `backend/src/chunker.py` to exclude empty chunks: filter chunks with empty/whitespace-only text, log count of excluded chunks
- [ ] T025 [P] Enhance `backend/src/deduplicator.py` to generate deduplication report: add method `get_dedup_report()` returning stats (total chunks processed, duplicates found, dedup rate)
- [ ] T026 Create `backend/src/reconciler.py` with `DataReconciler` class: validate log consistency (methods: `reconcile(log: IngestionLog, qdrant_collection) -> ReconciliationResult`, checks: URLs fetched = discovered - failed, chunks_embedded + chunks_dedup ≤ chunks_created, vectors_stored = chunks_embedded, API calls ≤ ceil(chunks_embedded/8))
- [ ] T027 Enhance `backend/src/log_generator.py` to include detailed per-page statistics: add methods to generate per-page logs (URL, title, chunks created, chunks embedded, extraction method, errors, timings)
- [ ] T028 Enhance `backend/src/pipeline.py` to call `reconciler.py` after pipeline completes: add validation step before writing final log, log reconciliation result (PASS/FAIL with details)
- [ ] T029 Create `backend/tests/integration/test_deduplication.py`: integration test that runs pipeline on sample book with duplicates, verifies dedup rate ≥99%
- [ ] T030 Create `backend/tests/integration/test_log_accuracy.py`: integration test that compares ingestion log totals against Qdrant collection count (variance ±0.1% acceptable)

**Checkpoint**: User Stories 1 + 2 complete - pipeline produces trustworthy, validated output with full deduplication and data quality assurance

---

## Phase 5: User Story 3 - Reproduce Embeddings Locally (Priority: P3)

**Goal**: Enable developers to re-run the pipeline reproducibly with full idempotency support, configuration flexibility, and checkpoint-based resumption

**Independent Test**: Run pipeline, simulate interruption (kill process), resume with `--resume` flag; verify:
- Resume checkpoint loads successfully
- Pipeline skips already-processed URLs (via checkpoint)
- New/updated URLs are re-processed
- Final vector count includes both original and new vectors
- Pipeline completes without duplicate ingestion errors

**Value Delivered**: Full reproducibility and resilience; pipeline can be interrupted and resumed; ready for CI/CD integration

### Implementation for User Story 3

- [ ] T031 [P] Enhance `backend/src/config.py` to support YAML config file: add method `load_from_yaml(path: str)` to read `config.yaml` and merge with environment variables (env vars take precedence)
- [ ] T032 [P] Create `backend/config.example.yaml` template: book_root_url, cohere_model, qdrant_collection, batch_size, max_pages, log_level (example for advanced users)
- [ ] T033 Enhance `backend/src/checkpoint.py` to implement full idempotency: add methods `mark_url_processed(url)`, `get_processed_urls()`, `mark_chunks_embedded(chunk_ids)`, queries Qdrant to detect already-stored vectors to avoid re-ingestion
- [ ] T034 Enhance `backend/src/pipeline.py` to support `--resume` mode: modify `run()` method to load checkpoint, skip processed URLs, skip deduplicated chunks already in Qdrant, continue from last unprocessed URL
- [ ] T035 Enhance `backend/src/main.py` to support config file mode: add `--config` argument to load `config.yaml`, merge with `.env` variables
- [ ] T036 Create `backend/tests/integration/test_idempotency.py`: integration test that runs pipeline, saves checkpoint, resumes pipeline, verifies no duplicate vector ingestion
- [ ] T037 Create `backend/tests/integration/test_config_file.py`: integration test that runs pipeline with `config.yaml` file, verifies configuration values loaded correctly
- [ ] T038 Create `backend/tests/integration/test_dry_run.py`: integration test with `--dry-run` flag, verifies URL discovery and extraction without API calls
- [ ] T039 Update `backend/README.md` or `../quickstart.md` with examples: show `--resume`, `--config config.yaml`, `--dry-run` usage patterns

**Checkpoint**: User Stories 1 + 2 + 3 complete - fully reproducible, resilient, configurable pipeline ready for production use

---

## Phase 6: Testing & Validation

**Purpose**: Comprehensive test coverage for all components and integration scenarios

**Duration**: ~2 hours

### Unit Tests

- [ ] T040 [P] Create `backend/tests/unit/test_crawler.py`: unit tests for `DocosaurusCrawler` (mock HTTP responses, sitemap parsing, URL extraction)
- [ ] T041 [P] Create `backend/tests/unit/test_extractor.py`: unit tests for `TextExtractor` (various HTML structures, boilerplate exclusion, edge cases)
- [ ] T042 [P] Create `backend/tests/unit/test_chunker.py`: unit tests for `TextChunker` (paragraph boundaries, token counting, metadata assignment, empty chunk filtering)
- [ ] T043 [P] Create `backend/tests/unit/test_deduplicator.py`: unit tests for `Deduplicator` (SHA256 hashing, duplicate detection, collision tests)
- [ ] T044 [P] Create `backend/tests/unit/test_config.py`: unit tests for config loading (environment variables, YAML file, merging, validation)
- [ ] T045 [P] Create `backend/tests/unit/test_models.py`: unit tests for Pydantic models (validation, serialization, field requirements)

### Contract Tests (API Contracts)

- [ ] T046 [P] Create `backend/tests/contract/test_cohere_embed.py`: contract tests for Cohere embed endpoint (mock responses, dimension validation, batch processing, rate limit handling)
- [ ] T047 [P] Create `backend/tests/contract/test_qdrant_upsert.py`: contract tests for Qdrant upsert (mock responses, idempotency, metadata validation)

### Integration Tests

- [ ] T048 Create `backend/tests/integration/test_end_to_end.py`: end-to-end test with sample book (small HTML pages), mocked Cohere and Qdrant, verifies complete pipeline flow
- [ ] T049 Create `backend/tests/integration/test_error_handling.py`: tests for error scenarios (crawl failure, extraction failure, rate limit, Qdrant connection error, graceful recovery)
- [ ] T050 Create `backend/tests/fixtures/mock_pages.py`: fixture HTML pages representing various Docusaurus layouts for testing
- [ ] T051 Create `backend/tests/fixtures/mock_cohere.py`: mock Cohere client returning deterministic embeddings for tests
- [ ] T052 Create `backend/tests/fixtures/mock_qdrant.py`: mock Qdrant client tracking upserted points and metadata

**Checkpoint**: Comprehensive test coverage; all components validated; ready for production

---

## Phase 7: Performance & Documentation

**Purpose**: Performance validation, optimization, and user documentation

**Duration**: ~1 hour

### Performance Validation

- [ ] T053 Create `backend/tests/performance/benchmark_crawler.py`: benchmark crawling speed for 50-page sample (target: ≤1 sec/page)
- [ ] T054 Create `backend/tests/performance/benchmark_extractor.py`: benchmark extraction speed (target: ≤1 sec/page)
- [ ] T055 Create `backend/tests/performance/benchmark_embedding.py`: benchmark embedding generation with batching (target: ≤2 sec/chunk including API latency)

### Documentation

- [ ] T056 Create `backend/README.md` with: feature overview, setup instructions (UV, .env, uv sync), usage examples (basic, --dry-run, --resume, --config), troubleshooting
- [ ] T057 [P] Ensure `../quickstart.md` is up-to-date with all CLI options and examples from main.py
- [ ] T058 [P] Create `backend/ARCHITECTURE.md` with: data flow diagram, module responsibilities, class interfaces, configuration schema
- [ ] T059 [P] Create `backend/API_REFERENCE.md` documenting: CohereEmbedder, QdrantStorage, EmbeddingPipeline public methods and error handling
- [ ] T060 Create `backend/examples/sample_config.yaml` with annotated configuration options
- [ ] T061 Create `backend/tests/README.md` documenting test structure, how to run tests, mocking strategy

**Checkpoint**: Fully documented, benchmarked, production-ready codebase

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and best practices

**Duration**: ~1 hour

### Quality & Hardening

- [ ] T062 [P] Add type hints to all functions in core modules (src/*.py) - use mypy for validation
- [ ] T063 [P] Add docstrings to all public classes and methods (Google-style docstring format)
- [ ] T064 [P] Run `pylint` or `flake8` to lint all code; fix style issues
- [ ] T065 [P] Add security checks: ensure API keys never logged, HTTPS-only for API calls, no sensitive data in error messages
- [ ] T066 Verify `.gitignore` excludes: `.env`, `__pycache__`, `*.pyc`, `embeddings_output/`, local checkpoint files
- [ ] T067 [P] Add version number and changelog: `__version__ = "0.1.0"` in `src/__init__.py`, create `CHANGELOG.md`

### Integration & Deployment

- [ ] T068 Create `backend/Dockerfile` (optional) for containerized deployment: Python 3.11, UV, copy code, entrypoint to `python src/main.py`
- [ ] T069 Create `backend/.dockerignore` to exclude unnecessary files from image
- [ ] T070 Create `backend/run_pipeline.sh` (simplified wrapper) to standardize local execution across OSes
- [ ] T071 Validate `uv sync` produces consistent `uv.lock` across different machines

### Final Validation

- [ ] T072 Run full test suite (`pytest tests/`) and verify all tests pass
- [ ] T073 Run end-to-end on sample book (5-10 pages) and verify all steps succeed
- [ ] T074 Verify `uv run python src/main.py --help` displays all options correctly
- [ ] T075 Verify `uv run python src/main.py` runs successfully with valid `.env` (or provide test mode)

**Checkpoint**: Production-ready codebase; all tests pass; documentation complete; ready for release

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
  ↓
Phase 2: Foundational (BLOCKS all user stories)
  ↓ (Foundational must complete before user stories start)
Phase 3: User Story 1 (P1) - MVP
Phase 4: User Story 2 (P2)
Phase 5: User Story 3 (P3)
  ↓ (Can proceed in parallel after Foundational)
Phase 6: Testing & Validation
  ↓
Phase 7: Performance & Documentation
  ↓
Phase 8: Polish & Cross-Cutting Concerns
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) + User Story 1 data (deduplication, logging enhancements)
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) + User Story 1 + User Story 2 (reproducibility and config features)

### Within Phase 2 (Foundational)

All T010-T015 marked `[P]` can run in parallel (different files):
- T010: crawler.py
- T011: extractor.py
- T012: chunker.py
- T013: deduplicator.py
- T014: retry_policy.py
- (T015: checkpoint.py - no [P] marker, depends on others for data structures)

### Parallel Opportunities

**Setup Phase (T001-T009)**:
- T003, T004, T005, T006, T007 can run in parallel (different files)

**Foundational Phase (T010-T015)**:
- T010, T011, T012, T013, T014 can run in parallel (different files)
- T015 should follow (depends on module interfaces)

**User Story 1 Implementation (T016-T022)**:
- T016, T017 can run in parallel (embedder.py, storage.py)
- T018, T019, T020 sequential (pipeline.py depends on T016, T017)
- T021, T022 final (examples and docs)

**Testing Phase (T040-T052)**:
- All unit tests (T040-T045) can run in parallel
- All contract tests (T046-T047) can run in parallel
- Integration tests (T048-T052) sequential

**Documentation Phase (T056-T061)**:
- T057, T058, T059, T060, T061 can run in parallel

**Polish Phase (T062-T075)**:
- T062, T063, T064, T065, T067 can run in parallel (linting, type hints, docstrings, security)
- T066, T068, T069, T070, T071 can run in parallel (config files, Docker, scripts)
- T072, T073, T074, T075 sequential (validation and final checks)

---

## Parallel Execution Example: User Story 1

```bash
# After Foundational phase (T010-T015) completes:

# Launch embedder and storage in parallel (both needed by pipeline):
Task T016: Create embedder.py
Task T017: Create storage.py

# Wait for T016 + T017 to complete, then:
Task T018: Create pipeline.py (orchestrator)
Task T019: Create main.py (CLI)

# Then in parallel:
Task T020: Create log_generator.py
Task T021: Create run_embedding_pipeline.sh

# Final:
Task T022: Update documentation
```

---

## MVP Scope (Suggested Implementation Path)

To deliver a working MVP quickly:

1. **Complete Phase 1**: Setup (T001-T009) - ~30 min
2. **Complete Phase 2**: Foundational (T010-T015) - ~1.5 hours
3. **Complete Phase 3**: User Story 1 (T016-T022) - ~2 hours
4. **Run T072-T075**: Validation - ~30 min

**Total MVP time**: ~4 hours → Functional end-to-end pipeline

**Stop here if**: You need to validate core pipeline functionality quickly

**Next**: Add User Story 2 (data quality) and Story 3 (reproducibility) for production readiness

---

## Task Summary

| Phase | ID Range | Count | Duration | Blocking |
|-------|----------|-------|----------|----------|
| Setup | T001-T009 | 9 | 30 min | No |
| Foundational | T010-T015 | 6 | 1.5 hrs | **YES** |
| User Story 1 (P1) | T016-T022 | 7 | 2 hrs | MVP |
| User Story 2 (P2) | T023-T030 | 8 | 1.5 hrs | Production quality |
| User Story 3 (P3) | T031-T039 | 9 | 1.5 hrs | Production reproducibility |
| Testing | T040-T052 | 13 | 2 hrs | Validation |
| Performance & Docs | T053-T061 | 9 | 1 hr | Documentation |
| Polish | T062-T075 | 14 | 1 hr | Final quality |
| **TOTAL** | **T001-T075** | **75** | **~10.5 hrs** | |

---

## Notes

- All file paths use `backend/` prefix (single Python project structure from plan.md)
- Tests are OPTIONAL but recommended for validation and regression prevention
- Each task includes actionable description with exact file paths
- [P] markers indicate parallelizable tasks (different files, no cross-dependencies)
- Checkpoints after each phase enable stopping point for validation or demo
- Configuration model (T005) enables all subsequent tasks to use environment variables
- Foundation phase (T010-T015) must complete before any user story work begins
- Each user story is independently testable and deployable (incremental delivery)

---

## Getting Started

1. Start with Phase 1 (Setup): `T001` → `T009` (in order)
2. Progress to Phase 2 (Foundational): `T010` → `T015` (can parallelize T010-T014)
3. **Stop and validate before continuing to user stories**
4. Choose implementation path:
   - **MVP**: Phase 1 + 2 + 3 (User Story 1 only)
   - **Production**: Phase 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 (all features)

Good luck! 🚀
