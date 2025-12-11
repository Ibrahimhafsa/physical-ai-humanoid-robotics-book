# Implementation Plan: Retrieval-Augmented Agent API

**Branch**: `004-rag-agent-api` | **Date**: 2025-12-12 | **Spec**: [specs/004-rag-agent-api/spec.md](spec.md)

**Input**: FastAPI backend with OpenAI Agents SDK that performs retrieval-augmented generation (RAG) using Qdrant similarity search results. Agent responds ONLY using retrieved context, never hallucinating. API returns answer with sources and similarity scores.

## Summary

Build a production-ready REST API that orchestrates context-grounded responses by integrating retrieval (Feature 003: Qdrant similarity search) with LLM generation (OpenAI Agents SDK). The agent receives user queries via POST `/chat`, retrieves relevant book chunks from Qdrant, assembles context up to token limits, and generates factually grounded responses using a constraint-based system prompt. All responses include request tracking, source citations, similarity scores, and token usage metrics. Architecture emphasizes stateless design, graceful error handling, and zero hallucination through context-only generation.

## Technical Context

**Language/Version**: Python 3.11+ (aligns with Feature 003 backend, robotics standard)

**Primary Dependencies**:
- **FastAPI** 0.104+ - REST API framework with OpenAPI schema generation
- **OpenAI SDK** (beta Agents API) - Agent orchestration and LLM calls
- **Pydantic** 2.0+ - Request/response validation and JSON serialization
- **Qdrant Client** 2.7+ - Vector search client (reuses Feature 003 configuration)
- **tiktoken** 0.5+ - OpenAI token counting for context assembly
- **python-dotenv** 1.0+ - Environment variable management
- **uvicorn** 0.24+ - ASGI server for FastAPI

**Storage**: None (stateless, all context passed per-request; integration with Qdrant for retrieval only)

**Testing**: pytest 7.4+ with async support, mocking for OpenAI API and Qdrant client

**Target Platform**: Linux server (deployment), development on macOS/Windows with Python 3.11+

**Project Type**: Web API (backend only; frontend integration handled separately)

**Performance Goals**:
- Response latency: <3s p95 (including Qdrant search + LLM generation)
- Context assembly: <1s for top-K retrieval and token counting
- Token efficiency: <6000 tokens per request (95% of requests)

**Constraints**:
- Context window safety margin: max 6000 tokens (vs 4096 context window for GPT-3.5-turbo)
- Token limit enforcement: drop lower-relevance chunks if assembly exceeds limit
- Stateless per-request: no conversation history or session state
- Hallucination prevention: constraint prompting + context validation
- Rate limiting: 100 requests/minute per API key (client-configurable)

**Scale/Scope**:
- 10+ concurrent requests without degradation
- Handles 100+ spikes with rate limiting
- Supports 10-20 top-K chunks per query
- Average response payload: 1-2KB JSON

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I: Education-First Design** ✅ PASS
- RAG system serves learner needs (accurate, context-grounded answers to book questions)
- Clear system prompt enforces context-only responses (no hallucination)
- Error messages friendly and informative ("I don't have information about this topic")
- **Evidence**: Spec UC1 (query assistant), SC-004 (0% hallucination rate), edge case handling

**Principle II: Practical, Engineering-Focused Content** ✅ PASS
- API connects to real book content (Feature 002: embedded chapters)
- Token limits and latency constraints reflect real deployment constraints
- Stateless design reflects real API patterns (no state leaks)
- **Evidence**: FR-001-010 all testable with real Qdrant collection and OpenAI API

**Principle III: Content Accuracy & Safety** ✅ PASS
- Context-only generation prevents inaccuracy from hallucination
- Constraint prompting enforces accuracy boundaries
- API returns source citations for verification (similarity scores, URLs, chunk IDs)
- **Evidence**: SC-004 (0% hallucination), SC-007 (accurate citations), FR-003 (context-only)

**Principle IV: Docusaurus Standards & Consistency** ✅ PASS (not directly applicable to API)
- API serves Docusaurus content but does not modify it
- Metadata preserved in responses (source URLs, section_title)
- **Evidence**: FR-004 (return sources with metadata)

**Principle V: Testable, Reproducible Examples** ✅ PASS
- Success criteria measurable and testable (SC-001 through SC-010)
- Example request/responses in spec demonstrate usage
- Token counting and latency testable in CI/CD
- **Evidence**: Spec Success Validation Plan (5 validation steps)

