# Data Model: Retrieval Pipeline Validation

**Feature**: 003-retrieval-validation
**Date**: 2025-12-12
**Purpose**: Define entities, relationships, and validation rules for the validation suite

## Entities

### TestQuery

Represents a single query to validate against the Qdrant collection.

```python
@dataclass
class TestQuery:
    id: str                           # Unique identifier (e.g., "q1", "q2")
    text: str                         # Query string (e.g., "What is physical AI?")
    topic: Optional[str] = None       # Topic category (e.g., "foundational", "middleware")
    difficulty: Optional[str] = None  # Difficulty level: "easy", "medium", "hard"
    expected_chapters: Optional[List[str]] = None  # Chapter slugs where answer should appear
    notes: Optional[str] = None       # Metadata, hints for manual review
```

**Validation Rules**:
- `id`: Must be non-empty, alphanumeric (a-zA-Z0-9_-), unique within query set
- `text`: Must be non-empty, ≤500 characters, valid UTF-8
- `topic`: If provided, must be one of predefined topic categories
- `difficulty`: If provided, must be one of: "easy", "medium", "hard"
- `expected_chapters`: If provided, must be list of valid chapter slugs
- `notes`: If provided, must be ≤1000 characters

**Source**: User-provided JSON file or predefined queries.json

---

### RetrievalResult

Represents a single retrieved chunk (top-K result) from Qdrant.

```python
@dataclass
class RetrievalResult:
    rank: int                              # Position in results (1-K)
    similarity_score: float                # Cosine similarity (0.0-1.0)
    chunk_id: str                          # Unique chunk ID from Qdrant
    source_url: str                        # Full URL to book page
    section_title: str                     # Chapter/section name
    text_excerpt: str                      # First 200 chars of chunk
    relevance_assessment: Optional[str]    # "relevant", "partially_relevant", "irrelevant", null
    relevance_notes: Optional[str]         # Manual assessment notes
```

**Validation Rules**:
- `rank`: Must be positive integer, ≥1, ≤K
- `similarity_score`: Must be float in [0.0, 1.0]
  - Flag if >0.95 (potential embedding quality issue)
  - Flag if <0.5 (potentially low-quality match)
- `chunk_id`: Must match chunk ID from Qdrant metadata
- `source_url`: Must be valid HTTPS URL
- `section_title`: Non-empty string
- `text_excerpt`: Non-empty, ≤500 chars
- `relevance_assessment`: Must be one of: "relevant", "partially_relevant", "irrelevant", or null
- `relevance_notes`: If provided, ≤500 characters

**Source**: Qdrant similarity search results + optional manual assessment

---

### ValidationResult

Represents results for a single query (success or failure).

```python
@dataclass
class ValidationResult:
    query_id: str                           # Reference to TestQuery.id
    query_text: str                         # Query string (cached)
    retrieved_chunks: int                   # Count of results returned (≤K)
    results: List[RetrievalResult]          # Top-K retrieved chunks
    error: Optional[str]                    # Error message if query failed
    execution_time_ms: float                # Time to embed + search (milliseconds)
```

**Validation Rules**:
- `query_id`: Must reference a valid TestQuery.id
- `query_text`: Must match original query text
- `retrieved_chunks`: Must equal len(results)
- `results`: List of RetrievalResult objects
  - If `error` is not null, results must be empty
  - If `error` is null, results must be non-empty (or logged as "no relevant results")
- `error`: If present, must be non-empty string describing the error
- `execution_time_ms`: Must be non-negative float

**State Transitions**:
- Initial: created with query_id, query_text
- In-Progress: embedding query, searching Qdrant
- Success: populated with results and execution_time_ms
- Failure: populated with error message

**Source**: Computed during validation run (one per TestQuery)

---

### ValidationReport

Complete report from a validation run.

```python
@dataclass
class ValidationReport:
    validation_id: str                      # Run ID (e.g., "run-2025-12-12T10:30:00Z")
    timestamp: str                          # ISO 8601 timestamp
    total_queries: int                      # Total queries in set
    queries_executed: int                   # Queries that ran (success or failure)
    queries_failed: int                     # Queries with errors
    results: List[ValidationResult]         # Results for each query
    summary: SummaryStats                   # Aggregated statistics
    filters_applied: Dict[str, Any]         # Filters used (url, section, chunks)
    duration_seconds: float                 # Total run duration
```

**Nested: SummaryStats**

```python
@dataclass
class SummaryStats:
    avg_similarity_score: float             # Mean of all similarity scores
    min_similarity_score: float             # Minimum similarity score
    max_similarity_score: float             # Maximum similarity score
    relevant_results_percent: float         # % marked "relevant" (0-100)
    partially_relevant_percent: float       # % marked "partially_relevant" (0-100)
    irrelevant_percent: float               # % marked "irrelevant" (0-100)
    pass_fail: bool                         # True if ≥80% relevant
```

**Validation Rules**:
- `validation_id`: Format "run-YYYY-MM-DDTHH:MM:SSZ", unique per run
- `timestamp`: Valid ISO 8601 datetime
- `total_queries`: Must be ≥0
- `queries_executed`: Must be ≤total_queries
- `queries_failed`: Must be ≤queries_executed
- `results`: List with len(results) == queries_executed
- `summary.relevant_results_percent + partially_relevant_percent + irrelevant_percent ≤ 100` (due to null assessments)
- `summary.pass_fail`: True iff `relevant_results_percent ≥ 80`
- `filters_applied`: Dict with optional keys: "url", "section", "chunk_index_range"
- `duration_seconds`: Non-negative float

