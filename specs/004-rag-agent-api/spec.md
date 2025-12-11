# Feature Specification: Retrieval-Augmented Agent API

**Feature Branch**: `004-rag-agent-api`
**Created**: 2025-12-12
**Status**: Draft
**Input**: Build a FastAPI backend using OpenAI Agents SDK that performs retrieval-augmented responses using Qdrant results. Agent receives user queries via REST POST, fetches relevant chunks from Qdrant, responds ONLY using provided context with no hallucinations, returns answer with sources and similarity scores, handles empty results gracefully.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Query Assistant with Context-Grounded Responses (Priority: P1)

As a developer integrating the retrieval-augmented agent into a book chatbot, I want the agent to answer user questions about book content by retrieving relevant chunks from Qdrant and responding ONLY using that context, so that all answers are factually accurate and grounded in the source material.

**Why this priority**: This is the core MVP—the agent must reliably answer questions using retrieved context without hallucinating or inventing information. Without this, the chatbot cannot be trusted for learning.

**Independent Test**: Send a POST request to `/chat` with a user query (e.g., "What is physical AI?"), verify that:
1. Agent retrieves top-K chunks from Qdrant
2. Agent generates answer using ONLY those chunks
3. API returns answer, list of source URLs, and similarity scores
4. Answer is grounded in retrieved text (no hallucination)

**Acceptance Scenarios**:

1. **Given** a user query about book content, **When** the query is POSTed to `/chat`, **Then** the agent retrieves relevant chunks and responds with an answer grounded in those chunks, including source URLs and similarity scores
2. **Given** a question about "kinematics and dynamics", **When** the agent searches Qdrant, **Then** it returns an answer referencing retrieved chunks with similarity scores ≥0.7
3. **Given** a valid query, **When** the agent responds, **Then** the response includes: answer text, list of source URLs, and similarity scores for each chunk used
4. **Given** a question outside book scope (e.g., "current stock price"), **When** no relevant chunks are retrieved (scores all <0.5), **Then** agent responds with "I don't have information about this topic in the provided materials"

---

### User Story 2 - Error Handling for Empty or Irrelevant Results (Priority: P2)

As a chatbot developer, I want the agent to gracefully handle cases where no relevant context is found for a user query, so that the chatbot provides helpful error messages instead of hallucinating answers or crashing.

**Why this priority**: Error handling is essential for production reliability. Users should receive clear feedback when the system cannot find relevant information, rather than receiving made-up answers.

**Independent Test**: Send queries that produce no results (e.g., "What is the weather today?") and verify:
1. Agent detects low relevance (all chunk scores <threshold, default 0.5)
2. Agent responds with a friendly, informative message
3. API returns appropriate HTTP status and error details
4. No hallucination occurs (agent does not make up an answer)

**Acceptance Scenarios**:

1. **Given** a query with no relevant chunks (all scores <0.5), **When** the agent evaluates results, **Then** it returns an informative response like "I don't have information about this topic"
2. **Given** an empty Qdrant collection, **When** `/chat` is called, **Then** the agent responds with a clear error message and HTTP 503 (Service Unavailable)
3. **Given** a malformed query or missing required fields, **When** the request is validated, **Then** the API returns HTTP 400 (Bad Request) with field-specific error details

---

### User Story 3 - Performance and Safety Within Token Limits (Priority: P3)

As a platform engineer, I want the agent to respect context window limits and respond within reasonable latency, so that the chatbot remains responsive and does not exceed token limits that would cause API failures.

**Why this priority**: Token management and response latency are critical for production deployments. Exceeding token limits causes API errors, and slow responses degrade user experience. This ensures the system remains cost-effective and responsive.

**Independent Test**: Monitor agent responses for:
1. Total context + response stays within safe token limits (e.g., 6000 tokens for GPT-3.5-turbo with 4096 context window)
2. Response latency <3 seconds for typical queries
3. Context is prioritized (top-K chunks selected, lower-relevance chunks excluded if needed to stay within token limit)

**Acceptance Scenarios**:

1. **Given** a query that retrieves many chunks, **When** context assembly would exceed token limit, **Then** the agent includes only top-scoring chunks and notes that some results were omitted
2. **Given** a complex query, **When** the agent retrieves and processes results, **Then** the response is returned within 3 seconds
3. **Given** repeated queries over time, **When** agent responds, **Then** no memory of previous conversations is retained (stateless per request)