**Principle VI: Iterative Improvement & Community Feedback** ✅ PASS
- API stateless design enables easy updates without state migration
- Configuration via environment variables (no hardcoding)
- Request ID tracking enables feedback/debugging
- **Evidence**: FR-009 (request ID), configurable thresholds (FR-005, FR-007)

**Overall Status**: ✅ **PASS** - All 6 principles satisfied. Design is education-focused, practical, safe, accurate, testable, and iterable.

## Project Structure

### Documentation (this feature)

```text
specs/004-rag-agent-api/
├── spec.md                      # Feature specification (complete)
├── plan.md                       # This file (in-progress)
├── research.md                   # Phase 0: Research findings (TBD)
├── data-model.md                 # Phase 1: Data entities & schemas
├── quickstart.md                 # Phase 1: Getting started guide
├── contracts/                    # Phase 1: API contracts
│   ├── openapi.json              # OpenAPI 3.0 specification
│   └── request-response.md        # Example payloads and error responses
├── checklists/
│   └── requirements.md           # Quality checklist (complete)
└── tasks.md                      # Phase 2: Implementation tasks (TBD)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agent/                   # Agent orchestration (NEW for Feature 004)
│   │   ├── __init__.py
│   │   ├── rag_agent.py          # OpenAI Agents SDK integration
│   │   ├── orchestrator.py        # Request → retrieval → generation flow
│   │   └── prompts.py            # Constraint prompts for context-only generation
│   │
│   ├── chat/                     # Chat API endpoints (NEW for Feature 004)
│   │   ├── __init__.py
│   │   ├── api.py                # FastAPI route definitions
│   │   ├── models.py             # Pydantic ChatRequest, ChatResponse
│   │   └── handlers.py           # Request validation & response assembly
│   │
│   ├── retrieve.py               # Reused from Feature 003
│   │   └── QueryEmbedder, QdrantRetriever, ContextExtractor
│   │
│   ├── config.py                 # Configuration management (NEW for Feature 004)
│   │   └── Settings, environment variables
│   │
│   ├── logging.py                # Structured logging (extend from Feature 003)
│   │
│   ├── tokens.py                 # Token counting utilities (NEW for Feature 004)
│   │   └── count_tokens, estimate_context_size
│   │
│   └── main.py                   # FastAPI app initialization (NEW for Feature 004)
│
├── tests/
│   ├── agent/                    # Agent tests
│   │   ├── test_rag_agent.py
│   │   └── test_orchestrator.py
│   │
│   ├── chat/                     # Chat API tests
│   │   ├── test_api.py
│   │   ├── test_models.py
│   │   └── test_handlers.py
│   │
│   ├── integration/              # End-to-end tests
│   │   └── test_chat_flow.py
│   │
│   └── conftest.py               # Shared pytest fixtures
│
├── examples/
│   └── predefined_queries.json   # Reused from Feature 003
│
├── .env.example                  # Environment variables (extend from Feature 003)
├── pyproject.toml                # UV project config (extend from Feature 003)
├── requirements.txt              # Dependencies
└── README.md                      # Feature 004 setup & usage
```

**Structure Decision**: Web API (backend only). Extends existing `backend/` directory from Feature 003. New modules for agent orchestration (`agent/`) and API endpoints (`chat/`). Reuses retrieval modules from Feature 003. Follows separation of concerns: retrieval (Feature 003), agent reasoning (Feature 004 agent/), REST API (Feature 004 chat/).

## Phase 0: Research & Architecture Decisions

*Output: research.md with decision log*

**Key Research Tasks:**

1. **OpenAI Agents SDK Integration** - Confirm API availability, authentication patterns, context injection methods
2. **Async Context Assembly** - Best practices for concurrent Qdrant search + token counting
3. **Constraint Prompting Patterns** - How to enforce context-only generation without hallucination
4. **Error Handling Strategies** - Circuit breaker patterns for external service calls (Qdrant, OpenAI)
5. **Request Tracing** - Request ID generation and correlation logging patterns
6. **Token Counting Accuracy** - tiktoken edge cases and accuracy in context assembly

