# Implementation Plan: Retrieval Pipeline Validation for RAG System

**Branch**: `003-retrieval-validation` | **Date**: 2025-12-12 | **Spec**: [specs/003-retrieval-validation/spec.md](spec.md)
**Input**: Feature specification from `specs/003-retrieval-validation/spec.md`

**Note**: This plan guides implementation of a validation suite for vector retrieval accuracy testing before RAG agent integration.

## Summary

Build a CLI-based validation suite that executes test queries against Qdrant embeddings, verifies retrieval accuracy (≥0.7 similarity for ≥80% of queries), and generates detailed debug reports with metrics. Support custom query sets, filtering by source URL/section, and reproducible validation runs. The MVP (P1 story) focuses on query execution and accuracy validation; P2 adds debug reporting; P3 adds custom queries and filtering.

## Technical Context

**Language/Version**: Python 3.11+ (consistent with Feature 002 embedding pipeline)
**Primary Dependencies**:
- Cohere SDK (embed queries using same model as embedded content)
- Qdrant Client (search similarity, retrieve chunks with metadata)
- Pydantic (data models and validation)
- Click or argparse (CLI interface)
- JSON/CSV libraries (report generation)

**Storage**: Local JSON files for validation config, custom query sets, and debug reports; Qdrant Cloud for vector search (no new storage required)
**Testing**: pytest with fixtures for mock Cohere/Qdrant responses
**Target Platform**: Linux/macOS/Windows (CLI, runs locally or in CI/CD)
**Project Type**: CLI tool (single project with modular services)
**Performance Goals**:
- Individual query embedding + retrieval: <2 seconds
- Full validation run (10 queries): <15 seconds total
- Report generation: <5 seconds

**Constraints**:
- Must reuse same Cohere embedding model as Feature 002 (consistency)
- Qdrant collection must already exist and contain embedded chunks (dependency on Feature 002)
- No external APIs beyond Cohere and Qdrant
- Results must be reproducible (same queries + Qdrant state = same results)

**Scale/Scope**:
- 5-10 predefined test queries (P1 MVP)
- Support for custom query sets (P2+)
- Debug report format: JSON or CSV
- Up to 100 queries per validation run supported

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I: Education-First Design** ✅ PASS
- Validation suite validates RAG accuracy, enabling better learning outcomes
- Debug reports teach developers about retrieval quality and embedding gaps
- Edge case handling (stale embeddings, malformed queries) teaches robustness

**Principle II: Practical, Engineering-Focused Content** ✅ PASS
- Directly supports integration of RAG embeddings into chatbot (practical use case)
- Test queries are real questions learners will ask the book's chatbot
- Debug output guides practical improvements to embedding quality

**Principle III: Content Accuracy & Safety (Critical)** ✅ PASS
- Validation ensures RAG accuracy before deployment (safety for chatbot correctness)
- 80% relevance threshold prevents low-quality retrievals from being used
- Clear reporting of failures helps identify and fix embedding issues

**Principle IV: Docosaurus Standards & Consistency** ✅ PASS
- Validation verifies that Docosaurus-sourced chunks are correctly embedded and retrievable
- Maintains consistency between source (book chapters) and embedded vectors
- Source URLs preserved in metadata for traceability

**Principle V: Testable, Reproducible Examples** ✅ PASS
- Validation suite itself is reproducible (same inputs = same results)
- Test queries are predefined and version-controlled
- Debug reports make retrieval quality measurable and auditable