---

### Edge Cases

- What happens if Qdrant is unreachable? → Return HTTP 503 with clear error message, no attempt to generate response without context
- What happens if OpenAI API rate limit is exceeded? → Return HTTP 429 (Too Many Requests) with retry guidance
- What happens if a query is empty or contains only whitespace? → Return HTTP 400 with validation error
- What happens if retrieved chunks are very short or repetitive? → Agent acknowledges limited context and provides best-effort answer with caveat
- What happens if similarity scores are all below threshold but some results are retrieved? → Agent returns "Limited information available" rather than silence or fabrication

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Agent MUST receive user queries via REST POST endpoint `/chat`
- **FR-002**: Agent MUST retrieve top-K relevant chunks from Qdrant collection based on query similarity
- **FR-003**: Agent MUST generate responses ONLY using context from retrieved chunks (no external knowledge or hallucination)
- **FR-004**: Agent MUST return response including: answer text, list of source URLs, similarity scores, and chunk metadata
- **FR-005**: Agent MUST validate that retrieved chunks have similarity scores above threshold (default 0.5); if not, return "no relevant information" message
- **FR-006**: Agent MUST handle cases where Qdrant is unreachable or collection is empty with appropriate error responses
- **FR-007**: Agent MUST respect OpenAI API token limits; context window must not exceed safe limits (configurable, default 6000 tokens)
- **FR-008**: Agent MUST implement stateless request/response (no conversation history or memory across requests)
- **FR-009**: Agent MUST provide request ID tracking for debugging and logging
- **FR-010**: API MUST validate request format and return clear validation errors for malformed requests

### Key Entities

- **ChatRequest**: User query with optional metadata (user_id, session_id, metadata dict)
- **RetrievalResult**: Chunk retrieved from Qdrant with similarity_score, source_url, section_title, text, chunk_id
- **ChatResponse**: Agent's response including answer_text, retrieved_sources (list of URLs), similarity_scores, context_used, request_id, timestamp
- **ContextWindow**: Configuration for token limits and context assembly strategy

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent successfully answers 80% of user questions correctly using only retrieved context (verified via manual QA with 20+ test queries)
- **SC-002**: Agent generates responses within 3 seconds for typical queries (95th percentile latency)
- **SC-003**: Total context (retrieved chunks + query + response) stays within 6000 tokens for 95% of requests
- **SC-004**: System correctly rejects queries with no relevant context (similarity all <0.5) with appropriate message (0% hallucination rate)
- **SC-005**: API returns HTTP 400 for malformed requests with clear field-level error messages
- **SC-006**: API returns HTTP 503 for unreachable Qdrant with recovery instructions (no 5xx server crashes)
- **SC-007**: Agent citations are accurate (source URLs and chunk references are correct)
- **SC-008**: Response includes all required fields: answer_text, sources, similarity_scores, request_id
- **SC-009**: System handles spike in requests (100+ concurrent) without queue buildup or timeout (with rate limiting guidance)
- **SC-010**: Agent does not retain conversation state between requests (each request is independent, no memory leaks)

---

## Assumptions

- OpenAI API keys are configured via environment variables or secure secret management
- Qdrant collection (`book_embeddings`) exists and is pre-populated with book chunks (from Feature 002: Book Embedding Pipeline)
- Retrieved chunks have metadata including: url (source URL), section_title, text, chunk_id (from Qdrant payload)
- Similarity threshold of 0.5 is acceptable for determining "relevant" context; threshold is configurable
- Context window limit of 6000 tokens is safe for the LLM being used (GPT-3.5-turbo or compatible)
- Queries are in English; non-English queries may not perform as well
- Users accept rate limiting for high-volume scenarios (e.g., 100 requests per minute per API key)
- Responses are expected to be concise and factual, not creative or conversational in tone

---

## Non-Functional Requirements

### Performance
- Query response latency: <3 seconds for 95th percentile (including Qdrant retrieval + LLM generation)
- API throughput: Support 10+ concurrent requests without significant degradation
- Token usage: <6000 tokens per request (safety margin below LLM context limit)

### Reliability
- Graceful degradation when Qdrant is unreachable (HTTP 503, not crash)
- Graceful handling of OpenAI API errors (rate limits, timeouts, overloaded service)
- No conversation state retention (each request independent, no memory leaks)