**Architecture Decisions to Document:**

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| **Stateless per-request** | Simplifies deployment, no session management, matches REST principles | Session-based (adds complexity, violates spec) |
| **Constraint prompting for hallucination prevention** | System prompt limits agent to context-only responses | Fine-tuning (expensive), retrieval augmentation alone (insufficient) |
| **Token limit enforcement before LLM call** | Prevents API errors and cost overruns | Generate then truncate (wastes tokens) |
| **Context assembly via top-K ranking** | Simple, deterministic, aligns with similarity scores | Semantic clustering (adds complexity) |
| **HTTP status codes for error classes** | Standard REST semantics (400 validation, 429 rate limit, 503 unavailable) | Custom status codes (non-standard, confusing) |
| **Request ID for all responses** | Enables debugging, tracing, user support | No tracking (impossible to debug) |
| **Stateless agent design** | No memory leaks, matches spec FR-008, simplifies testing | Stateful (violates spec) |

---

## Phase 1: Data Model & API Design

*Output: data-model.md, contracts/openapi.json, contracts/request-response.md, quickstart.md*

### Data Model Entities

**ChatRequest** (user input)
- `query: str` - User question (required, non-empty)
- `top_k: int = 5` - Number of chunks to retrieve (1-20, configurable)
- `similarity_threshold: float = 0.5` - Minimum relevance score (0.0-1.0)
- `user_id: str | None` - Optional user identifier for tracking
- `session_id: str | None` - Optional session identifier
- `metadata: dict | None` - Additional user metadata
- **Validation**: query must be non-empty, top_k ∈ [1,20], threshold ∈ [0.0, 1.0]

**RetrievalResult** (chunk from Qdrant)
- `chunk_id: str` - Unique chunk identifier
- `text: str` - Chunk text content
- `similarity_score: float` - Cosine similarity to query (0.0-1.0)
- `source_url: str` - URL of source document
- `section_title: str` - Document section/chapter
- `rank: int` - Position in result set (1-indexed)

**ContextWindow** (assembly configuration)
- `max_tokens: int = 6000` - Maximum total context tokens
- `reserved_for_response: int = 1500` - Tokens reserved for LLM response
- `chunk_ordering: str = "similarity"` - Ranking strategy (similarity, position, hybrid)

**ChatResponse** (API response)
- `request_id: str` - Request tracking ID (UUID format)
- `answer: str` - Agent-generated answer
- `sources: list[RetrievalResult]` - Retrieved chunks used
- `context_used: int` - Number of chunks included
- `tokens_used: int` - Total tokens consumed
- `response_time_ms: int` - API latency
- `timestamp: str` - ISO 8601 timestamp
- `note: str | None` - Optional message (e.g., "Limited context available")

**ErrorResponse** (error cases)
- `request_id: str` - Request tracking ID
- `error: str` - Error type (e.g., "Validation Error", "Service Unavailable")
- `details: list[ErrorDetail]` - Field-level errors
- `timestamp: str` - ISO 8601 timestamp

### API Contracts

**POST /chat** (primary endpoint)

*Request*:
```json
{
  "query": "What is physical AI?",
  "top_k": 5,
  "similarity_threshold": 0.7,
  "user_id": "user_123"
}
```

*Response (200 OK)*:
```json
{
  "request_id": "req_abc123",
  "answer": "Physical AI refers to artificial intelligence systems embodied in physical agents...",
  "sources": [
    {
      "chunk_id": "chunk_001",
      "text": "Physical AI is the study of...",
      "similarity_score": 0.89,
      "source_url": "https://book.example.com/docs/01-fundamentals/physical-ai",
      "section_title": "Introduction to Physical AI",
      "rank": 1
    }
  ],
  "context_used": 3,
  "tokens_used": 487,
  "response_time_ms": 1850,
  "timestamp": "2025-12-12T10:30:00Z"
}
```

*Error Responses*:
- **400 Bad Request**: Invalid query (empty), malformed top_k/threshold
- **429 Too Many Requests**: Rate limit exceeded (100 req/min)
- **503 Service Unavailable**: Qdrant unreachable, OpenAI API error

**GET /health** (health check)
- Returns: `{ "status": "ok", "timestamp": "..." }`
- Used for deployment readiness checks

**GET /docs** (OpenAPI documentation)
- Auto-generated by FastAPI, available at `/docs`

### Integration with Feature 003

