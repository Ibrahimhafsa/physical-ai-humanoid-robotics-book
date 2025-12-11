# Phase 1 Data Model: Book Embedding Pipeline

**Date**: 2025-12-12
**Feature**: 002-book-embeddings
**Status**: Complete

## Entity Overview

The Book Embedding Pipeline operates on four core entities: **Page**, **Chunk**, **Vector**, and **IngestionLog**. These represent the data flow from discovery to storage.

---

## Entity: Page

**Definition**: A single Docusaurus page URL with fetched HTML content.

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `url` | string | Yes | Full URL to the page (e.g., `https://example.com/docs/intro`) | Must be valid HTTP(S) URL; unique |
| `title` | string | Yes | Page title extracted from `<title>` or `<h1>` | Non-empty; max 255 chars |
| `html_content` | string | Yes | Raw HTML fetched from URL | Non-empty; valid HTML structure |
| `status_code` | int | Yes | HTTP response code (200, 404, 500, etc.) | Must be valid HTTP status |
| `fetched_at` | timestamp | Yes | ISO 8601 timestamp when page was fetched | Recent (within pipeline run) |
| `fetch_error` | string | Optional | Error message if fetch failed (e.g., "timeout", "404") | Human-readable; logged |

**Relationships**:
- One Page → Multiple Chunks (1:N)
- One Page → One or more Vectors (via its Chunks)

**State Transitions**:
1. **Discovered** → URL added to crawl queue
2. **Fetching** → HTTP GET in progress
3. **Fetched** → HTML content received; `status_code` = 200
4. **Failed** → Fetch error; `fetch_error` populated; continue with next page
5. **Extracted** → Chunks generated from HTML; ready for embedding

**Validation Rules**:
- `url` must not be empty or null
- `status_code` = 200 required to proceed to Chunk extraction
- `html_content` must contain at least one `<article>`, `<main>`, or `<body>` tag
- `fetched_at` must be within 1 hour of pipeline start (freshness check)

**Storage**: In-memory during pipeline; serialized in ingestion log

---

## Entity: Chunk

**Definition**: A semantic unit of text extracted from a Page, ready for embedding.

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `chunk_id` | string | Yes | Unique identifier (SHA256 hash of normalized text) | 64 hex chars; unique per pipeline run |
| `url` | string | Yes | Parent page URL | Must match a Page.url |
| `text` | string | Yes | Clean, normalized text content | Non-empty; max 8192 chars (≤512 tokens) |
| `section_title` | string | Optional | Section/heading context (e.g., "Installation") | Max 255 chars |
| `chunk_index` | int | Yes | Position within page (0-indexed) | Non-negative |
| `token_count` | int | Yes | Estimated token count (word count × 1.3) | >0; ≤512 |
| `created_at` | timestamp | Yes | ISO 8601 timestamp when chunk was created | Within pipeline run |
| `extraction_method` | string | Yes | How text was extracted (e.g., "semantic_paragraph", "fallback_html") | Enum: "semantic_paragraph", "fallback_html", "fallback_raw" |

**Relationships**:
- Many Chunks ← One Page (N:1)
- One Chunk → One Vector (1:1, after embedding)

**State Transitions**:
1. **Extracted** → Chunk created from HTML; text not yet embedded
2. **Deduplicated** → Content hash checked; marked as duplicate (skip embedding)
3. **Embedding** → Cohere API call in progress
4. **Embedded** → Vector generated; ready for storage
5. **Stored** → Vector + metadata upserted to Qdrant
6. **Failed** → Extraction or embedding error; logged; skip

**Validation Rules**:
- `chunk_id` = SHA256(normalized `text`) → immutable, unique per content
- `text` must be non-empty after whitespace normalization
- `text` length ≤ 8192 chars (conservative limit for Cohere model)
- `token_count` = word_count(text) × 1.3 (estimated; capped at 512)
- `url` must reference a valid Page
- `chunk_index` must be sequential per page (0, 1, 2, ...)

**Content Normalization Rules** (for `text`):
- Remove leading/trailing whitespace
- Collapse multiple spaces to single space
- Remove control characters (except newlines preserved for readability)
- Preserve original line breaks within code blocks
- Preserve markdown formatting (bold, italic, links) if present

**Deduplication**:
- Chunks with identical `chunk_id` are duplicates (same content)
- Skip embedding; log as "deduplicated"
- Update metadata if chunk appears in new URL context

---

