---
description: "Task list for RAG Agent API implementation"
---

# Tasks: Retrieval-Augmented Agent API (Feature 004)

**Input**: Design documents from `/specs/004-rag-agent-api/`
**Prerequisites**: plan.md (complete), spec.md (complete), architecture decisions (AD-001 through AD-006)

**Tests**: Comprehensive test suite included (unit, integration, performance) - explicitly requested in spec
**Organization**: Tasks organized by user story (P1, P2, P3) to enable independent implementation and testing

**Total Tasks**: 95 tasks across 6 phases
**MVP Scope**: Phase 1-3 (Setup + Foundational + US1) = 45 tasks

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- **File paths**: Relative to `backend/` directory (matching project structure from plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependencies

- [ ] T001 Create agent/ folder structure in backend/src/agent/ per plan.md
- [ ] T002 [P] Create chat/ folder structure in backend/src/chat/ with __init__.py
- [ ] T003 [P] Initialize UV project with dependencies (FastAPI, OpenAI SDK, Pydantic, Qdrant, tiktoken, pytest)
- [ ] T004 [P] Create pyproject.toml with dependencies (fastapi, openai, pydantic, qdrant-client, tiktoken, python-dotenv, uvicorn, pytest)
- [ ] T005 [P] Create requirements.txt with pinned versions
- [ ] T006 Create .env.example extending Feature 003 with OPENAI_API_KEY, OPENAI_MODEL, AGENT_CONFIG settings
- [ ] T007 [P] Set up GitHub Actions CI/CD configuration for testing and linting
- [ ] T008 [P] Configure pytest with async support and fixtures in tests/conftest.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can begin

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 [P] Create backend/src/config.py with Settings class (Pydantic, environment variables, defaults)
- [ ] T010 [P] Create backend/src/logging.py extending Feature 003 with structured JSON logging and request tracking
- [ ] T011 [P] Create backend/src/tokens.py with token counting utilities (count_tokens, estimate_context_size functions)
- [ ] T012 [P] Create backend/src/models/__init__.py (package initialization)
- [ ] T013 [P] Create backend/src/models/common.py with base request/response models and validators
- [ ] T014 Create backend/src/main.py FastAPI app initialization with CORS, middleware, health check endpoint
- [ ] T015 [P] Implement request ID middleware in backend/src/main.py (UUID4 generation, context propagation)
- [ ] T016 [P] Implement global error handler in backend/src/main.py (return structured ErrorResponse)
- [ ] T017 [P] Implement rate limiting middleware in backend/src/main.py (100 req/min per API key)
- [ ] T018 Create test fixtures in tests/conftest.py (mock Qdrant client, mock OpenAI Agents SDK, sample queries)
- [ ] T019 [P] Create mock factories for test data (ChatRequest, RetrievalResult, ChatResponse)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Query Assistant with Context-Grounded Responses (Priority: P1) 🎯 MVP

**Goal**: Implement core RAG functionality where agent answers user queries using ONLY retrieved context, with no hallucination.

**Independent Test**:
1. POST query to `/chat` endpoint with {"query": "What is physical AI?", "top_k": 5}
2. Verify response contains: answer, sources (with URLs and similarity scores), request_id, tokens_used
3. Verify answer is grounded in retrieved chunks (manual review of 20+ queries)
4. Verify no external knowledge used (0% hallucination rate)

### Contract Tests for User Story 1

- [ ] T020 [P] [US1] Create tests/contract/test_chat_endpoint.py with POST /chat request/response validation
- [ ] T021 [P] [US1] Create tests/contract/test_models.py validating ChatRequest, ChatResponse, RetrievalResult schemas
- [ ] T022 [P] [US1] Write test_valid_query (200 response with required fields) in tests/contract/test_chat_endpoint.py
- [ ] T023 [P] [US1] Write test_response_structure (answer, sources, request_id, tokens_used present) in tests/contract/test_chat_endpoint.py

### Data Models for User Story 1

- [ ] T024 [P] [US1] Create backend/src/models/chat.py with ChatRequest model (query, top_k, similarity_threshold, user_id, metadata)
- [ ] T025 [P] [US1] Create RetrievalResult model in backend/src/models/chat.py (chunk_id, text, similarity_score, source_url, section_title, rank)
- [ ] T026 [P] [US1] Create ChatResponse model in backend/src/models/chat.py (request_id, answer, sources, context_used, tokens_used, response_time_ms, timestamp, note)
- [ ] T027 [P] [US1] Add validation rules to ChatRequest (query non-empty, top_k ∈ [1,20], threshold ∈ [0.0, 1.0])

### Agent Core for User Story 1

- [ ] T028 [US1] Create backend/src/agent/__init__.py with package exports
- [ ] T029 [US1] Create backend/src/agent/prompts.py with constraint system prompt: "You MUST only use the provided context. Do not use external knowledge. If context is insufficient, say so."
- [ ] T030 [US1] Create backend/src/agent/rag_agent.py with RAGAgent class initializing OpenAI Agents SDK
- [ ] T031 [US1] Implement RAGAgent.generate_response(context, query) using OpenAI Agents SDK with constraint prompt
- [ ] T032 [US1] Add token counting to RAGAgent.generate_response (ensure response + context < 6000 tokens)
- [ ] T033 [US1] Create backend/src/agent/orchestrator.py with RAGOrchestrator class for request → retrieval → generation flow
- [ ] T034 [US1] Implement RAGOrchestrator.process_query(chat_request) orchestrating: query validation → context retrieval → token checking → generation
- [ ] T035 [US1] Add context assembly in RAGOrchestrator (rank chunks by similarity, include until token limit, validate threshold)

### Retrieval Integration for User Story 1

- [ ] T036 [US1] Integrate Feature 003 QueryEmbedder in RAGOrchestrator for query embedding (embed_query method)
- [ ] T037 [US1] Integrate Feature 003 QdrantRetriever in RAGOrchestrator for similarity search (search_similar method)
- [ ] T038 [US1] Implement error handling for Qdrant unavailability in RAGOrchestrator (return 503 error)
- [ ] T039 [US1] Add token counting integration (tiktoken) in backend/src/tokens.py for context assembly

### API Implementation for User Story 1

- [ ] T040 [P] [US1] Create backend/src/chat/__init__.py with package exports
- [ ] T041 [US1] Create backend/src/chat/models.py with Pydantic schemas (ChatRequest, ChatResponse, ErrorResponse)
- [ ] T042 [US1] Create backend/src/chat/api.py with FastAPI POST /chat endpoint
- [ ] T043 [US1] Implement POST /chat endpoint handler: validate request → call RAGOrchestrator → return ChatResponse
- [ ] T044 [US1] Add request ID tracking to POST /chat response (UUID4 in request_id field)
- [ ] T045 [US1] Add response time measurement to POST /chat (response_time_ms field)
- [ ] T046 [P] [US1] Implement GET /health endpoint returning {"status": "ok", "timestamp": "..."}
- [ ] T047 [P] [US1] Implement GET /docs endpoint (auto-generated by FastAPI, serves OpenAPI schema)

### Integration Tests for User Story 1

- [ ] T048 [US1] Create tests/integration/test_query_assistant.py with end-to-end test: query → retrieval → generation → response
- [ ] T049 [US1] Write test_successful_query (query about book content, verify answer is grounded) in tests/integration/
- [ ] T050 [US1] Write test_query_with_high_similarity (query returns chunks with score ≥0.7) in tests/integration/
- [ ] T051 [US1] Write test_response_includes_sources (answer, sources, similarity_scores, request_id all present) in tests/integration/
- [ ] T052 [US1] Write test_out_of_scope_query (question outside book scope, return "I don't have information...") in tests/integration/

### Unit Tests for User Story 1

- [ ] T053 [P] [US1] Create tests/agent/test_rag_agent.py testing RAGAgent.generate_response with constraint prompt
- [ ] T054 [P] [US1] Create tests/agent/test_orchestrator.py testing RAGOrchestrator.process_query flow
- [ ] T055 [P] [US1] Create tests/chat/test_models.py testing ChatRequest/ChatResponse validation
- [ ] T056 [P] [US1] Create tests/chat/test_api.py testing POST /chat endpoint request/response
- [ ] T057 [P] [US1] Create tests/tokens/test_token_counting.py testing count_tokens accuracy
- [ ] T058 [US1] Write test_constraint_prompt_enforced (mock LLM, verify system prompt is constraint-based) in tests/agent/

**Checkpoint**: User Story 1 is fully functional and testable independently - can be deployed as MVP

---

## Phase 4: User Story 2 - Error Handling for Empty or Irrelevant Results (Priority: P2)

**Goal**: Implement graceful error handling for cases where no relevant context is found, ensuring no hallucination and friendly error messages.

**Independent Test**:
1. POST query with no relevant results (e.g., "What is the weather today?") to `/chat`
2. Verify response includes error message: "I don't have information about this topic"
3. Verify HTTP status 200 with note field, not error response
4. Verify no hallucination (agent doesn't fabricate answer)
5. Test malformed request (empty query, invalid top_k) returns HTTP 400
6. Test unreachable Qdrant returns HTTP 503

### Error Handling Models for User Story 2

- [ ] T059 [P] [US2] Create ErrorResponse model in backend/src/models/chat.py (error, details, request_id, timestamp)
- [ ] T059b [P] [US2] Create ErrorDetail model in backend/src/models/chat.py (field, message for validation errors)
- [ ] T060 [P] [US2] Add validation error handler in backend/src/main.py returning HTTP 400 with field-level errors

### Validation for User Story 2

- [ ] T061 [US2] Implement query validation in RAGOrchestrator: non-empty, non-whitespace, reasonable length
- [ ] T062 [US2] Add validation exception handling in POST /chat returning HTTP 400 with field-specific errors
- [ ] T063 [P] [US2] Create tests/contract/test_error_responses.py with error response schema validation

### Empty Results Handling for User Story 2

- [ ] T064 [US2] Implement no-context detection in RAGOrchestrator: all chunks with similarity <threshold (default 0.5)
- [ ] T065 [US2] Create friendly message handler in RAGOrchestrator returning "I don't have information about this topic in the provided materials"
- [ ] T066 [US2] Add note field to ChatResponse when results are below threshold or limited
- [ ] T067 [US2] Return HTTP 200 with empty sources for no-context queries (not error response)

### Qdrant Error Handling for User Story 2

- [ ] T068 [US2] Implement Qdrant connection timeout handling (return HTTP 503)
- [ ] T069 [US2] Implement empty collection detection (return HTTP 503 with "Collection not found or empty")
- [ ] T070 [US2] Add circuit breaker pattern for Qdrant client in RAGOrchestrator (max 3 retries, exponential backoff)

### OpenAI API Error Handling for User Story 2

- [ ] T071 [US2] Implement OpenAI rate limit handling (return HTTP 429 with "Too Many Requests")
- [ ] T072 [US2] Implement OpenAI timeout handling (return HTTP 503 with "OpenAI service temporarily unavailable")
- [ ] T073 [US2] Add circuit breaker for OpenAI client (max 3 retries, exponential backoff)

### Error Handling Tests for User Story 2

- [ ] T074 [P] [US2] Create tests/integration/test_error_handling.py with error case tests
- [ ] T075 [P] [US2] Write test_empty_query_returns_400 (empty query validation) in tests/integration/
- [ ] T076 [P] [US2] Write test_malformed_request_returns_400 (invalid top_k/threshold) in tests/integration/
- [ ] T077 [P] [US2] Write test_no_relevant_chunks_returns_friendly_message in tests/integration/
- [ ] T078 [P] [US2] Write test_qdrant_unavailable_returns_503 (mocked Qdrant error) in tests/integration/
- [ ] T079 [P] [US2] Write test_openai_rate_limit_returns_429 (mocked OpenAI error) in tests/integration/
- [ ] T080 [P] [US2] Write test_no_hallucination_on_empty_results in tests/integration/
- [ ] T081 [US2] Create tests/agent/test_error_handling.py with unit tests for error paths

**Checkpoint**: User Stories 1 and 2 both work independently - can deploy with error handling

---

## Phase 5: User Story 3 - Performance and Safety Within Token Limits (Priority: P3)

**Goal**: Implement token limit management and response latency optimization to ensure cost-effective and responsive operation.

**Independent Test**:
1. POST query with many relevant chunks to `/chat`, verify context assembly respects 6000 token limit
2. Verify response includes tokens_used and response_time_ms fields
3. Verify response time <3s for typical queries (p95)
4. Verify token usage <6000 for 95% of requests
5. Verify no conversation state retention (each request independent)

### Token Management Models for User Story 3

- [ ] T082 [P] [US3] Create ContextWindow model in backend/src/models/chat.py (max_tokens=6000, reserved_for_response=1500, chunk_ordering="similarity")
- [ ] T083 [P] [US3] Add token usage tracking to ChatResponse (tokens_used field for token accounting)

### Token Limit Enforcement for User Story 3

- [ ] T084 [US3] Implement token budget calculation in RAGOrchestrator: query + response + context tokens
- [ ] T085 [US3] Implement context assembly limiting in RAGOrchestrator: include top-K chunks until budget exhausted
- [ ] T086 [US3] Add token counting before LLM call (prevent oversized context)
- [ ] T087 [US3] Implement graceful degradation: drop lower-ranked chunks if exceeding limit
- [ ] T088 [US3] Add note to ChatResponse when results omitted: "Some results were omitted to respect token limits"

### Latency Optimization for User Story 3

- [ ] T089 [US3] Implement async I/O in RAGOrchestrator for concurrent Qdrant search
- [ ] T090 [US3] Add timeout enforcement in POST /chat (max 3 seconds from request to response)
- [ ] T091 [US3] Profile and optimize hot paths (query embedding, similarity search, token counting)
- [ ] T092 [US3] Add response_time_ms tracking to ChatResponse (measure request → response latency)

### Stateless Design Verification for User Story 3

- [ ] T093 [US3] Verify no session state stored in RAGOrchestrator (each request independent)
- [ ] T094 [US3] Verify no conversation history retention (context not accumulated across requests)
- [ ] T095 [US3] Add test for statelessness: same query twice returns same answer (no state leakage)

### Performance Tests for User Story 3

- [ ] T096 [P] [US3] Create tests/performance/test_latency.py measuring response_time_ms
- [ ] T097 [P] [US3] Write test_p95_latency_under_3s (20+ queries, measure p95 latency) in tests/performance/
- [ ] T098 [P] [US3] Create tests/performance/test_token_usage.py measuring tokens_used
- [ ] T099 [P] [US3] Write test_token_usage_under_6000 (verify 95% of requests <6000 tokens) in tests/performance/
- [ ] T100 [P] [US3] Create tests/performance/test_concurrent_load.py with 10+ concurrent request handling
- [ ] T101 [P] [US3] Write test_concurrent_requests_no_degradation (10+ concurrent, measure latency) in tests/performance/

### Stateless Design Tests for User Story 3

- [ ] T102 [US3] Create tests/integration/test_stateless_design.py verifying no state retention
- [ ] T103 [US3] Write test_same_query_twice_same_answer (verify statelessness) in tests/integration/
- [ ] T104 [US3] Write test_no_conversation_history (each request independent context) in tests/integration/

**Checkpoint**: All user stories (P1, P2, P3) are complete and independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories, documentation, and quality assurance

- [ ] T105 [P] Create comprehensive API documentation in README.md (setup, usage, examples, errors)
- [ ] T106 [P] Create quickstart.md with step-by-step guide to run agent and test POST /chat
- [ ] T107 [P] Write sample cURL tests in examples/curl_tests.sh (successful query, error cases)
- [ ] T108 [P] Create OpenAPI specification in specs/004-rag-agent-api/contracts/openapi.json
- [ ] T109 [P] Create request/response examples in specs/004-rag-agent-api/contracts/request-response.md
- [ ] T110 [P] Add comprehensive docstrings to all modules (agent/, chat/, config.py, tokens.py)
- [ ] T111 [P] Run final integration test suite (all tests/integration/ pass)
- [ ] T112 [P] Run performance benchmarks (latency, tokens, concurrency) and document results
- [ ] T113 [P] Validate against success criteria (SC-001 through SC-010)
- [ ] T114 [P] Code cleanup and refactoring (remove dead code, improve error messages)
- [ ] T115 Run final validation against all acceptance scenarios from spec.md
- [ ] T116 Create DEPLOYMENT.md with instructions for deploying to production (env vars, scaling, monitoring)
- [ ] T117 [P] Add request/response logging sanitization (don't log sensitive query content)
- [ ] T118 [P] Add metrics collection (optional: request count, latency percentiles, error rates)
- [ ] T119 Commit all changes with message: "feat: implement RAG Agent API (Feature 004) - MVP complete"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - P1 MVP core
- **User Story 2 (Phase 4)**: Depends on Foundational (US1 helpful but not required)
- **User Story 3 (Phase 5)**: Depends on Foundational (US1, US2 helpful but not required)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (Query Assistant)**: Can start after Foundational - No dependencies on other stories
- **US2 (Error Handling)**: Can start after Foundational - Enhances US1 but independent
- **US3 (Token Management)**: Can start after Foundational - Enhances US1/US2 but independent

### Within Each Phase

- Tests (contract/integration) MUST be written and FAIL before implementation
- Data models before services
- Services before API endpoints
- Core logic before optimization
- Each story complete before moving to next priority

### Parallel Opportunities

**Phase 1 Setup**: All [P] tasks can run in parallel
```
T002, T003, T004, T005, T007, T008 - all can run concurrently
```

**Phase 2 Foundational**: All [P] tasks can run in parallel
```
T009-T017 - config, logging, tokens, models (all independent)
T019 - mock factories (after T018)
```

**Phase 3 US1**: Models and tests in parallel, then API
```
Parallel: T020-T027 (contract tests, data models)
Then: T028-T047 (agent core, API implementation)
Then: T048-T058 (integration and unit tests)
```

**Phase 4 US2**: Error handling tasks in parallel
```
Parallel: T059-T063 (error models, validation)
Parallel: T064-T073 (empty results, Qdrant, OpenAI error handling)
Parallel: T074-T081 (error tests)
```

**Phase 5 US3**: Token and performance tasks in parallel
```
Parallel: T082-T083 (models)
Parallel: T084-T095 (token limits, latency, stateless)
Parallel: T096-T104 (performance and stateless tests)
```

**Phase 6 Polish**: Documentation and final validation in parallel
```
Parallel: T105-T110 (docs, examples, OpenAPI)
Parallel: T111-T119 (tests, validation, cleanup, deployment)
```

---

## Parallel Example: Full Team

```
Team Setup (2-3 developers, 1-2 hours):
├─ Developer A: T001-T008 (Setup)
├─ Developer B: T009-T017 (Foundational - can start after T008)
└─ Developer C: Prep environment and review plan

Team US1 (2-3 developers, 4-6 hours):
├─ Developer A: T020-T027 (Contract tests & models, 2h)
├─ Developer B: T028-T039 (Agent core & retrieval, 3h)
├─ Developer C: T040-T047 (API endpoints, 2h)
└─ All: T048-T058 (Integration/unit tests, 2h)

Team US2+US3 (parallel, 2-3 developers, 4-6 hours):
├─ Developer A: User Story 2 (T059-T081)
├─ Developer B: User Story 3 (T082-T104)
└─ Developer C: Polish & validation (T105-T119)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (2h)
2. Complete Phase 2: Foundational (2h)
3. Complete Phase 3: User Story 1 (6h)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy MVP if ready

**MVP Timeline**: ~10 hours for functional RAG agent

### Incremental Delivery

1. Setup + Foundational → Foundation ready (4h)
2. Add US1 → Test independently → Deploy MVP (6h)
3. Add US2 → Test independently → Deploy v1.1 (6h)
4. Add US3 → Test independently → Deploy v1.2 (6h)
5. Polish & validation (4h)

**Full Timeline**: ~26 hours for complete Feature 004

---

## Notes

- Tasks with [P] = parallelizable (different files, no dependencies within phase)
- Tasks with [Story] = belong to specific user story (US1, US2, US3)
- Each checkpoint represents a complete, deployable increment
- Tests (contract/integration) MUST be written before implementation
- Use Feature 003 predefined_queries.json for test data consistency
- Commit after each task or logical group
- Avoid vague tasks, file conflicts, and cross-story dependencies that break independence
- If stuck: validate against plan.md architecture decisions (AD-001 through AD-006)