- **Retrieval Pipeline**: Reuse QueryEmbedder, QdrantRetriever from Feature 003
- **Configuration**: Extend .env.example with OpenAI API key, agent configuration
- **Logging**: Extend structured logging from Feature 003 to include request tracing

---

## Key Implementation Decisions

**AD-001: Constraint Prompting for Hallucination Prevention**
- **Decision**: Use system prompt to limit agent to context-only responses
- **Constraint**: "You MUST only use the provided context. Do not use external knowledge. If context is insufficient, say so."
- **Rationale**: Aligns with SC-004 (0% hallucination rate), simplest approach, no fine-tuning needed
- **Trade-off**: LLM cannot leverage pre-training knowledge (by design, prevents hallucination)

**AD-002: Stateless Request Processing**
- **Decision**: All context passed per-request, no session storage
- **Rationale**: Aligns with spec FR-008, simplifies deployment, prevents state leaks (SC-010)
- **Trade-off**: Cannot maintain multi-turn conversation history (by design, outside scope)

**AD-003: Token-Limited Context Assembly**
- **Decision**: Assemble context by ranking chunks by similarity, include until token limit or relevance threshold
- **Implementation**: Use tiktoken to count tokens, drop lower-ranked chunks if exceeding max
- **Rationale**: Respects FR-007 and SC-003 (6000 token limit, 95% of requests)
- **Trade-off**: May exclude relevant chunks if token budget exhausted (acceptable per spec)

**AD-004: Structured Error Responses**
- **Decision**: Return HTTP status codes + detailed error objects (not plain text)
- **Status Codes**: 400 (validation), 429 (rate limit), 503 (service unavailable)
- **Rationale**: Aligns with SC-005, SC-006; enables client error handling
- **Trade-off**: Requires clients to parse JSON errors (standard practice)

**AD-005: Request ID Tracking**
- **Decision**: Generate UUID4 for every request, include in all responses
- **Rationale**: Aligns with FR-009, enables debugging and user support
- **Implementation**: Middleware generates request_id, passed through all layers

**AD-006: Async I/O for Concurrency**
- **Decision**: Use async/await for Qdrant search + token counting, serial LLM generation
- **Rationale**: Maximize concurrency for I/O-bound operations (Qdrant), serial for CPU-bound (token counting)
- **Rationale**: Supports SC-009 (100+ concurrent requests)
- **Trade-off**: Adds complexity but necessary for performance goals

---

## Testing Strategy

**Unit Tests** (agent, handlers, token counting):
- Mock Qdrant client (return sample chunks)
- Mock OpenAI Agents SDK (return structured responses)
- Test token counting accuracy
- Test error handling (invalid input, API errors)

**Integration Tests**:
- Full request → retrieval → generation → response flow
- Verify response structure and required fields
- Test edge cases (no context, rate limiting)

**Performance Tests**:
- Measure latency (goal: <3s p95)
- Measure token usage (goal: <6000 tokens)
- Load test with 10+ concurrent requests

**Example Test Queries**: Use Feature 003 predefined_queries.json for consistency

---

## Success Criteria Mapping

| Spec Success Criterion | Implementation Approach |
|------------------------|-------------------------|
| SC-001: 80% accuracy | Manual QA with 20+ test queries using predefined set |
| SC-002: <3s latency | Measure response_time_ms in ChatResponse |
| SC-003: <6000 tokens | Track tokens_used, enforce limit in context assembly |
| SC-004: 0% hallucination | Constraint prompting + validation (no external knowledge) |
| SC-005: HTTP 400 for validation | Pydantic model validation + explicit error responses |
| SC-006: HTTP 503 for unreachable | Circuit breaker pattern for external calls |
| SC-007: Accurate citations | Return actual source URLs from Qdrant metadata |
| SC-008: All required fields | ChatResponse includes: answer, sources, similarity_scores, request_id |
| SC-009: 100+ concurrent | Async I/O, rate limiting, tested via load test |
| SC-010: Stateless | No session storage, per-request context assembly |

---

## Next Steps

1. **Phase 0 Complete**: Research decisions and architecture patterns documented
2. **Phase 1 Complete**: Data model, API contracts, integration points defined
3. **Ready for**: Phase 2 task generation (`/sp.tasks`) to create implementation checklist
4. **Then**: Phase 3 implementation (`/sp.implement`) with code generation
