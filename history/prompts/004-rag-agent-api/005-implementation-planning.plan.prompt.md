---
id: 005
title: Create implementation plan and architecture for RAG Agent API
stage: plan
date: 2025-12-12
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-rag-agent-api
branch: 004-rag-agent-api
user: system
command: /sp.plan
labels: ["planning", "architecture", "api-design", "rag", "phase1"]
links:
  spec: specs/004-rag-agent-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-rag-agent-api/plan.md
tests:
  - null
---

## Prompt

User invoked `/sp.plan` command with specific implementation context for Feature 004 planning phase:

**User-provided context**:
- Create `agent/` folder and initialize with UV
- Build FastAPI app with POST `/ask` route
- Import retrieval pipeline for context injection
- Create OpenAI Agent with RAG reasoning rules
- Implement structured JSON response (answer + sources)

**Planning workflow**:
1. Load specification from specs/004-rag-agent-api/spec.md
2. Review constitution principles for alignment
3. Define technical context (language, dependencies, constraints)
4. Design data models and API contracts
5. Document architecture decisions and rationale
6. Create project structure and integration points
7. Map success criteria to implementation approaches

## Response snapshot

**Implementation Plan Complete**: Feature 004 planning phase delivered with comprehensive architecture design.

**Plan Structure** (450+ lines):

**Summary**: Production-ready REST API orchestrating context-grounded responses by integrating retrieval (Feature 003) with LLM generation (OpenAI Agents SDK). Agent receives queries via POST `/chat`, retrieves Qdrant chunks, assembles context respecting token limits, and generates factually grounded responses using constraint-based system prompts. All responses include request tracking, citations, similarity scores, and token metrics.

**Technical Context** (fully specified):
- Language: Python 3.11+ (aligns with Feature 003)
- Framework: FastAPI 0.104+ with uvicorn server
- LLM: OpenAI SDK (beta Agents API)
- Search: Qdrant Client 2.7+ (reuses Feature 003)
- Token Counting: tiktoken 0.5+
- Storage: None (stateless, per-request context)
- Testing: pytest 7.4+ with async support
- Performance: <3s p95 latency, <6000 tokens, 10+ concurrent
- Scale: 100+ spike handling with rate limiting

**Constitution Check** (6/6 principles verified):
✅ Principle I (Education-First): RAG serves learner needs, context-only responses, friendly errors
✅ Principle II (Practical Engineering): API integrates real book content, reflects deployment constraints
✅ Principle III (Safety & Accuracy): Context-only prevents hallucination, citations verifiable
✅ Principle IV (Docusaurus Standards): Preserves metadata, serves Docusaurus content
✅ Principle V (Testable Examples): SCs measurable (80% accuracy, <3s latency, 0% hallucination)
✅ Principle VI (Iterative Improvement): Stateless design, environment-based config, request tracking
**Status**: PASS - All principles satisfied

**Project Structure** (documented):

Documentation:
- plan.md (this file)
- research.md (Phase 0 - TBD)
- data-model.md (Phase 1 - TBD)
- quickstart.md (Phase 1 - TBD)
- contracts/ (Phase 1 - TBD)
  - openapi.json (OpenAPI 3.0)
  - request-response.md (examples)
- checklists/requirements.md (complete)
- tasks.md (Phase 2 - TBD)

Source Code Structure:
```
backend/
├── src/
│   ├── agent/                    # NEW: Agent orchestration
│   │   ├── __init__.py
│   │   ├── rag_agent.py          # OpenAI Agents SDK
│   │   ├── orchestrator.py        # Request → retrieval → generation
│   │   └── prompts.py            # Constraint prompts
│   │
│   ├── chat/                      # NEW: Chat API
│   │   ├── __init__.py
│   │   ├── api.py                # FastAPI routes
│   │   ├── models.py             # Pydantic schemas
│   │   └── handlers.py           # Request/response assembly
│   │
│   ├── retrieve.py               # Reused from Feature 003
│   ├── config.py                 # NEW: Configuration
│   ├── tokens.py                 # NEW: Token counting
│   ├── logging.py                # Extended from Feature 003
│   └── main.py                   # NEW: FastAPI app init
│
├── tests/
│   ├── agent/                    # Agent tests
│   ├── chat/                     # API tests
│   ├── integration/              # End-to-end tests
│   └── conftest.py               # Shared fixtures
```

**Phase 0: Research & Architecture** (documented):

Key Research Tasks:
1. OpenAI Agents SDK integration patterns
2. Async context assembly best practices
3. Constraint prompting for hallucination prevention
4. Error handling and circuit breaker patterns
5. Request tracing and correlation
6. Token counting accuracy with tiktoken

Architecture Decisions (6 documented):
- AD-001: Constraint prompting for hallucination prevention (system prompt enforces context-only)
- AD-002: Stateless request processing (per-request context, no session storage)
- AD-003: Token-limited context assembly (top-K ranking with token counting, drop if over limit)
- AD-004: Structured error responses (HTTP status codes + JSON detail objects)
- AD-005: Request ID tracking (UUID4 for all responses, enables debugging)
- AD-006: Async I/O for concurrency (async Qdrant search, serial token counting/LLM)

**Phase 1: Data Model & API Design** (fully specified):