## Entity: Vector

**Definition**: A 4096-dimensional embedding of a Chunk, stored in Qdrant Cloud.

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `vector_id` | string | Yes | Unique ID for Qdrant point (same as `chunk_id`) | 64 hex chars; UUID-like |
| `vector` | array[float32] | Yes | 4096-dimensional embedding from Cohere | Exactly 4096 dimensions; L2-normalized |
| `url` | string | Yes | Source page URL (metadata) | Must match original Page.url |
| `chunk_id` | string | Yes | Source chunk hash (metadata) | Must match Chunk.chunk_id |
| `text` | string | Yes | Original text content (metadata for retrieval) | Exact copy of Chunk.text |
| `section_title` | string | Optional | Section context (metadata) | Max 255 chars |
| `chunk_index` | int | Yes | Position within page (metadata) | Non-negative |
| `token_count` | int | Yes | Token count of original text (metadata) | ≤512 |
| `embedded_at` | timestamp | Yes | ISO 8601 timestamp when embedding was generated | Within pipeline run |
| `embedding_model` | string | Yes | Cohere model used (e.g., "embed-3-large") | Fixed: "embed-3-large" |

**Relationships**:
- One Vector ← One Chunk (1:1)
- Vector stored in Qdrant with metadata payload

**Qdrant Storage Structure**:
```json
{
  "id": "vector_id (chunk_id)",
  "vector": [float, float, ..., float],  // 4096 dimensions
  "payload": {
    "url": "https://example.com/docs/intro",
    "chunk_id": "abc123...",
    "text": "Full text of chunk...",
    "section_title": "Installation",
    "chunk_index": 0,
    "token_count": 128,
    "embedded_at": "2025-12-12T10:30:00Z",
    "embedding_model": "embed-3-large"
  }
}
```

**Validation Rules**:
- `vector` must have exactly 4096 elements
- All vector elements must be valid float32 (within ±1e38)
- `vector` should be L2-normalized by Cohere (automatic)
- `vector_id` must be unique in Qdrant collection
- Duplicate `vector_id` triggers upsert (update existing, no duplicate insertion)

**Vector Search**:
- Query vector (from user question) compared to stored vectors via cosine similarity
- Similarity score: 0.0 (orthogonal) to 1.0 (identical)
- Typical retrieval threshold: similarity ≥ 0.7 for relevant results

---

## Entity: IngestionLog

**Definition**: Summary statistics and details of a pipeline run, stored as JSON file.

**Structure**:

```json
{
  "pipeline_metadata": {
    "run_id": "run-20251212-103000",
    "started_at": "2025-12-12T10:30:00Z",
    "completed_at": "2025-12-12T11:15:30Z",
    "duration_seconds": 2730,
    "status": "success"
  },
  "configuration": {
    "book_root_url": "https://example.com",
    "cohere_model": "embed-3-large",
    "qdrant_collection": "book_embeddings"
  },
  "summary": {
    "urls_discovered": 150,
    "urls_fetched": 150,
    "urls_failed": 0,
    "chunks_created": 1250,
    "chunks_deduplicated": 5,
    "chunks_embedded": 1245,
    "vectors_stored": 1245,
    "duplicate_skipped": 5
  },
  "performance": {
    "crawl_time_seconds": 45,
    "extraction_time_seconds": 120,
    "embedding_time_seconds": 1500,
    "storage_time_seconds": 60,
    "total_time_seconds": 2730
  },
  "api_usage": {
    "cohere_api_calls": 156,
    "cohere_tokens_used": 320000,
    "cohere_quota_remaining": 680000,
    "qdrant_upserts": 156,
    "qdrant_collection_size_mb": 21.5
  },
  "errors": [
    {
      "url": "https://example.com/docs/broken",
      "error_type": "extraction_failed",
      "message": "No article content found; fell back to raw HTML",
      "timestamp": "2025-12-12T10:35:15Z"
    }
  ],
  "pages": [
    {
      "url": "https://example.com/docs/intro",
      "title": "Introduction",
      "status": "success",
      "chunks_created": 5,
      "chunks_embedded": 5,
      "fetch_time_ms": 250,
      "extraction_time_ms": 50,
      "embedding_time_ms": 800
    }
  ]
}
```

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `pipeline_metadata` | object | Run ID, timestamps, overall status |
| `configuration` | object | Book URL, model, collection name (for reproducibility) |
| `summary` | object | Total counts: URLs, chunks, vectors, deduplications, failures |
| `performance` | object | Timing breakdown (crawl, extraction, embedding, storage) |
| `api_usage` | object | Cohere calls/tokens, Qdrant upserts, storage size |
| `errors` | array | Detailed error logs (one entry per failure) |
| `pages` | array | Per-page statistics (for debugging and validation) |

