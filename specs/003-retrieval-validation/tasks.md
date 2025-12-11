# Implementation Tasks: Retrieval Pipeline Validation for RAG System

**Feature**: 003-retrieval-validation
**Date**: 2025-12-12
**Branch**: 003-retrieval-validation
**MVP Scope**: User Story 1 (P1) - Core validation with predefined queries
**Total Tasks**: 75+ implementation tasks across 8 phases

---

## Executive Summary

This document breaks down the retrieval validation feature into independently testable phases, organized by user story priority (P1, P2, P3). Each phase builds incrementally on previous work, with clear acceptance criteria and parallelization opportunities.

**Implementation Strategy**:
1. **Phase 1 (Setup)**: Project initialization, dependencies, configuration
2. **Phase 2 (Foundational)**: Shared infrastructure - query loading, configuration, logging
3. **Phase 3 (P1 MVP)**: Core validation - query embedding, retrieval, basic reporting
4. **Phase 4 (P2 Enhancement)**: Advanced reporting - detailed metrics, CSV/JSON export
5. **Phase 5 (P3 Advanced)**: Custom queries, filtering, comparative analysis
6. **Phase 6 (Testing)**: Unit tests, integration tests, edge case validation
7. **Phase 7 (Documentation)**: README, examples, troubleshooting guides
8. **Phase 8 (Polish)**: Error handling, performance optimization, CI/CD integration

---

## User Story Dependency Graph

```
P1: Validate Query Retrieval Accuracy (MVP)
    ├─ Core retrieval loop
    ├─ Predefined test queries
    └─ Console output (minimal)

P2: Generate Debug Report with Metrics
    ├─ Depends on P1: retrieval results
    ├─ Enhanced reporting (JSON/CSV)
    └─ Per-query metrics

P3: Support Custom Query Sets and Filtering
    ├─ Depends on P1: retrieval function
    ├─ Custom query loading
    └─ Result filtering (URL, section, chunk index)
```

**Parallelization**: P2 and P3 can be developed in parallel after P1 core is complete. P1 modules (embedding, retrieval, basic report) are blockers for all others.

---

## Phase 1: Setup & Project Initialization

### Phase Goal
Initialize project structure, dependencies, configuration, and logging infrastructure.

### Independent Test Criteria
- Project directory structure created
- UV dependencies installed and locked
- .env configuration file populated with test values
- Logger initialized and outputs JSON
- No API calls made (dry configuration only)

---

- [ ] T001 Create backend/src/ directory structure per plan.md (create subdirectories: models/, services/, cli/)
- [ ] T002 Copy .env.example to backend/.env and populate with test Cohere + Qdrant credentials
- [ ] T003 Create backend/pyproject.toml with UV dependencies (cohere, qdrant-client, pydantic, click or argparse, pytest)
- [ ] T004 Run `uv sync` to install and lock dependencies
- [ ] T005 Create backend/src/__init__.py with package exports (config, models, services)
- [ ] T006 Implement backend/src/config.py with Pydantic Settings class for .env loading and validation
- [ ] T007 Implement backend/src/logger.py with JSON logging to console and file (validation.log)
- [ ] T008 Create backend/.gitignore excluding .env, __pycache__, embeddings_output/, *.log
- [ ] T009 Create backend/examples/predefined_queries.json with 10 test queries (from spec.md lines 173-184)

---

## Phase 2: Foundational Infrastructure

### Phase Goal
Build shared, reusable components that all user stories depend on: configuration, data models, query loading.

### Independent Test Criteria
- Configuration system loads .env without errors
- Data models validate correctly (Pydantic)
- Query loader parses JSON files
- Logger outputs JSON with timestamps
- All foundational modules have <300 lines of code

---

- [ ] T010 Implement backend/src/models.py with Pydantic data classes:
  - TestQuery (id, text, topic, difficulty, expected_chapters, notes)
  - RetrievalResult (rank, similarity_score, chunk_id, source_url, section_title, text_excerpt, relevance_assessment, relevance_notes)
  - ValidationResult (query_id, query_text, retrieved_chunks, results, error, execution_time_ms)
  - ValidationReport (validation_id, timestamp, total_queries, queries_executed, queries_failed, results, summary, filters_applied, duration_seconds)
  - QuerySet (test_queries, metadata with name, created_at, description, version, author)

