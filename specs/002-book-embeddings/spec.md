# Feature Specification: Book Embedding Pipeline

**Feature Branch**: `002-book-embeddings`
**Created**: 2025-12-12
**Status**: Draft
**Input**: Build fully automated pipeline that fetches deployed book URLs, extracts clean text, generates embeddings using Cohere, and stores them in Qdrant for RAG chatbot usage.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Embedded Book for RAG Chatbot (Priority: P1)

As a chatbot developer, I want to automatically crawl the deployed Docusaurus book, extract all content as text chunks, generate embeddings via Cohere, and store vectors in Qdrant so that the chatbot can retrieve relevant content to answer user questions.

**Why this priority**: This is the core outcome—without embeddings stored in Qdrant, the RAG chatbot cannot function. This is the MVP for the entire feature.

**Independent Test**: The pipeline runs locally, crawls all public book URLs, processes them into chunks with embeddings, stores them in Qdrant Cloud, and produces a log showing successful ingestion of all content.

**Acceptance Scenarios**:

1. **Given** a published Docusaurus book at a public URL, **When** the pipeline runs, **Then** all pages are crawled and indexed in Qdrant
2. **Given** extracted text chunks, **When** embeddings are generated, **Then** each chunk has a valid 4096-dimensional Cohere embedding
3. **Given** stored vectors in Qdrant, **When** a similarity search is performed, **Then** relevant content is retrieved with proper metadata (URL, chunk_id, original text)

---

### User Story 2 - Verify Data Quality & Prevent Duplicates (Priority: P2)

As a pipeline operator, I want to ensure the embedding log shows exactly what was ingested (URL count, chunk count, timestamps) and that no duplicate vectors are stored, so I can trust the pipeline output and debug any issues.

**Why this priority**: Data quality validation is critical for RAG reliability. Without verification, the chatbot may have gaps or redundant content.

**Independent Test**: The pipeline produces a verifiable JSON or CSV log listing every URL processed, chunk count per URL, total vectors stored, and timestamps. No duplicate embeddings exist in Qdrant for the same content.

**Acceptance Scenarios**:

1. **Given** a completed pipeline run, **When** the embedding log is reviewed, **Then** it lists all crawled URLs, chunk counts, and processing timestamps
2. **Given** duplicate content across multiple URLs, **When** the pipeline processes them, **Then** only one instance is stored (duplicates detected and skipped)
3. **Given** empty or whitespace-only text chunks, **When** processing, **Then** they are excluded from embedding and logged as skipped

---

### User Story 3 - Reproduce Embeddings Locally (Priority: P3)

As a developer, I want to run the entire pipeline with a single Python script or FastAPI job locally (with API keys in environment variables) so that I can regenerate embeddings if needed without manual intervention.

**Why this priority**: Reproducibility ensures the pipeline can be re-run during updates to the book or troubleshooting. This enables CI/CD integration in the future.

**Independent Test**: The pipeline script accepts configuration (book URL, Cohere API key, Qdrant endpoint) via environment variables or config file, runs end-to-end locally, and completes with a success/failure status.

**Acceptance Scenarios**:

1. **Given** a local machine with Python and environment variables set (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY), **When** the script runs, **Then** the pipeline executes without manual intervention
2. **Given** an unfinished pipeline (e.g., network interruption), **When** the script runs again, **Then** it processes new/updated content without re-processing successfully stored vectors
3. **Given** a config file with all parameters, **When** the script reads it, **Then** it uses those values and completes successfully

---

### Edge Cases

- What happens if a page fails to load or returns an error during crawling? → Log the failure, continue with other pages
- What happens if the Cohere API rate limit is exceeded? → Implement exponential backoff and retry; log throttling events
- What happens if text extraction fails for a specific page format? → Fall back to raw HTML text, log the issue, continue
- What happens if duplicate content already exists in Qdrant before re-run? → Skip re-ingesting; update metadata if needed
- What happens if the Qdrant connection drops mid-ingestion? → Persist progress state and resume from the last successful chunk

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST crawl all public URLs from the deployed Docusaurus book and discover all pages (including nested navigation)
- **FR-002**: System MUST extract clean, structured text from each page, removing HTML markup, navigation elements, and boilerplate
- **FR-003**: System MUST split extracted text into semantic chunks (paragraphs or sections) with a maximum size limit to fit Cohere's embedding model
- **FR-004**: System MUST call Cohere's embed endpoint to generate embeddings for each chunk (embedding dimension: 4096 for Cohere v3 embed model)
- **FR-005**: System MUST store each vector with metadata in Qdrant Cloud: `{url, chunk_id, text, vector}`
- **FR-006**: System MUST prevent duplicate vectors by comparing content hash or checking for existing embeddings before storage
- **FR-007**: System MUST generate a final log (JSON or CSV) recording all URLs processed, chunk count, total vectors stored, and timestamps
- **FR-008**: System MUST handle failures gracefully: log errors, retry with backoff for transient failures, skip failed pages and continue
- **FR-009**: System MUST accept configuration via environment variables (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, BOOK_ROOT_URL) or config file
- **FR-010**: System MUST track and skip pages that have already been successfully embedded (idempotent behavior)