**Source**: Generated at end of validation run

---

### QuerySet

Container for loading predefined or custom query sets.

```python
@dataclass
class QuerySet:
    test_queries: List[TestQuery]           # Array of queries
    metadata: QuerySetMetadata              # Metadata about the set
```

**Nested: QuerySetMetadata**

```python
@dataclass
class QuerySetMetadata:
    name: str                               # Human-readable name
    created_at: str                         # ISO 8601 creation timestamp
    description: Optional[str] = None       # Description of the query set
    version: Optional[str] = None           # Version string (e.g., "1.0.0")
    author: Optional[str] = None            # Author/creator
```

**Validation Rules**:
- `test_queries`: Must be non-empty list of unique TestQuery objects (no duplicate IDs)
- `metadata.name`: Non-empty string, ≤100 chars
- `metadata.created_at`: Valid ISO 8601 datetime
- `metadata.description`: If provided, ≤500 chars
- `metadata.version`: If provided, valid semantic version (e.g., "1.0.0")
- `metadata.author`: If provided, ≤100 chars

**Source**: JSON file (predefined_queries.json or user-provided)

---

## Relationships

```
QuerySet
├── test_queries: List[TestQuery]
│   └── (each TestQuery processed independently)
│
ValidationReport
├── results: List[ValidationResult]
│   └── results[i].results: List[RetrievalResult]
│       (for each retrieved chunk)
│
└── summary: SummaryStats
    └── (aggregated from all ValidationResult)
```

**Key Relationships**:
1. **TestQuery → ValidationResult**: One-to-one (after validation run)
2. **ValidationResult → RetrievalResult**: One-to-many (K results per query)
3. **RetrievalResult → Qdrant Metadata**: Reference (chunk_id links back to Qdrant vector metadata)

---

## Validation Constraints

### Query-Time Validation

When loading TestQuery:
- Reject queries with missing `id` or `text`
- Reject queries with `text` length >500 or <3 characters
- Warn on duplicate IDs
- Skip malformed query entries with detailed error logging

### Result-Time Validation

When recording RetrievalResult:
- Reject if similarity_score outside [0.0, 1.0]
- Validate chunk_id matches Qdrant response
- Validate source_url is HTTPS URL
- Warn if similarity >0.95 (potential embedding issue)
- Warn if similarity <0.5 (low-quality match)

When computing ValidationReport:
- Require total_queries ≥ queries_executed - queries_failed
- Require summary percentages sum to ≤100% (due to null assessments)
- Require pass_fail logic: (relevant_percent ≥ 80) → True

### Error Handling

**Recoverable Errors** (logged, validation continues):
- Single query embedding fails → log, mark result as error, continue
- Single Qdrant search times out → log, mark result as error, continue
- Malformed custom query → skip with warning, continue

**Fatal Errors** (halt validation):
- Cannot connect to Cohere API
- Cannot connect to Qdrant instance
- Invalid .env configuration
- Custom query file not found or malformed JSON

---

## Example: Complete Data Flow

**Input**: TestQuery
```json
{
  "id": "q1",
  "text": "What is physical AI?",
  "topic": "foundational",
  "difficulty": "easy",
  "expected_chapters": ["01-fundamentals"]
}
```

**Processing**:
1. Embed query via Cohere API → 4096-D vector
2. Search Qdrant for top-5 similar chunks → 5 RetrievalResult objects
3. Record execution time

**Output**: ValidationResult
```json
{
  "query_id": "q1",
  "query_text": "What is physical AI?",
  "retrieved_chunks": 5,
  "results": [
    {
      "rank": 1,
      "similarity_score": 0.89,
      "chunk_id": "abc123",
      "source_url": "https://book.com/docs/01-fundamentals/physical-ai",
      "section_title": "Introduction to Physical AI",
      "text_excerpt": "Physical AI is the branch of artificial intelligence...",
      "relevance_assessment": "relevant",
      "relevance_notes": "Accurate definition"
    },
    ...
  ],
  "error": null,
  "execution_time_ms": 1850
}
```

**Aggregated**: ValidationReport
```json
{
  "validation_id": "run-2025-12-12T10:30:00Z",
  "timestamp": "2025-12-12T10:30:00Z",
  "total_queries": 10,
  "queries_executed": 10,
  "queries_failed": 0,
  "results": [...],
  "summary": {
    "avg_similarity_score": 0.81,
    "min_similarity_score": 0.65,
    "max_similarity_score": 0.92,
    "relevant_results_percent": 85,
    "partially_relevant_percent": 10,
    "irrelevant_percent": 5,
    "pass_fail": true
  },
  "filters_applied": {},
  "duration_seconds": 23.5
}
```

---

## Testing Considerations

**Unit Test Data**:
- Mock TestQuery with valid + edge case values
- Mock RetrievalResult with boundary scores (0.0, 0.7, 1.0, >0.95)
- Mock ValidationReport with 100% relevant, 50% relevant, 0% relevant scenarios

**Integration Test Data**:
- End-to-end with mocked Cohere/Qdrant APIs
- Verify error handling (API timeouts, malformed responses)
- Verify report generation matches expected format

---

## Schema Evolution

**Current Version**: 1.0.0

**Future Compatibility**:
- Add optional fields to TestQuery, RetrievalResult (backward compatible)
- Add new SummaryStats fields (computed dynamically)
- Never remove required fields; use deprecation patterns

**Migration Path** (if schema changes):
- Version field in QuerySetMetadata + ValidationReport
- Migration scripts to convert old reports to new format
- Document changes in CHANGELOG.md