- [ ] T011 Add Pydantic validation rules to models.py:
  - TestQuery.id: non-empty, alphanumeric only
  - TestQuery.text: non-empty, ≤500 chars
  - RetrievalResult.similarity_score: float in [0.0, 1.0]
  - ValidationResult: consistency checks (results count == retrieved_chunks)
  - ValidationReport.pass_fail: True iff relevant_percent ≥ 80

- [ ] T012 Implement backend/src/query_loader.py with QueryLoader class:
  - load_predefined_queries() → loads backend/examples/predefined_queries.json
  - load_custom_queries(path) → loads user-provided JSON file
  - validate_queries(queries) → checks for duplicate IDs, malformed entries
  - Error handling: skip malformed queries, log warnings

- [ ] T013 [P] Implement backend/src/retry_policy.py (from Feature 002) with exponential backoff for API failures:
  - RetryPolicy class with configurable max_retries, initial_delay_ms, max_delay_ms, backoff_multiplier
  - Methods: retry_async(func, *args), retry_sync(func, *args)

- [ ] T014 [P] Implement backend/src/models.py extended with helper methods:
  - TestQuery.to_dict() for JSON serialization
  - ValidationResult.is_success() → error is None
  - ValidationReport.get_summary_stats() → computes avg/min/max similarity, percentages

---

## Phase 3: User Story 1 (P1) - Validate Query Retrieval Accuracy (MVP)

### Phase Goal
Core retrieval validation: embed queries, search Qdrant, retrieve chunks, validate accuracy.

### Independent Test Criteria (P1 MVP)
- Query embedding via Cohere works (can test with --dry-run mock)
- Qdrant similarity search returns top-K results
- Retrieved chunks have metadata (URL, section, text)
- Similarity scores in valid range [0.0, 1.0]
- At least 80% of predefined queries return results with score ≥0.7
- Console output shows query + top result + score

### User Story Acceptance
- ✅ FR-001: Execute queries against Qdrant, retrieve top-K
- ✅ FR-002: Embed queries using Cohere
- ✅ FR-003: Calculate cosine similarity scores
- ✅ FR-004: Fetch chunk text and metadata
- ✅ FR-005: Validate metadata consistency
- ✅ FR-006: Support predefined test query sets

---

### T015-T030: Core Embedding & Retrieval

- [ ] T015 Implement backend/src/query_embedder.py with QueryEmbedder class:
  - __init__(api_key: str, model: str = "embed-3-large", batch_size: int = 8)
  - embed_query(query_text: str) → returns List[float] (4096-D vector)
  - embed_batch(queries: List[str]) → returns List[List[float]] with batching
  - Error handling: retry on timeout/rate limit, raise on API key invalid

- [ ] T016 [P] Implement backend/src/retrieval_client.py with QdrantRetriever class:
  - __init__(url: str, api_key: str, collection_name: str = "book_embeddings")
  - search_similar(query_vector: List[float], top_k: int = 5) → returns List[RetrievalResult]
  - Extracts metadata from Qdrant payload (url, section_title, chunk_id, text)
  - Error handling: check collection exists, handle empty results gracefully

- [ ] T017 [P] Implement backend/src/validator.py with Validator class:
  - execute_query(query: TestQuery) → returns ValidationResult
  - execute_queries(query_set: QuerySet) → returns List[ValidationResult]
  - Calls: embedder.embed_query() → retriever.search_similar() → ValidationResult
  - Tracks execution_time_ms per query