**Principle VI: Iterative Improvement & Community Feedback** ✅ PASS
- Custom query sets enable community to validate specific book sections
- Reports surface issues that can be tracked and improved iteratively
- Validation data supports quarterly content reviews (Constitution VI)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── config.py                # Configuration (Cohere model, Qdrant URL, thresholds)
│   ├── models.py                # Data models (TestQuery, RetrievalResult, ValidationReport)
│   ├── logger.py                # Logging setup (JSON format for reports)
│   ├── query_embedder.py        # Query embedding via Cohere API
│   ├── retrieval_client.py      # Qdrant similarity search and chunk retrieval
│   ├── validator.py             # Core validation logic (execute queries, score results)
│   ├── report_generator.py      # Generate JSON/CSV debug reports
│   ├── query_loader.py          # Load predefined and custom query sets
│   ├── filter_engine.py         # URL, section, chunk index filtering
│   ├── main.py                  # CLI entry point (argparse)
│   └── cli.py                   # CLI command handlers (if using Click)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures (mock Cohere, Qdrant)
│   ├── unit/
│   │   ├── test_query_embedder.py
│   │   ├── test_retrieval_client.py
│   │   ├── test_validator.py
│   │   ├── test_report_generator.py
│   │   └── test_filter_engine.py
│   ├── integration/
│   │   ├── test_end_to_end.py   # Full validation run with mocked APIs
│   │   └── test_report_output.py
│   └── fixtures/
│       ├── mock_queries.json     # Test data
│       └── mock_results.json
│
├── examples/
│   ├── predefined_queries.json   # Default test queries (10 questions)
│   ├── custom_queries_template.json
│   └── run_validation.sh         # Example run script
│
├── pyproject.toml
├── .env.example
├── README.md
└── .gitignore
```

**Structure Decision**: Single CLI project (Option 1). Validation suite is self-contained, no separate frontend/backend. Reuses same backend/ directory as Feature 002 embedding pipeline for consistency. Tests organized by scope (unit, integration). Examples include predefined queries and run scripts.

## Phase 0: Research & Unknowns Resolution

All technical context is determined; no NEEDS CLARIFICATION items remain.

### Research Topics Addressed

**Topic 1: Query Embedding Best Practices**
- **Decision**: Use Cohere API with same model as Feature 002 (embed-3-large)
- **Rationale**: Consistency required for vector space alignment; reuses existing API key and configuration
- **Alternative Rejected**: Separate embedding model would create misalignment between query and chunk vectors

**Topic 2: Similarity Scoring & Threshold Selection**
- **Decision**: Use cosine similarity (Qdrant's default); threshold ≥0.7 for "relevant"
- **Rationale**: Cosine similarity standard for embedding spaces; 0.7 threshold empirically validated in RAG literature for high-precision retrieval
- **Validation Path**: Spec includes edge case handling for unreasonably high scores (flags >0.95) and low scores (<0.5)

**Topic 3: Validation Architecture Pattern**
- **Decision**: CLI-based tool with modular validators, not integrated into embedding pipeline
- **Rationale**: Separation of concerns; validation runs independently after embeddings exist; enables CI/CD validation without triggering re-embedding
- **Benefit**: Supports rapid iteration on queries and filtering without touching pipeline

**Topic 4: Report Format & Reproducibility**
- **Decision**: JSON primary (parseable, structured); CSV optional for spreadsheet viewing
- **Rationale**: JSON enables programmatic validation in CI/CD; includes full result history; CSV provides human-friendly export
- **Reproducibility**: All inputs (queries, Qdrant state) tracked; results deterministic given fixed inputs

**Topic 5: Custom Query Set Format**
- **Decision**: JSON with optional metadata (difficulty, expected_chapters, notes)
- **Rationale**: Lightweight, version-controllable, integrates with CI/CD; matches Feature 002's configuration approach
- **Flexibility**: Allows filtering tests by difficulty or chapter, supports A/B testing different query sets

### No External Research Needed

- Cohere API stability/reliability: established (Feature 002 uses it)
- Qdrant client library: established Python bindings available
- Pydantic validation patterns: established (Feature 002 uses Pydantic)
- pytest fixtures for mocking: standard pytest patterns
- JSON/CSV generation: standard Python libraries

**Gate Result**: ✅ PASS - All unknowns resolved; no blockers for Phase 1 design

## Phase 1: Design Artifacts & Contracts

### 1. Data Model (data-model.md)

Key entities extracted from specification:

**TestQuery**
- `id`: str (unique identifier, e.g., "q1")
- `text`: str (query string, e.g., "What is physical AI?")
- `topic`: str (optional, e.g., "foundational", "middleware")
- `difficulty`: str (optional, one of: "easy", "medium", "hard")
- `expected_chapters`: List[str] (optional, chapter slugs where answer should be found)
- `notes`: str (optional, metadata for manual review)

**RetrievalResult**
- `rank`: int (1-K, where K is top-K limit)
- `similarity_score`: float (0.0-1.0, cosine similarity)
- `chunk_id`: str (unique chunk identifier from Qdrant)
- `source_url`: str (full URL to book page)
- `section_title`: str (chapter/section name)
- `text_excerpt`: str (first 200 chars of chunk text)
- `relevance_assessment`: str (one of: "relevant", "partially_relevant", "irrelevant", or null if not assessed)
- `relevance_notes`: str (optional, manual comments)

**ValidationResult (single query)**
- `query_id`: str
- `query_text`: str
- `retrieved_chunks`: int (count of results returned)
- `results`: List[RetrievalResult] (top-K results)
- `error`: str (null if successful, error message if failed)
- `execution_time_ms`: float (time to embed query + search Qdrant)

**ValidationReport (full run)**
- `validation_id`: str (UUID, e.g., "run-2025-12-12T10:30:00Z")
- `timestamp`: str (ISO 8601)
- `total_queries`: int
- `queries_executed`: int
- `queries_failed`: int
- `results`: List[ValidationResult] (one per query)
- `summary`: {
    - `avg_similarity_score`: float
    - `min_similarity_score`: float
    - `max_similarity_score`: float
    - `relevant_results_percent`: float (0-100)
    - `partially_relevant_percent`: float (0-100)
    - `irrelevant_percent`: float (0-100)
    - `pass_fail`: bool (≥80% relevant = pass)
  }
- `filters_applied`: dict (URL, section, chunk_index filters if any)
- `duration_seconds`: float

**QuerySet (container)**
- `test_queries`: List[TestQuery]
- `metadata`: {
    - `name`: str (e.g., "predefined_set_v1")
    - `created_at`: str (ISO 8601)
    - `description`: str
  }

### 2. API Contracts (contracts/)

**CLI Entry Point** (`main.py` with argparse)

```
usage: validation-suite [OPTIONS] COMMAND [ARGS]