### Key Entities

- **Page**: A single Docusaurus page with a URL, title, and HTML content
- **Chunk**: A semantic unit of text (paragraph or section) extracted from a page; has chunk_id, text, and parent URL
- **Vector**: A 4096-dimensional embedding generated by Cohere for a chunk; includes chunk metadata and timestamp
- **Embedding Log**: A structured record (JSON/CSV) of all processed pages and chunks with counts and timestamps

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All public URLs of the deployed book are crawled and processed (100% of discovered pages)
- **SC-002**: Text extraction succeeds for at least 95% of pages; failures are logged with reasons
- **SC-003**: Each chunk generates a valid Cohere embedding without errors
- **SC-004**: All vectors are stored in Qdrant Cloud with complete metadata (url, chunk_id, text, vector)
- **SC-005**: Zero duplicate vectors exist for identical content; deduplication success rate ≥ 99%
- **SC-006**: The pipeline completes end-to-end in under 1 hour for a book with up to 500 pages
- **SC-007**: The embedding log is accurate: total logged vectors match count in Qdrant (within 0.1% variance)
- **SC-008**: The pipeline can be re-run locally and idempotently (no errors on second run for same book state)
- **SC-009**: A developer can run the pipeline with a single command and environment variables (no manual setup beyond keys)

## Assumptions

- The Docusaurus book is publicly deployed and accessible without authentication
- Cohere API key has sufficient quota (Free Tier or higher) for the book's content volume
- Qdrant Cloud Free Tier has sufficient storage for the embedded vectors (estimated based on chunk count)
- Text extraction via libraries like `BeautifulSoup` or `Playwright` is sufficient (no JavaScript rendering complexities for dynamic content)
- Pages use standard HTML structures (semantic tags, paragraphs); unusual page formats may require custom handlers
- Network connectivity is stable; temporary failures are handled with retry logic
- The book structure (URLs, naming) remains stable during pipeline execution

## Non-Functional Requirements

### Performance
- Crawling + extraction: ≤ 1 second per page on average
- Embedding generation: ≤ 2 seconds per chunk (including API latency)
- Total pipeline time: ≤ 1 hour for 500 pages with 5000 chunks

### Reliability
- Retry transient failures (network, rate limits) with exponential backoff (max 3 attempts)
- Graceful handling of non-transient errors (invalid content, API errors); log and continue
- Idempotent re-runs: no duplicate ingestion or data loss on subsequent runs

### Security
- API keys (Cohere, Qdrant) stored in environment variables, never hardcoded or logged
- Extracted text and vectors stored only in Qdrant; no local caching of sensitive data beyond temporary processing
- HTTPS used for all external API calls

### Scalability
- Support books with 100–1000 pages and 10,000+ chunks
- Batch embedding requests to Cohere when possible to reduce API calls
- Stream results to Qdrant to avoid memory overload

## Out of Scope

- UI or interactive dashboard
- Chatbot logic or retrieval augmentation
- Agents or autonomous systems
- Frontend integration or embedding browser
- Retrieval tuning (e.g., similarity threshold tuning)
- Alternative embedding models (only Cohere)
- Multi-language support or translation
- Fine-tuning embeddings for specific domains
- Automated re-indexing on book updates (one-off pipeline; manual re-run as needed)

## Success Validation Plan

1. **Crawl Validation**: Verify all public URLs are discovered by comparing against the Docusaurus sitemap or manual page listing
2. **Extraction Validation**: Sample 10–20 pages and manually verify text is clean and complete
3. **Embedding Validation**: Query Qdrant for a known chunk and verify the returned vector is valid and metadata is correct
4. **Deduplication Validation**: Identify pages with duplicate content (e.g., "Home" duplicated in nav) and verify only one vector exists
5. **Log Validation**: Compare embedding log totals against actual count in Qdrant and ensure timestamps are accurate
6. **End-to-End Test**: Run the full pipeline on a test environment and verify all steps succeed with a final success status
