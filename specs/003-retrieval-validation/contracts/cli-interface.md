# CLI Interface Contract: Retrieval Validation Suite

**Feature**: 003-retrieval-validation
**Date**: 2025-12-12
**Interface Type**: Command-Line Interface (argparse/Click)
**Target Users**: Developers, QA engineers

---

## Overview

The validation suite is a CLI tool that executes test queries against a Qdrant collection and generates reports on retrieval accuracy. The tool supports predefined query sets, custom query loading, result filtering, and multiple output formats.

**Entry Point**: `python src/main.py` (or `uv run python src/main.py` in development)

---

## Main Commands

### 1. `validate` - Execute Validation Suite

**Purpose**: Execute a validation run against Qdrant.

**Signature**:
```bash
python src/main.py validate [OPTIONS]
```

**Options**:

| Option | Type | Default | Required | Description |
|--------|------|---------|----------|-------------|
| `--queries` | PATH | predefined_queries.json | No | Path to custom query set (JSON file) |
| `--filter-url` | TEXT | (none) | No | Filter results by source URL pattern (regex or substring) |
| `--filter-section` | TEXT | (none) | No | Filter results by section title |
| `--filter-chunks` | TEXT | (none) | No | Filter by chunk index range (e.g., "0-100") |
| `--output` | PATH | validation_report.json | No | Path to save report file |
| `--format` | STRING | json | No | Report format: `json` or `csv` |
| `--top-k` | INT | 5 | No | Number of top results to retrieve per query (1-100) |
| `--assess-manually` | FLAG | False | No | Interactive mode to manually label relevance |
| `--dry-run` | FLAG | False | No | Test without calling APIs (no Cohere/Qdrant calls) |
| `--config` | PATH | .env | No | Path to environment config file |
| `--log-level` | STRING | INFO | No | Logging level: DEBUG, INFO, WARNING, ERROR |
| `--help` | FLAG | - | No | Show help message |

**Return Code**:
- `0`: Success (validation completed, regardless of pass/fail)
- `1`: Fatal error (API unreachable, config missing, malformed input)
- `2`: Invalid arguments

**Output**:

**Stdout** (if `--output` not specified):
```
Validation Suite - Retrieval Accuracy Report
=============================================

Run ID:               run-2025-12-12T10:30:00Z
Timestamp:            2025-12-12 10:30:00 UTC
Total Queries:        10
Queries Executed:     10
Queries Failed:       0

Summary Statistics
------------------
Avg Similarity Score: 0.81
Min Similarity Score: 0.65
Max Similarity Score: 0.92

Relevance Assessment
--------------------
Relevant:             85%
Partially Relevant:   10%
Irrelevant:            5%

Result: PASS (≥80% relevant)
Duration: 23.5 seconds

Report saved to: validation_report.json
```

**File Output**:
- JSON file with complete ValidationReport (see data-model.md)
- CSV file (if `--format csv`) with rows per query/result

---

### 2. `report` - View/Export Report

**Purpose**: Load and view a previously generated report.

**Signature**:
```bash
python src/main.py report [OPTIONS]
```

**Options**:

| Option | Type | Default | Required | Description |
|--------|------|---------|----------|-------------|
| `--input` | PATH | validation_report.json | No | Path to report file to load |
| `--format` | STRING | json | No | Output format: `json`, `csv`, `html`, `summary` |
| `--summary-only` | FLAG | False | No | Print summary statistics only |
| `--sort-by` | STRING | rank | No | Sort results by: rank, similarity, query_id |
| `--filter-assessment` | STRING | (all) | No | Filter results by assessment: relevant, partial, irrelevant |
| `--help` | FLAG | - | No | Show help message |

**Return Code**:
- `0`: Success
- `1`: File not found or malformed
- `2`: Invalid arguments

**Output** (Stdout):

For `--format summary`:
```
Report Summary: run-2025-12-12T10:30:00Z
=========================================
Total Queries: 10
Pass/Fail: PASS

Avg Similarity: 0.81 (min: 0.65, max: 0.92)
Relevant: 85% | Partially: 10% | Irrelevant: 5%
```

For `--format json`:
Full ValidationReport JSON (same as validate output)

For `--format csv`:
CSV with columns: query_id, query_text, rank, similarity_score, source_url, relevance_assessment

For `--format html`:
HTML report with tables and charts (future)

---

## Query File Format

### Predefined Queries (`examples/predefined_queries.json`)

```json
{
  "test_queries": [
    {
      "id": "q1",
      "text": "What is physical AI?",
      "topic": "foundational",
      "difficulty": "easy",
      "expected_chapters": ["01-fundamentals"],
      "notes": "Should return intro to physical AI"
    },
    {
      "id": "q2",
      "text": "How do you configure ROS 2 nodes?",
      "topic": "middleware",
      "difficulty": "medium",
      "expected_chapters": ["03-control-simulation"],
      "notes": "Should cover ROS 2 setup"
    }
  ],
  "metadata": {
    "name": "predefined_set_v1",
    "created_at": "2025-12-12T00:00:00Z",
    "description": "10 sample queries covering major book topics",
    "version": "1.0.0",
    "author": "AI & Physical Robotics Project"
  }
}
```