### Security
- API keys not logged or exposed in responses
- Request/response logging sanitized (no sensitive query content in logs by default)
- CORS policy configured appropriately for chatbot integration
- Rate limiting to prevent abuse (e.g., 100 requests per minute per client)

### Usability
- Clear error messages for users when context is unavailable
- API responses always include request_id for debugging
- Documentation with examples for chatbot integration
- Configurable similarity threshold and context window via environment variables

### Maintainability
- Code modular: separate concerns for retrieval, context assembly, agent orchestration
- Configuration externalized (environment variables for API keys, thresholds, limits)
- Comprehensive logging for debugging and monitoring

---

## Out of Scope

- Frontend UI integration (chatbot UI is built separately)
- Database admin tools or dashboards
- Streaming or WebSocket endpoints (request/response only)
- Multi-turn conversation history (each request is stateless)
- Fine-tuning or training of the LLM
- Custom LLM models (uses OpenAI API only)
- Voice input/output or multi-language support
- Analytics or usage dashboards

---

## Success Validation Plan

1. **Accuracy Validation**: Test 20+ diverse queries covering all major book chapters; verify answers use only retrieved context and are accurate (manual review by domain expert)
2. **Error Handling**: Test 10+ edge cases (empty results, unreachable services, malformed input); verify appropriate error responses with no hallucination
3. **Performance**: Load test with 10+ concurrent requests; measure latency and token usage; verify <3s response time
4. **Integration**: Connect to live chatbot UI (if available); validate end-to-end chat flow
5. **Security**: Verify API keys not exposed, rate limiting works, CORS configured correctly

---

## Example Request/Response

### Example 1: Successful Query

**Request**:
```json
{
  "query": "What is physical AI?",
  "top_k": 5,
  "similarity_threshold": 0.7,
  "user_id": "user_123"
}
```

**Response**:
```json
{
  "request_id": "req_abc123def456",
  "answer": "Physical AI refers to artificial intelligence systems embodied in physical agents like robots. It combines control theory, perception, and learning to enable robots to interact with the real world and accomplish physical tasks.",
  "sources": [
    {
      "url": "https://book.example.com/docs/01-fundamentals/physical-ai",
      "section_title": "Introduction to Physical AI",
      "similarity_score": 0.89,
      "chunk_id": "chunk_001"
    },
    {
      "url": "https://book.example.com/docs/01-fundamentals/embodied-intelligence",
      "section_title": "Embodied Intelligence Concepts",
      "similarity_score": 0.82,
      "chunk_id": "chunk_002"
    }
  ],
  "context_used": 3,
  "tokens_used": 487,
  "response_time_ms": 1850,
  "timestamp": "2025-12-12T10:30:00Z"
}
```

### Example 2: No Relevant Context

**Request**:
```json
{
  "query": "What is the current stock market?",
  "top_k": 5,
  "similarity_threshold": 0.7
}
```

**Response**:
```json
{
  "request_id": "req_xyz789abc123",
  "answer": "I don't have information about this topic in the provided book materials. The book focuses on physical AI and humanoid robotics, not financial markets.",
  "sources": [],
  "context_used": 0,
  "tokens_used": 45,
  "response_time_ms": 320,
  "timestamp": "2025-12-12T10:31:00Z",
  "note": "No chunks with similarity ≥0.7 found for this query"
}
```

### Example 3: Error - Malformed Request

**Request**:
```json
{
  "query": ""
}
```

**Response** (HTTP 400):
```json
{
  "error": "Validation Error",
  "details": [
    {
      "field": "query",
      "message": "Query cannot be empty"
    }
  ],
  "request_id": "req_error_456"
}
```

---

## Implementation Notes for Developers

- Use OpenAI Agents SDK for agent orchestration and LLM calls
- Implement retrieval via Qdrant client (search by similarity)
- Assemble context by concatenating top-K chunk texts until token limit or relevance threshold is breached
- Use system prompt to constrain agent: "You MUST only use the provided context. Do not use external knowledge. If context is insufficient, say so."
- Implement token counting before sending to LLM (use `tiktoken` library for OpenAI token estimation)
- Log all requests/responses with sanitization (no sensitive user data)
- Use structured logging (JSON format) for monitoring and debugging
- Implement circuit breaker or timeout for external service calls (Qdrant, OpenAI)