Options:
  --config PATH              Load config from YAML/JSON (optional, defaults to .env)
  --log-level {DEBUG,INFO,WARNING,ERROR}  Logging level (default: INFO)
  --help                     Show this message and exit

Commands:
  validate                   Run validation suite
  report                     Generate or view report
```

**validate command**
```
validation-suite validate [OPTIONS]

Options:
  --queries PATH             Path to custom queries JSON (default: predefined set)
  --filter-url TEXT          Filter results by source URL pattern
  --filter-section TEXT      Filter results by section title
  --filter-chunks TEXT       Filter by chunk index range (e.g., "0-100")
  --output PATH              Save report to file (default: stdout + JSON file)
  --format {json,csv}        Report format (default: json)
  --assess-manually          Interactive mode to label relevance
  --dry-run                  Test without calling APIs
  --help
```

**report command**
```
validation-suite report [OPTIONS]

Options:
  --input PATH               Load report from file
  --format {json,csv,html}   Output format (default: json)
  --summary-only             Print summary statistics only
  --help
```

### 3. Quick Start Guide (quickstart.md)

**Installation**
```bash
cd backend
uv sync  # Install validation suite dependencies
```

**Basic Validation Run**
```bash
# Run with predefined queries
uv run python src/main.py validate

# Run with custom queries
uv run python src/main.py validate --queries my_queries.json

# Filter results by chapter
uv run python src/main.py validate --filter-section "Chapter 2"

# Save report to file
uv run python src/main.py validate --output report.json
```

**Understanding the Report**
- `avg_similarity_score`: Average relevance (higher = better); >0.7 generally indicates good retrieval
- `relevant_results_percent`: % of results marked relevant (target: ≥80%)
- `pass_fail`: True if validation passes (≥80% relevant)

**Next Steps**
- Review low-scoring queries in the report
- Check retrieved chunks for relevance (manual_relevance_assessment)
- Update embedding quality or queries based on findings

### Architecture Decisions

**AD-001: Modular Validator Design**
- Separate concerns: embedding, retrieval, filtering, reporting
- Enables independent testing and future enhancements
- Each module <200 lines for maintainability

**AD-002: JSON-First Report Format**
- Primary format for CI/CD integration and programmatic access
- CSV export available for spreadsheet analysis
- All data preserved in JSON for audit trail

**AD-003: No Caching of Query Embeddings**
- Each validation run embeds queries fresh
- Ensures reproducibility (same query + Qdrant state = same results)
- Acceptable latency (<2s per query)

**AD-004: Similarity Threshold at 0.7**
- Based on cosine similarity standard for embedding spaces
- Empirically validated in RAG literature
- Threshold flags unreasonably high scores (>0.95) as potential issues