### Custom Queries

User-provided queries JSON must follow same schema as predefined queries.

**Validation**:
- All queries must have unique `id` and non-empty `text`
- Missing optional fields are allowed (defaults to null)
- Invalid queries logged with error; validation continues with remaining queries

---

## Exit Behaviors & Error Handling

### Success Cases

**Case 1: All queries successful**
```
Exit Code: 0
Stdout: Summary with pass/fail result
Files: validation_report.json created
```

**Case 2: Some queries failed (e.g., Qdrant timeout on 1 of 10)**
```
Exit Code: 0 (suite completed, logged failures)
Stdout: Summary noting 1 failure
Files: Report includes error details for failed query
```

### Error Cases

**Case 3: Cannot connect to Cohere API**
```
Exit Code: 1
Stderr: "Error: Cannot reach Cohere API. Check COHERE_API_KEY and network connection."
Files: None created
```

**Case 4: Qdrant collection does not exist**
```
Exit Code: 1
Stderr: "Error: Qdrant collection 'book_embeddings' not found. Run embedding pipeline first."
Files: None created
```

**Case 5: Invalid query file**
```
Exit Code: 1
Stderr: "Error: Query file 'my_queries.json' is malformed JSON."
Files: None created
```

**Case 6: Invalid arguments**
```
Exit Code: 2
Stderr: "Error: Unrecognized arguments: --invalid-flag"
Files: None created
```

---

## Configuration

Configuration loaded from `.env` file (or `--config` path):

**Required**:
- `COHERE_API_KEY`: API key for Cohere embeddings
- `QDRANT_URL`: Qdrant instance URL (https://...)
- `QDRANT_API_KEY`: Qdrant authentication key

**Optional**:
- `COHERE_MODEL`: Embedding model (default: `embed-3-large`)
- `QDRANT_COLLECTION`: Collection name (default: `book_embeddings`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `SIMILARITY_THRESHOLD`: Relevance threshold (default: `0.7`)

---

## Logging

**Log Format** (JSON):
```json
{
  "timestamp": "2025-12-12T10:30:00Z",
  "level": "INFO",
  "message": "Executing query q1: What is physical AI?",
  "query_id": "q1",
  "execution_time_ms": 1850
}
```

**Log Levels**:
- `DEBUG`: Detailed API calls, embeddings, search results
- `INFO`: Query progress, summary statistics
- `WARNING`: Failed queries, unusual scores (>0.95 or <0.5)
- `ERROR`: Fatal errors, API failures

**Log Output**:
- Stdout: INFO and above
- File: `validation.log` (all levels, JSON format)

---

## Interactive Mode (`--assess-manually`)

When enabled, after validation run, user is prompted to assess each query's relevance:

```
Query q1: What is physical AI?
---
Result 1 (rank 1, score 0.89):
  "Physical AI is the branch of artificial intelligence..."

Relevant? (y/n/p/skip): y
Notes (optional): Accurate definition, good intro

Result 2 (rank 2, score 0.84):
  "Embodied intelligence refers to..."

Relevant? (y/n/p/skip): y
Notes: Good supporting context

[Continue for all results...]
```

Assessment options:
- `y`: Relevant
- `n`: Irrelevant
- `p`: Partially relevant
- `skip`: Leave unassessed (use in report as null)

Final report includes user assessments in `relevance_assessment` and `relevance_notes`.

---

## Examples

### Example 1: Basic validation run

```bash
cd backend
uv run python src/main.py validate
```

Runs predefined queries, saves report to `validation_report.json`, prints summary.

### Example 2: Custom queries, save as CSV

```bash
uv run python src/main.py validate \
  --queries my_queries.json \
  --format csv \
  --output my_report.csv
```

### Example 3: Filter by section, interactive assessment

```bash
uv run python src/main.py validate \
  --filter-section "Control Systems" \
  --assess-manually
```

### Example 4: Dry-run (no API calls)

```bash
uv run python src/main.py validate --dry-run
```

Tests query loading, filtering, report generation without hitting Cohere/Qdrant.

### Example 5: View existing report

```bash
uv run python src/main.py report \
  --input validation_report.json \
  --summary-only
```

---

## Future Enhancements (Out of Scope for MVP)

- `--stream` flag for real-time streaming results
- `--compare` to compare two validation runs
- `--export-to-html` for formatted HTML reports
- `--webhook` to post results to external service
- `--threshold-override` to use different similarity threshold
- API endpoint mode (REST API instead of CLI)