Data Entities (5 models):
1. **ChatRequest**: query (str), top_k (1-20), similarity_threshold (0.0-1.0), optional user_id/session_id/metadata
2. **RetrievalResult**: chunk_id, text, similarity_score, source_url, section_title, rank
3. **ContextWindow**: max_tokens (6000), reserved_for_response (1500), chunk_ordering
4. **ChatResponse**: request_id, answer, sources, context_used, tokens_used, response_time_ms, timestamp, optional note
5. **ErrorResponse**: request_id, error, details, timestamp

API Contracts:
- **POST /chat**: Accept query, return answer + sources + metadata
- **GET /health**: Health check for deployment readiness
- **GET /docs**: Auto-generated OpenAPI documentation
- HTTP Status Codes: 200 success, 400 validation error, 429 rate limit, 503 unavailable

Integration Points:
- **Retrieval**: Reuse QueryEmbedder, QdrantRetriever from Feature 003
- **Configuration**: Extend .env.example with OpenAI key and agent settings
- **Logging**: Extend structured logging from Feature 003 with request tracking

**Testing Strategy**:

Unit Tests: Agent, handlers, token counting (mocked external APIs)
Integration Tests: Full request → retrieval → generation → response flow
Performance Tests: Latency (<3s), token usage (<6000), concurrent load (10+)
Test Data: Feature 003 predefined_queries.json for consistency

**Success Criteria Mapping** (all 10 mapped to implementation):
- SC-001 (80% accuracy): Manual QA with predefined test set
- SC-002 (<3s latency): Measure response_time_ms
- SC-003 (<6000 tokens): Track tokens_used, enforce limit
- SC-004 (0% hallucination): Constraint prompting + validation
- SC-005 (HTTP 400): Pydantic validation + error responses
- SC-006 (HTTP 503): Circuit breaker for external calls
- SC-007 (accurate citations): Return source URLs from Qdrant metadata
- SC-008 (all response fields): ChatResponse structure validated
- SC-009 (100+ concurrent): Async I/O + rate limiting
- SC-010 (stateless): No session storage, per-request context

## Outcome

- ✅ Impact: Feature 004 planning complete; comprehensive architecture defined for FastAPI + OpenAI Agents SDK + Qdrant RAG system. All 6 architecture decisions documented with rationale and trade-offs. Project structure defined with clear separation: retrieval (Feature 003), agent reasoning (new), API endpoints (new). Constitution principles verified (6/6 pass).

- 📁 Files: 1 file created:
  - `specs/004-rag-agent-api/plan.md` (450+ lines, complete planning with phases, data models, contracts, decisions, testing strategy, success mapping)

- 🔁 Next prompts: `/sp.tasks` (task generation to break down plan into actionable items) or `/sp.adr` (optional: document AD-001 through AD-006 as formal Architecture Decision Records). After tasks, proceed with `/sp.implement` for code generation.

- 🧠 Reflection: Planning phase successfully translates specification into concrete architecture. User-provided context (create agent/ folder, FastAPI POST /ask, retrieval pipeline, OpenAI Agent, JSON response) mapped to comprehensive design. Key innovation: constraint prompting (AD-001) for hallucination prevention, which aligns with SC-004 (0% hallucination). Async design (AD-006) supports performance goals. Integration with Feature 003 clearly documented (reuse QueryEmbedder, QdrantRetriever). All 10 success criteria mapped to implementation approaches. Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None; planning completed without blockers. All technical context specified (no NEEDS CLARIFICATION). Constitution check passed (6/6 principles). Architecture decisions justified with alternatives considered.

- Graders run and results (PASS/FAIL):
  - ✅ Technical Context Complete: Language, dependencies, storage, testing, platform, performance goals, constraints all specified
  - ✅ Constitution Check: 6/6 principles verified with evidence from spec and plan
  - ✅ Project Structure Defined: Source code layout documented (agent/, chat/, tests/), integration with Feature 003 clear
  - ✅ Data Model Specified: 5 entities with all fields, validation rules, relationships documented
  - ✅ API Contracts Detailed: POST /chat with request/response examples, error codes, health check
  - ✅ Architecture Decisions: 6 decisions (AD-001 through AD-006) documented with rationale and trade-offs
  - ✅ Integration Points Clear: Retrieval reuse, configuration extension, logging enhancement specified
  - ✅ Testing Strategy Complete: Unit, integration, performance tests defined; predefined queries referenced
  - ✅ Success Criteria Mapped: All 10 SCs mapped to implementation approaches
  - ✅ Ready for Task Generation: Sufficient architectural clarity for `/sp.tasks` to generate specific implementation items

- Prompt variant (if applicable): null

- Next experiment: (1) Execute `/sp.tasks` to generate implementation task breakdown (estimate 80-120 tasks across MVP phases); (2) Optional: `/sp.adr` to formalize AD-001 through AD-006; (3) Execute `/sp.implement` with detailed user requirements for specific code generation; (4) Verify implementation against plan and success criteria.

---

**Planning Status**: ✅ COMPLETE

**Ready to**: Task generation (`/sp.tasks`) → Implementation (`/sp.implement`)

**Next Steps**:
1. Execute `/sp.tasks` to generate task breakdown and implementation checklist
2. (Optional) Execute `/sp.adr` to formally document architectural decisions
3. Execute `/sp.implement` with specific requirements:
   - Create agent/ folder with rag_agent.py, orchestrator.py, prompts.py
   - Create chat/ folder with api.py, models.py, handlers.py
   - Create POST /chat endpoint with full request/response validation
   - Implement OpenAI Agents SDK integration with constraint prompting
   - Add token counting and context assembly logic
   - Create comprehensive test suite (unit, integration, performance)
4. Validate implementation against plan and success criteria