**Validation Rules**:
- `run_id` unique (timestamp-based)
- `completed_at` ≥ `started_at`
- `summary` counts must be mutually consistent (e.g., `chunks_created` = `chunks_deduplicated` + `chunks_embedded`)
- `vectors_stored` must match Qdrant collection point count (±0.1% variance acceptable)
- All timestamps in ISO 8601 format
- All numeric fields ≥ 0

**Reconciliation Checks** (for validation):
1. `urls_fetched` = `urls_discovered` - `urls_failed` (or logged errors)
2. `chunks_embedded` + `chunks_deduplicated` ≤ `chunks_created`
3. `vectors_stored` = `chunks_embedded` (1:1 mapping)
4. `cohere_api_calls` ≤ ceil(`chunks_embedded` / 8) (batch size assumption)
5. Log total time ≈ sum of performance breakdown times

---

## Data Flow Diagram

```
Page Discovery (sitemap)
    ↓
Page Fetching (HTTP GET)
    ├─ Success → Page.status_code = 200
    └─ Failure → Page.fetch_error logged; continue
    ↓
Text Extraction (BeautifulSoup4)
    ├─ Success → Chunks created with text
    └─ Failure → Fallback to raw HTML; log extraction_method
    ↓
Deduplication Check (SHA256 hash)
    ├─ New chunk → Proceed to embedding
    └─ Duplicate → Skip embedding; log chunk_id as deduplicated
    ↓
Cohere Embedding (batch mode, max 8 chunks/call)
    ├─ Success → Vector generated (4096-D)
    └─ Failure → Retry with exponential backoff (max 3 attempts); log error
    ↓
Qdrant Storage (upsert vectors + metadata)
    ├─ Success → Vector stored with payload
    └─ Failure → Log error; retry or manual recovery via checkpoint
    ↓
IngestionLog Generation
    └─ Summarize: URLs, chunks, vectors, timings, API usage, errors
```

---

## Constraints & Assumptions

**Entity Constraints**:
- Page.url must be unique per pipeline run (no duplicate URLs crawled)
- Chunk.chunk_id must be immutable (SHA256 of normalized text; content determines ID)
- Vector.vector must have exactly 4096 dimensions (Cohere embed-3-large requirement)
- IngestionLog must be generated after all vectors stored (final reconciliation)

**Data Consistency**:
- All timestamps in UTC; ISO 8601 format
- Text encoding: UTF-8 (no BOM)
- Floating-point precision: float32 for vectors (4 bytes each)
- No null values in mandatory fields; optional fields may be null

**Storage Limits**:
- Page.html_content: max ~1MB per page (typical Docusaurus pages: 100KB)
- Chunk.text: max 8192 chars (conservative; typical: 500–2000 chars)
- Vector storage: 17KB per vector (4096 float32 + metadata)
- IngestionLog: typically <1MB for books with <10k chunks

---

## Index & Query Patterns

**Qdrant Collection Configuration**:
- Vector size: 4096 (Cohere embed-3-large)
- Distance metric: Cosine similarity
- Indexing: HNSW (Hierarchical Navigable Small World) for fast approximate nearest neighbor search

**Query Patterns** (for retrieval-augmented chatbot):
1. **Similarity Search**: Given user question embedding, find top-K similar chunks
   ```sql
   SELECT chunk_id, url, text, similarity_score
   FROM vectors
   WHERE cosine_similarity(user_query_vector, vector) > 0.7
   ORDER BY similarity_score DESC
   LIMIT 5
   ```

2. **URL Filter**: Retrieve chunks from specific page
   ```sql
   SELECT * FROM vectors WHERE url = "..."
   ```

3. **Full Collection Scan**: Validate vector count, metadata
   ```sql
   SELECT COUNT(*), AVG(token_count) FROM vectors
   ```

---

## Next Steps

- **Phase 2 (Tasks)**: Generate detailed tasks for implementing each entity's CRUD operations
- **Implementation**: Code contracts in `contracts/embeddings.openapi.yaml`
- **Testing**: Unit tests for entity validation; integration tests for data flow
