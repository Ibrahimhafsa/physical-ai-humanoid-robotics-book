# Feature Specification: Retrieval Pipeline Validation for RAG System

**Feature Branch**: `003-retrieval-validation`
**Created**: 2025-12-12
**Status**: Draft
**Input**: Build validation suite to ensure accurate vector retrieval from Qdrant before integrating with RAG agents; focus on debugging and quality assurance for embedding-based search.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate Query Retrieval Accuracy (Priority: P1)

As a developer integrating RAG embeddings, I want to execute sample queries against the embedded book content and verify that retrieved chunks are relevant and contextually accurate, so I can confidently integrate these results into my chatbot agent.

**Why this priority**: This is the core validation—if retrieval accuracy is not verified before agent integration, the entire RAG system will produce incorrect or irrelevant answers. This is the MVP for the validation suite.

**Independent Test**: Run 5–10 predefined test queries against the Qdrant collection; for each query, retrieve top-K results, manually verify that retrieved text is relevant to the query, and check that similarity scores are reasonable (≥0.7).

**Acceptance Scenarios**:

1. **Given** a test query ("What is physical AI?"), **When** the retrieval system searches Qdrant, **Then** the top 3 results contain relevant content about physical AI/embodied intelligence with similarity scores ≥0.7
2. **Given** a sample query about a specific chapter ("Kinematics and dynamics"), **When** the system retrieves chunks, **Then** returned text matches the original book content and context is preserved
3. **Given** multiple test queries from different book sections, **When** all are executed, **Then** at least 80% of queries return relevant results (as determined by manual review)

---

### User Story 2 - Generate Debug Report with Metrics (Priority: P2)

As a developer, I want a detailed debugging report that shows retrieval quality metrics (similarity scores, chunk sources, text excerpts) for each test query, so I can identify gaps or issues in the embedding quality before deploying the RAG system.

**Why this priority**: Quality metrics and detailed debugging output are essential for identifying and fixing embedding/retrieval issues. Without this report, problems are harder to diagnose.

**Independent Test**: Run validation queries and generate a JSON/CSV report listing: query text, retrieved chunk count, similarity score ranges, chunk sources (URLs), text snippets, and manual relevance assessment for each query.

**Acceptance Scenarios**:

1. **Given** a completed validation run, **When** the debug report is reviewed, **Then** it includes query text, top-K results, similarity scores, and source URLs for each query
2. **Given** multiple test queries with varying relevance, **When** the report is generated, **Then** it flags low-confidence retrievals (similarity < 0.7) and notes potential embedding gaps
3. **Given** a report output file, **When** a developer reviews it, **Then** they can identify which chunks/pages have weak embeddings and need re-processing

---

### User Story 3 - Support Custom Query Sets and Filtering (Priority: P3)

As a power user or QA engineer, I want to define custom test query sets, filter results by source URL or section, and compare retrieval quality across different queries or time periods, so I can systematically validate the embedding quality for specific book sections.

**Why this priority**: Custom queries and filtering enable targeted testing and iterative refinement. This supports advanced validation workflows and regression testing.

**Independent Test**: Create custom query sets in a JSON file; run validation with filters (e.g., "only retrieve from Chapter 2", "exclude navigation pages"); generate comparative reports showing retrieval metrics by section/page.

**Acceptance Scenarios**:

1. **Given** a custom query set file, **When** the validation system loads it, **Then** all custom queries are executed with proper error handling
2. **Given** URL/section filters, **When** applied during retrieval, **Then** results are correctly filtered and report shows only relevant chunks
3. **Given** multiple validation runs, **When** compared, **Then** users can see trends in retrieval quality and identify degradation or improvement

---

### Edge Cases

- What happens if a query returns no results (similarity < 0.5)? → Log as "no relevant results found", flag in debug report
- What happens if a chunk's text has been modified after initial embedding? → Detect mismatch, log as "stale embedding"
- What happens if the Qdrant collection is empty? → Graceful error, clear message about missing embeddings
- What happens if a test query is malformed (empty, too short)? → Validate input, skip with warning in report
- What happens if similarity scores seem unreasonably high (all > 0.95)? → Flag potential issue (embedding space quality, query diversity)

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST execute test queries against the Qdrant collection and retrieve top-K chunks (K configurable, default 5)
- **FR-002**: System MUST embed test queries using Cohere embeddings API (same model as original embeddings)
- **FR-003**: System MUST calculate and return cosine similarity scores for each retrieved chunk
- **FR-004**: System MUST fetch the original chunk text and metadata (URL, section title, chunk index) from Qdrant
- **FR-005**: System MUST validate that retrieved chunks are retrievable and metadata is consistent (no null/corrupted data)
- **FR-006**: System MUST support predefined test query sets (5–10 queries covering major book topics)
- **FR-007**: System MUST generate a detailed debug report (JSON or CSV) with query results, similarity scores, and source metadata
- **FR-008**: System MUST support manual relevance assessment and notes (e.g., "relevant", "partially relevant", "irrelevant") with optional comments
- **FR-009**: System MUST support custom query sets (user-provided JSON/YAML file with queries and optional expected results)
- **FR-010**: System MUST support filtering results by source URL, section title, or chunk index range

### Key Entities