- [ ] T018 Implement backend/src/context_extractor.py (user request #3):
  - extract_context(results: List[RetrievalResult]) → merged paragraph
  - Joins top-3 chunk text_excerpts with sentence boundaries preserved
  - Used later in P2 reporting

- [ ] T019 [P] Implement backend/src/report_generator.py with ReportGenerator class (basic console):
  - generate_console_report(results: List[ValidationResult]) → prints to stdout
  - Shows: query text, top result rank/score/url, pass/fail per query
  - Summary: avg_similarity, % relevant, overall pass/fail

- [ ] T020 Create backend/src/main.py entry point with argparse:
  - Subcommand: `validate`
  - Options: --queries (default: predefined), --top-k (default: 5), --dry-run, --log-level
  - Load config from .env
  - Execute validation run
  - Print console report

### T021-T030: P1 Acceptance Tests & Examples

- [ ] T021 Create backend/examples/run_validation.sh script:
  - Runs `uv run python src/main.py validate` with predefined queries
  - Shows expected output format
  - Callable from CI/CD

- [ ] T022 Create backend/tests/fixtures/predefined_queries.json with 5 test queries for unit tests
- [ ] T023 Create backend/tests/fixtures/mock_qdrant_results.json with expected retrieval results
- [ ] T024 Create backend/tests/unit/test_query_embedder.py (mock Cohere API):
  - Mock embed_query() to return fake 4096-D vector
  - Test batch embedding with batching logic
- [ ] T025 [P] Create backend/tests/unit/test_retrieval_client.py (mock Qdrant):
  - Mock search_similar() with fake results
  - Test metadata extraction
  - Test error handling (no results, API down)
- [ ] T026 [P] Create backend/tests/unit/test_validator.py:
  - Test execute_query() with mocked embedder + retriever
  - Test execute_queries() with multiple queries
  - Test execution_time_ms tracking
- [ ] T027 Create backend/tests/unit/test_report_generator.py:
  - Test console report formatting
  - Test summary calculation
- [ ] T028 Create backend/tests/integration/test_p1_end_to_end.py:
  - End-to-end flow: load queries → embed → retrieve → report
  - All with mocked APIs, no real Cohere/Qdrant calls
  - Verify console output format
- [ ] T029 Create backend/tests/conftest.py with pytest fixtures:
  - mock_cohere_client
  - mock_qdrant_client
  - predefined_queries fixture
  - validation_result fixture
- [ ] T030 Document P1 acceptance criteria in backend/P1_ACCEPTANCE.md:
  - Expected outputs for 5 test queries
  - Pass/fail criteria per query
  - Console output examples

---

## Phase 4: User Story 2 (P2) - Generate Debug Report with Metrics

### Phase Goal
Enhanced reporting: JSON/CSV exports, detailed metrics, per-query debugging info.

### Independent Test Criteria (P2)
- JSON report generated with complete ValidationReport structure
- CSV export with one row per result
- Metrics include: avg/min/max similarity, relevance percentages
- Low-confidence results (<0.7) flagged in report
- Report saved to file and parseable

### User Story Acceptance
- ✅ FR-007: Generate JSON/CSV debug report
- ✅ FR-008: Support manual relevance assessment
- Extends FR-001 through FR-006 with detailed output

---

### T031-T050: Advanced Reporting

- [ ] T031 Extend backend/src/report_generator.py with JSON report generation:
  - generate_json_report(validation_report: ValidationReport) → JSON string
  - Serializes full ValidationReport with all fields
  - Includes timestamp, validation_id, per-query results, summary stats

- [ ] T032 [P] Extend backend/src/report_generator.py with CSV export:
  - generate_csv_report(validation_report: ValidationReport) → CSV string
  - Columns: query_id, query_text, rank, similarity_score, source_url, section_title, chunk_id, relevance_assessment
  - One row per RetrievalResult (multiple rows per query if K > 1)

- [ ] T033 Implement backend/src/report_writer.py:
  - save_json_report(report: ValidationReport, output_path: str)
  - save_csv_report(report: ValidationReport, output_path: str)
  - Creates output directory if missing
  - Error handling: permission denied, disk full

- [ ] T034 [P] Implement backend/src/relevance_assessor.py for manual assessment:
  - interactive_assess(results: List[ValidationResult]) → prompts user for each result
  - Updates relevance_assessment field ("relevant", "partially_relevant", "irrelevant")
  - Saves optional notes per result

- [ ] T035 Extend backend/src/validator.py with metrics calculation:
  - calculate_summary_stats(results: List[ValidationResult]) → SummaryStats
  - Computes: avg/min/max similarity, percentage relevant/partial/irrelevant
  - Handles null assessments correctly (only count assessed results)

- [ ] T036 Extend backend/src/main.py with `validate` options:
  - --format {json,csv,summary} (default: json + summary to stdout)
  - --output FILE (save report to file)
  - --assess-manually (enable interactive relevance labeling)

- [ ] T037 Create backend/src/report_formatter.py for human-readable output:
  - format_summary(summary: SummaryStats) → pretty table
  - format_query_results(results: List[ValidationResult]) → formatted text
  - Highlight low scores (<0.7) and high scores (>0.95)

- [ ] T038 Add `report` command to backend/src/main.py:
  - Options: --input FILE, --format {json,csv,summary,html}
  - Load and display existing report
  - Filter by --filter-assessment {relevant, partial, irrelevant}

### T039-T050: P2 Tests & Documentation

- [ ] T039 Create backend/tests/unit/test_report_generator.py extended:
  - Test JSON serialization for all entity types
  - Test CSV format with multiple queries/results
  - Test escaping of special characters (commas, quotes in text)

- [ ] T040 [P] Create backend/tests/unit/test_report_writer.py:
  - Test save_json_report() creates file
  - Test save_csv_report() creates file
  - Test error handling (permission denied)

- [ ] T041 [P] Create backend/tests/unit/test_relevance_assessor.py:
  - Mock user input for interactive assessment
  - Verify relevance_assessment field updated
  - Test notes parsing

- [ ] T042 Create backend/tests/integration/test_p2_reporting.py:
  - Full flow: validate → generate JSON/CSV reports
  - Verify report files created and parseable
  - Verify summary stats correct

- [ ] T043 Create backend/tests/fixtures/sample_validation_report.json:
  - Complete ValidationReport with 5 queries
  - Used for testing report loading and formatting

- [ ] T044 Document P2 report format in backend/REPORT_FORMAT.md:
  - JSON schema with examples
  - CSV column definitions
  - Summary statistics definitions
  - How to interpret pass/fail criteria

- [ ] T045 Create backend/examples/sample_report.json with expected output
- [ ] T046 Create backend/examples/sample_report.csv with expected output
- [ ] T047 Create backend/examples/run_validation_with_report.sh:
  - Runs validation and saves to file
  - Shows how to view report with `report` command
- [ ] T048 Add P2 acceptance criteria to backend/P2_ACCEPTANCE.md:
  - JSON report structure validation
  - CSV export validation
  - Manual assessment workflow
- [ ] T049 Update backend/src/main.py help text with P2 options
- [ ] T050 Create backend/tests/conftest.py extended with report fixtures

---

## Phase 5: User Story 3 (P3) - Support Custom Query Sets and Filtering

### Phase Goal
Custom queries, result filtering, comparative analysis across validation runs.

### Independent Test Criteria (P3)
- Custom query file loads from JSON
- URL filtering works (substring/regex match)
- Section filtering works (exact match)
- Chunk index range filtering works (e.g., "100-500")
- Filtered results appear in reports correctly
- Multiple reports can be compared

### User Story Acceptance
- ✅ FR-009: Support custom query sets
- ✅ FR-010: Support filtering by URL, section, chunk index
- Extends P1 and P2 with targeted validation capabilities

---

### T051-T070: Custom Queries & Filtering

- [ ] T051 Create backend/examples/custom_queries_template.json:
  - Empty template with fields: id, text, topic, difficulty, expected_chapters, notes
  - Comments explaining each field
  - 2-3 example queries

- [ ] T052 Extend backend/src/query_loader.py:
  - load_custom_queries(path) → validates and loads custom set
  - Error handling: missing file, malformed JSON, duplicate IDs
  - Warning: skip invalid queries, continue with rest

- [ ] T053 Implement backend/src/filter_engine.py:
  - FilterConfig dataclass with url_pattern, section_name, chunk_index_range
  - apply_filters(results: List[RetrievalResult], filters: FilterConfig) → filtered results
  - URL filtering: regex or substring match against source_url
  - Section filtering: exact match against section_title
  - Chunk index filtering: parse "100-500" range and check chunk_id

- [ ] T054 [P] Integrate filtering into backend/src/validator.py:
  - execute_queries() accepts optional filters: FilterConfig
  - Applies filters to results before returning
  - Tracks filters_applied in ValidationReport

- [ ] T055 [P] Extend backend/src/main.py `validate` command:
  - --queries PATH (support custom queries file)
  - --filter-url TEXT (substring match against source URLs)
  - --filter-section TEXT (match section title)
  - --filter-chunks "START-END" (chunk index range)
  - Validation: confirm filters make sense (e.g., valid range syntax)

- [ ] T056 Implement backend/src/report_comparator.py:
  - load_report(path) → loads ValidationReport from JSON
  - compare_reports(report1, report2) → comparison object
  - Metrics: score improvements/degradations, relevance changes
  - Output: comparison table (query, old_score, new_score, delta)

- [ ] T057 Extend backend/src/main.py with `compare` command (future):
  - --first FILE --second FILE
  - Loads both reports and generates comparison
  - Output: JSON or formatted table

### T058-T070: P3 Tests & Examples

- [ ] T058 Create backend/examples/custom_queries_robotics.json:
  - 5 custom queries about kinematics/dynamics
  - With expected_chapters targeting Chapter 2
- [ ] T059 Create backend/examples/custom_queries_safety.json:
  - 5 custom queries about safety
  - With expected_chapters targeting safety sections

- [ ] T060 [P] Create backend/tests/unit/test_filter_engine.py:
  - Test URL filtering with regex patterns
  - Test section filtering
  - Test chunk index range parsing
  - Edge cases: empty filters, invalid range syntax

- [ ] T061 [P] Create backend/tests/unit/test_query_loader.py extended:
  - Test loading custom queries
  - Test error handling (missing file, malformed JSON)
  - Test duplicate ID detection

- [ ] T062 Create backend/tests/unit/test_report_comparator.py:
  - Test loading and comparing two reports
  - Test delta calculation (score improvements/degradations)
  - Test comparison output formatting

- [ ] T063 Create backend/tests/integration/test_p3_filtering.py:
  - End-to-end: load custom queries, apply filters, generate filtered report
  - Verify filtered results match expectations
  - Test all filter types individually and combined

- [ ] T064 Create backend/tests/integration/test_p3_custom_queries.py:
  - End-to-end: load custom queries from file
  - Execute validation
  - Verify all custom queries ran

- [ ] T065 Create backend/tests/fixtures/custom_queries_sample.json:
  - Sample custom query set for testing
  - With known expected results

- [ ] T066 Document custom query format in backend/CUSTOM_QUERIES.md:
  - JSON schema
  - Field definitions
  - Examples
  - Best practices for creating custom query sets

- [ ] T067 Document filtering in backend/FILTERING.md:
  - URL filtering patterns (regex or substring)
  - Section filtering (exact match)
  - Chunk index range syntax
  - Examples: filter by chapter, filter by page type

- [ ] T068 Create backend/examples/run_custom_validation.sh:
  - Runs validation with custom queries
  - Shows filtering examples
  - Demonstrates comparison workflow

- [ ] T069 Add P3 acceptance criteria to backend/P3_ACCEPTANCE.md:
  - Custom query loading
  - Filtering validation
  - Comparison output

- [ ] T070 Create backend/tests/conftest.py extended with custom query fixtures

---

## Phase 6: Testing & Quality Assurance

### Phase Goal
Comprehensive test coverage, edge case handling, performance validation.

### Independent Test Criteria
- Unit test coverage ≥80%
- Integration tests pass (mocked APIs)
- All edge cases handled gracefully
- Performance benchmarks met (<2s per query)
- No API calls in tests

---

- [ ] T071 Create backend/tests/unit/test_config.py:
  - Test Settings validation
  - Test .env loading with valid/invalid values
  - Test required field checking

- [ ] T072 [P] Create backend/tests/unit/test_models.py:
  - Test Pydantic validation for all models
  - Test invalid values (similarity > 1.0, negative execution_time)
  - Test serialization/deserialization

- [ ] T073 [P] Create backend/tests/edge_cases/test_empty_results.py:
  - Query returns no results (similarity < 0.5)
  - Verify handled gracefully, logged, report shows "no relevant results"

- [ ] T074 [P] Create backend/tests/edge_cases/test_malformed_queries.py:
  - Empty query text
  - Query too short (<3 chars)
  - Verify validation rejects or skips with warning

- [ ] T075 Create backend/tests/edge_cases/test_high_similarity_scores.py:
  - Verify warning logged when all scores > 0.95
  - Verify report flags potential embedding quality issue

---

## Phase 7: Documentation & User Guides

### Phase Goal
Comprehensive documentation for end users and developers.

### Independent Test Criteria
- README updated with all commands and options
- Quickstart guide works as written
- Examples are executable
- Troubleshooting covers common issues

---

- [ ] T076 Update backend/README.md with retrieval validation section:
  - Feature overview
  - Quick start (3 steps)
  - Command reference for `validate` and `report`
  - Filtering and custom queries
  - Output format explanation

- [ ] T077 Create backend/TROUBLESHOOTING.md:
  - Common errors (API failures, missing collection)
  - Solutions with exact commands
  - Debug logging (--log-level DEBUG)

- [ ] T078 Create backend/EXAMPLES.md:
  - 5 example workflows (basic validation, debugging, filtering, comparison)
  - Copy-paste ready commands
  - Expected output for each

- [ ] T079 Create backend/ARCHITECTURE.md:
  - Module overview (embedder, retriever, validator, reporter)
  - Data flow diagram (query → embed → retrieve → report)
  - Extension points for future features

---

## Phase 8: Polish, Optimization & CI/CD Integration

### Phase Goal
Error handling, performance optimization, production-ready code, CI/CD setup.

### Independent Test Criteria
- All error cases handled with clear messages
- Performance: single query <2s, 10 queries <15s
- Code passes linting (pylint, flake8)
- CI/CD pipeline configured

---

- [ ] T080 Add comprehensive error handling to all modules:
  - API failures (Cohere rate limit, Qdrant timeout)
  - File I/O errors (missing queries file, permission denied)
  - Configuration errors (missing .env, invalid values)
  - All with clear user-facing messages

- [ ] T081 Add performance logging:
  - Track execution_time_ms per query
  - Log aggregate stats (total time, average query time)
  - Warn if any query exceeds 2s or total exceeds 15s

- [ ] T082 Create backend/pyproject.toml extended:
  - Add dev dependencies: pytest, pylint, black, mypy
  - Configure pytest with minimum coverage threshold (80%)
  - Configure linting rules

- [ ] T083 Create backend/.pylintrc and backend/.flake8:
  - Code quality rules
  - Exclude generated files

- [ ] T084 Create .github/workflows/validation-tests.yml:
  - Run on PR to 003-retrieval-validation branch
  - Execute: `uv sync && uv run pytest tests/ --cov=src`
  - Run: `uv run pylint src/`
  - Require all tests pass before merge

- [ ] T085 Create backend/CONTRIBUTING.md:
  - How to add new test queries
  - How to extend validators
  - Code style guidelines
  - PR checklist

- [ ] T086 Add type hints to all modules:
  - Function signatures with input/output types
  - Run mypy for type checking

- [ ] T087 Create backend/performance_test.py:
  - Benchmark: 10 queries, measure total time
  - Assert: total time < 15s, per-query < 2s
  - Generate performance report

- [ ] T088 Create docker/Dockerfile for validation suite (optional):
  - Builds with UV
  - Copies configuration
  - Entrypoint: python src/main.py

---

## Task Execution Strategy

### MVP Scope (Phase 1-3, ~30 tasks)
Implement User Story 1 for P1 MVP. This includes:
- Project setup (T001-T009)
- Foundational infrastructure (T010-T020)
- Core validation (T015-T030)

**MVP Acceptance**: Run `uv run python src/main.py validate` with predefined queries, get console output showing retrieved chunks and similarity scores.

### Phase 2 Enhancement (Phase 4, ~20 tasks)
Add P2 reporting capabilities. Extends MVP with:
- JSON/CSV export (T031-T038)
- Manual assessment (T034)
- Advanced reporting (T039-T050)

**P2 Acceptance**: `uv run python src/main.py validate --format json --output report.json` generates valid JSON report with summary stats.

### Phase 3 Advanced (Phase 5, ~20 tasks)
Add P3 custom queries and filtering:
- Custom query loading (T051-T055)
- Filtering engine (T053-T055)
- Comparison tools (T056-T070)

**P3 Acceptance**: Load custom queries, apply filters, generate comparative reports.

### Full Implementation (All phases, 75+ tasks)
Complete feature with testing, documentation, and production hardening.

---

## Parallelization Opportunities

### Parallel After T020 (Foundational Complete):

**Stream A (P1 Core)**: T015-T030 (core embedding + retrieval)
**Stream B (Foundational Tests)**: T021-T030 (unit tests, fixtures)
**Stream C (Configuration)**: T006-T008 (config, logging)

All three streams can run in parallel; merge at T031 (P2 reporting).

### Parallel After T035 (P1 Complete):

**Stream D (P2 Reporting)**: T031-T050 (JSON, CSV, metrics)
**Stream E (P3 Filtering)**: T051-T070 (custom queries, filters)

Both can develop in parallel; merge at T071 (testing phase).

### Parallel After T050 (P2 Complete):

**Stream F (Testing)**: T071-T075 (comprehensive test suite)
**Stream G (Documentation)**: T076-T079 (README, guides)
**Stream H (Polish)**: T080-T088 (error handling, CI/CD)

All three streams can run in parallel.

---

## Task Dependencies

```
T001-T009 (Setup)
    ↓
T010-T020 (Foundational) ← Blocks all user stories
    ├─→ T015-T030 (P1 MVP)
    │     ├─→ T031-T050 (P2 Reporting)
    │     │     └─→ T076-T088 (Polish)
    │     └─→ T051-T070 (P3 Filtering)
    │
    └─→ T021-T030 (Tests, parallel with P1)
          ├─→ T039-T050 (P2 Tests)
          └─→ T058-T070 (P3 Tests)
                └─→ T071-T075 (Edge Cases)
```

---

## Acceptance Criteria by Phase

### Phase 1: Setup ✅
- [ ] Project structure created
- [ ] Dependencies installed (uv sync succeeds)
- [ ] .env configured with test values
- [ ] Logger outputs JSON

### Phase 2: Foundational ✅
- [ ] Configuration system works (loads .env)
- [ ] All Pydantic models validate correctly
- [ ] Query loader parses JSON files
- [ ] No errors on import (python -c "from src import *")

### Phase 3: P1 MVP ✅ (MVP Milestone)
- [ ] `uv run python src/main.py validate` executes with predefined queries
- [ ] Retrieves chunks from Qdrant (mocked in tests)
- [ ] Returns similarity scores in [0.0, 1.0]
- [ ] Console shows: query, top result, score
- [ ] At least 80% of predefined queries score ≥0.7

### Phase 4: P2 ✅
- [ ] `--format json` generates valid JSON report
- [ ] `--format csv` generates valid CSV export
- [ ] Summary stats calculated correctly
- [ ] Relevance assessment supported (manual + auto)

### Phase 5: P3 ✅
- [ ] Custom queries load from JSON file
- [ ] Filtering by URL, section, chunk index works
- [ ] Filtered results appear in reports
- [ ] Reports can be compared

### Phase 6: Testing ✅
- [ ] Unit tests: ≥80% coverage
- [ ] Integration tests: all pass
- [ ] Edge cases: all handled gracefully
- [ ] Performance: <2s per query, <15s for 10 queries

### Phase 7: Documentation ✅
- [ ] README updated
- [ ] Quickstart guide works
- [ ] Examples provided
- [ ] Troubleshooting documented

### Phase 8: Polish ✅
- [ ] Error messages clear and helpful
- [ ] Code passes linting
- [ ] CI/CD pipeline configured
- [ ] Production-ready

---

## File Structure Reference

```
backend/
├── src/
│   ├── __init__.py
│   ├── config.py                   # T006
│   ├── logger.py                   # T007
│   ├── models.py                   # T010-T011
│   ├── query_loader.py             # T012
│   ├── retry_policy.py             # T013
│   ├── query_embedder.py           # T015
│   ├── retrieval_client.py         # T016
│   ├── validator.py                # T017
│   ├── context_extractor.py        # T018
│   ├── report_generator.py         # T019, T031-T032
│   ├── report_writer.py            # T033
│   ├── relevance_assessor.py       # T034
│   ├── filter_engine.py            # T053
│   ├── report_comparator.py        # T056
│   ├── report_formatter.py         # T037
│   └── main.py                     # T020, T036, T038
│
├── tests/
│   ├── conftest.py                 # T029, T050, T070
│   ├── unit/
│   │   ├── test_config.py          # T071
│   │   ├── test_models.py          # T072
│   │   ├── test_query_embedder.py  # T024
│   │   ├── test_retrieval_client.py # T025
│   │   ├── test_validator.py       # T026
│   │   ├── test_report_generator.py # T027, T039
│   │   ├── test_report_writer.py   # T040
│   │   ├── test_relevance_assessor.py # T041
│   │   ├── test_filter_engine.py   # T060
│   │   ├── test_query_loader.py    # T061
│   │   └── test_report_comparator.py # T062
│   ├── integration/
│   │   ├── test_p1_end_to_end.py   # T028
│   │   ├── test_p2_reporting.py    # T042
│   │   ├── test_p3_filtering.py    # T063
│   │   └── test_p3_custom_queries.py # T064
│   ├── edge_cases/
│   │   ├── test_empty_results.py   # T073
│   │   ├── test_malformed_queries.py # T074
│   │   └── test_high_similarity_scores.py # T075
│   └── fixtures/
│       ├── predefined_queries.json  # T022
│       ├── mock_qdrant_results.json # T023
│       ├── custom_queries_sample.json # T065
│       └── sample_validation_report.json # T043
│
├── examples/
│   ├── predefined_queries.json     # T009
│   ├── custom_queries_template.json # T051
│   ├── custom_queries_robotics.json # T058
│   ├── custom_queries_safety.json  # T059
│   ├── sample_report.json          # T045
│   ├── sample_report.csv           # T046
│   ├── run_validation.sh           # T021
│   ├── run_validation_with_report.sh # T047
│   ├── run_custom_validation.sh    # T068
│   └── performance_test.py         # T087
│
├── pyproject.toml                  # T003, T082
├── .env.example                    # T002
├── .env                            # T002 (populated)
├── .gitignore                      # T008
├── .pylintrc                       # T083
├── .flake8                         # T083
├── README.md                       # T076
├── REPORT_FORMAT.md                # T044
├── CUSTOM_QUERIES.md               # T066
├── FILTERING.md                    # T067
├── TROUBLESHOOTING.md              # T077
├── EXAMPLES.md                     # T078
├── ARCHITECTURE.md                 # T079
├── CONTRIBUTING.md                 # T085
├── P1_ACCEPTANCE.md                # T030
├── P2_ACCEPTANCE.md                # T048
├── P3_ACCEPTANCE.md                # T069
├── performance_test.py             # T087
└── validation.log                  # T007 (generated)

.github/
└── workflows/
    └── validation-tests.yml        # T084

docker/
└── Dockerfile                      # T088 (optional)
```

---

## Success Metrics

- **MVP Completion**: Phase 1-3 done; `uv run python src/main.py validate` works end-to-end
- **P1 Validation**: At least 80% of predefined queries return relevant results (score ≥0.7)
- **Test Coverage**: ≥80% code coverage (measured by pytest --cov)
- **Performance**: Single query embedding + retrieval <2s; 10 queries <15s total
- **User Experience**: No more than 3 manual steps to run validation
- **Documentation**: README, quickstart, examples all present and tested

---

## Next Steps After Tasks

1. **Implement Phase 1-3 (MVP)**: ~30 tasks, estimated 3-4 days
2. **Test with real Cohere + Qdrant**: Validate against actual book embeddings
3. **Iterate on P2 + P3**: Add reporting, filtering based on MVP feedback
4. **Production Hardening**: Error handling, logging, CI/CD
5. **Integration with Feature 004 (RAG Agent)**: Use validation results in chatbot

---

**Tasks Status**: ✅ READY FOR IMPLEMENTATION

All 75+ tasks are now specific, actionable, and independently testable. Begin with Phase 1 (T001-T009) for project setup, then proceed to Phase 2 (T010-T020) for foundational infrastructure.