- **TestQuery**: A query string (text) with optional metadata (topic, expected results, difficulty level)
- **RetrievalResult**: Retrieved chunk with metadata (similarity score, source URL, text excerpt, chunk index)
- **RelevanceAssessment**: Manual evaluation of whether retrieved chunk is relevant to the query (relevant, partially relevant, irrelevant) with optional reasoning
- **DebugReport**: Structured output (JSON/CSV) containing: test queries, retrieval results, similarity scores, relevance assessments, and summary statistics

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All predefined test queries (5–10) execute without errors
- **SC-002**: Retrieval latency for each query is < 2 seconds (including Cohere embedding + Qdrant search)
- **SC-003**: Retrieved chunks have similarity scores ≥ 0.7 for at least 80% of queries (as manually verified)
- **SC-004**: Debug report is generated successfully and is readable/parseable (valid JSON/CSV)
- **SC-005**: Debug report includes all required fields: query text, retrieved chunks, similarity scores, source URLs, chunk text excerpts
- **SC-006**: Custom query sets (if provided) are loaded and executed correctly (error handling for malformed input)
- **SC-007**: Filtering by URL, section, or chunk index works correctly and results are properly filtered
- **SC-008**: Manual relevance assessments can be recorded for each query (interface or file format provided)
- **SC-009**: Validation results are reproducible: same input (queries, Qdrant state) produces identical results
- **SC-010**: Validation suite runs locally without external dependencies beyond Cohere and Qdrant APIs

---

## Assumptions

- Qdrant collection contains successfully embedded chunks (from the Book Embedding Pipeline feature 002)
- Book content is publicly available or accessible in Qdrant as chunk text (no external fetching required)
- Test queries are representative of real chatbot use cases (e.g., factual questions, topic searches)
- Cohere embedding model is the same as used in the embedding pipeline (consistency required)
- Manual relevance assessment is done by domain experts or QA engineers familiar with the book content
- Similarity threshold of 0.7 is acceptable as "relevant" (may be tuned based on use case)
- Qdrant Free Tier has sufficient storage and query limits for validation (up to 10,000 test queries is reasonable)
- Network connectivity is stable for Cohere and Qdrant API calls

---

## Non-Functional Requirements

### Performance
- Query embedding generation: ≤ 500ms per query (Cohere API)
- Qdrant similarity search: ≤ 500ms per query
- Total validation run (10 queries): ≤ 15 seconds
- Debug report generation: ≤ 5 seconds

### Reliability
- Retry logic for transient API failures (rate limits, timeouts)
- Graceful handling of empty results (no crashes, clear messages)
- Validation continues even if a single query fails (report includes failures)

### Security
- API keys (Cohere, Qdrant) not logged or exposed in report
- Chunk text and query logs stored locally only (no external transmission)
- HTTPS for all API calls

### Usability
- Clear command-line interface with simple options (e.g., `--queries queries.json`, `--filter-url "chapter-2"`)
- Human-readable debug report with summary statistics
- Optional interactive mode to manually label relevance

---

## Out of Scope

- Agent tool integration (handled separately)
- FastAPI endpoints or REST API (CLI-based validation only)
- Frontend or UI components
- Chat formatting, streaming, or conversation history
- Automated fixes (suggestions only, no auto-correction)
- Scalable distributed validation
- Multi-language query support (English queries only)

---

## Success Validation Plan

1. **Query Execution**: Run predefined test queries and verify all complete without errors
2. **Result Quality**: Manually review top-K results for each query and assess relevance (target: 80%+ relevant)
3. **Metadata Validation**: Confirm retrieved chunks have correct URLs, section titles, and text content
4. **Report Completeness**: Verify debug report includes all required fields and is properly formatted
5. **Custom Queries**: Test with user-provided query set and verify correct execution
6. **Filtering**: Test URL/section filters and confirm results are properly filtered
7. **Reproducibility**: Run same validation twice and confirm identical results
8. **Performance**: Measure latency for each query and verify < 2s individual queries and < 15s for full run

---

## Example Test Queries (for predefined set)

1. "What is physical AI?" (topic: foundational concepts)
2. "Explain kinematics and dynamics in humanoid robots" (topic: control and mechanics)
3. "What are the steps to set up a ROS 2 environment?" (topic: setup and tools)
4. "How do you implement feedback control?" (topic: control systems)
5. "What is reinforcement learning?" (topic: learning and AI)
6. "Describe the sim-to-real transfer problem" (topic: simulation and reality gap)
7. "How do you use Gazebo for simulation?" (topic: simulation tools)
8. "What safety precautions are needed for humanoid robots?" (topic: safety)
9. "Explain imitation learning with examples" (topic: learning)
10. "What are the key differences between ROS 1 and ROS 2?" (topic: middleware)

---

## Custom Query Format (Example)

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
      "notes": "Should cover ROS 2 setup and configuration"
    }
  ]
}
```

---

## Debug Report Format (Example)

```json
{
  "validation_timestamp": "2025-12-12T10:30:00Z",
  "total_queries": 10,
  "queries_executed": 10,
  "queries_failed": 0,
  "results": [
    {
      "query_id": "q1",
      "query_text": "What is physical AI?",
      "retrieved_chunks": 5,
      "results": [
        {
          "rank": 1,
          "similarity_score": 0.89,
          "source_url": "https://book.example.com/docs/01-fundamentals/physical-ai",
          "chunk_id": "abc123",
          "text_excerpt": "Physical AI is the branch of artificial intelligence...",
          "relevance_assessment": "relevant",
          "relevance_notes": "Accurate definition"
        },
        {
          "rank": 2,
          "similarity_score": 0.84,
          "source_url": "https://book.example.com/docs/01-fundamentals/embodied-intelligence",
          "chunk_id": "def456",
          "text_excerpt": "Embodied intelligence refers to...",
          "relevance_assessment": "relevant",
          "relevance_notes": "Good supporting context"
        }
      ]
    }
  ],
  "summary": {
    "avg_similarity_score": 0.81,
    "min_similarity_score": 0.65,
    "max_similarity_score": 0.92,
    "relevant_results_percent": 85,
    "partially_relevant_percent": 10,
    "irrelevant_percent": 5
  }
}
```
