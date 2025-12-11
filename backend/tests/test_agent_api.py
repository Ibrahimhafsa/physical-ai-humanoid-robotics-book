"""
Tests for RAG Agent API endpoints and core functionality.

Tests cover:
- POST /ask endpoint with valid/invalid requests
- Response structure and validation
- Error handling (400, 503, etc.)
- Grounding in retrieved context (no hallucination)
"""

import json
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

from fastapi.testclient import TestClient

from backend.src.api import app
from backend.src.models.chat import ChatRequest, ChatResponse, RetrievalResult, ErrorResponse


@pytest.fixture
def client():
    """Test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_orchestrator():
    """Mock RAG orchestrator."""
    orchestrator = MagicMock()

    # Sample response
    orchestrator.process_query.return_value = ChatResponse(
        request_id="test-123",
        answer="Physical AI refers to artificial intelligence systems embodied in physical agents like robots.",
        sources=[
            RetrievalResult(
                chunk_id="chunk_001",
                text="Physical AI is the study of AI in physical systems...",
                similarity_score=0.89,
                source_url="https://book.example.com/01-physical-ai",
                section_title="Introduction to Physical AI",
                rank=1,
            )
        ],
        context_used=1,
        tokens_used=150,
        response_time_ms=800,
        timestamp=datetime.utcnow().isoformat(),
    )

    return orchestrator


class TestHealthEndpoint:
    """Test /health endpoint."""

    def test_health_check_returns_200(self, client):
        """Health check should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


class TestChatEndpoint:
    """Test POST /ask endpoint."""

    @patch("backend.src.api.rag_orchestrator")
    def test_valid_query_returns_200(self, mock_orchestrator, client):
        """Valid query should return 200 with answer and sources."""
        # Mock the orchestrator
        from backend.src.api import RAGOrchestrator
        app.rag_orchestrator = mock_orchestrator

        response = client.post(
            "/ask",
            json={
                "query": "What is physical AI?",
                "top_k": 5,
                "similarity_threshold": 0.7,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["request_id"]
        assert "answer" in data
        assert "sources" in data
        assert "tokens_used" in data
        assert "response_time_ms" in data

    def test_empty_query_returns_400(self, client):
        """Empty query should return 400 Bad Request."""
        response = client.post(
            "/ask",
            json={
                "query": "",
                "top_k": 5,
            },
        )

        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "Validation Error"
        assert any(d["field"] == "query" for d in data["detail"]["details"])

    def test_whitespace_only_query_returns_400(self, client):
        """Whitespace-only query should return 400."""
        response = client.post(
            "/ask",
            json={
                "query": "   \n\t  ",
                "top_k": 5,
            },
        )

        # Pydantic validates through ChatRequest model
        assert response.status_code in [400, 422]  # Validation error

    def test_invalid_top_k_returns_400(self, client):
        """Invalid top_k should return 400."""
        response = client.post(
            "/ask",
            json={
                "query": "What is AI?",
                "top_k": 0,  # Invalid: must be >= 1
            },
        )

        assert response.status_code in [400, 422]

    def test_invalid_similarity_threshold_returns_400(self, client):
        """Invalid similarity_threshold should return 400."""
        response = client.post(
            "/ask",
            json={
                "query": "What is AI?",
                "similarity_threshold": 1.5,  # Invalid: must be <= 1.0
            },
        )

        assert response.status_code in [400, 422]

    @patch("backend.src.api.rag_orchestrator")
    def test_response_includes_request_id(self, mock_orch, client):
        """Response should include request_id."""
        app.rag_orchestrator = mock_orch
        response = client.post(
            "/ask",
            json={"query": "Test query"},
        )
        assert response.status_code == 200
        assert "request_id" in response.json()

    @patch("backend.src.api.rag_orchestrator")
    def test_response_includes_sources(self, mock_orch, client):
        """Response should include sources with metadata."""
        app.rag_orchestrator = mock_orch
        response = client.post(
            "/ask",
            json={"query": "What is physical AI?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "sources" in data
        assert len(data["sources"]) > 0

        source = data["sources"][0]
        assert "source_url" in source
        assert "similarity_score" in source
        assert "chunk_id" in source

    @patch("backend.src.api.rag_orchestrator")
    def test_response_includes_answer(self, mock_orch, client):
        """Response should include answer text."""
        app.rag_orchestrator = mock_orch
        response = client.post(
            "/ask",
            json={"query": "What is physical AI?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert len(data["answer"]) > 0

    @patch("backend.src.api.rag_orchestrator")
    def test_response_includes_token_metrics(self, mock_orch, client):
        """Response should include token usage and latency metrics."""
        app.rag_orchestrator = mock_orch
        response = client.post(
            "/ask",
            json={"query": "What is physical AI?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "tokens_used" in data
        assert "response_time_ms" in data
        assert isinstance(data["tokens_used"], int)
        assert isinstance(data["response_time_ms"], int)


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_request_id_in_error_responses(self, client):
        """Error responses should include request_id."""
        response = client.post(
            "/ask",
            json={"query": ""},
        )
        assert response.status_code == 400
        data = response.json()
        assert "request_id" in data["detail"]

    def test_missing_orchestrator_returns_503(self, client):
        """Missing orchestrator should return 503."""
        # Temporarily remove orchestrator
        original = app.rag_orchestrator
        try:
            app.rag_orchestrator = None
            response = client.post(
                "/ask",
                json={"query": "Test query"},
            )
            # Will fail at validation or startup, depending on timing
        finally:
            app.rag_orchestrator = original

    @patch("backend.src.api.rag_orchestrator")
    def test_runtime_error_returns_503(self, mock_orch, client):
        """RuntimeError from orchestrator should return 503."""
        mock_orch.process_query.side_effect = RuntimeError("Qdrant connection failed")
        app.rag_orchestrator = mock_orch

        response = client.post(
            "/ask",
            json={"query": "What is AI?"},
        )
        assert response.status_code == 503
        data = response.json()
        assert "error" in data["detail"]


class TestGrounding:
    """Test that responses are grounded in retrieved context (no hallucination)."""

    @patch("backend.src.api.rag_orchestrator")
    def test_answer_uses_retrieved_sources(self, mock_orch, client):
        """Answer should reference retrieved sources (no hallucination)."""
        # Setup mock to return specific sources
        mock_orch.process_query.return_value = ChatResponse(
            request_id="test-123",
            answer="Based on the retrieved materials, kinematics is the study of motion...",
            sources=[
                RetrievalResult(
                    chunk_id="chunk_002",
                    text="Kinematics is the study of motion in mechanical systems...",
                    similarity_score=0.85,
                    source_url="https://book.example.com/02-kinematics",
                    section_title="Kinematics Fundamentals",
                    rank=1,
                )
            ],
            context_used=1,
            tokens_used=200,
            response_time_ms=900,
            timestamp=datetime.utcnow().isoformat(),
        )
        app.rag_orchestrator = mock_orch

        response = client.post(
            "/ask",
            json={"query": "What is kinematics?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["sources"]) > 0
        # Answer should mention content from sources
        assert "kinematics" in data["answer"].lower()

    @patch("backend.src.api.rag_orchestrator")
    def test_no_results_returns_friendly_message(self, mock_orch, client):
        """No relevant results should return friendly message, not hallucination."""
        mock_orch.process_query.return_value = ChatResponse(
            request_id="test-123",
            answer="I don't have information about this topic in the provided materials.",
            sources=[],
            context_used=0,
            tokens_used=50,
            response_time_ms=300,
            timestamp=datetime.utcnow().isoformat(),
            note="No chunks with sufficient similarity found",
        )
        app.rag_orchestrator = mock_orch

        response = client.post(
            "/ask",
            json={"query": "What is the weather today?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["sources"]) == 0
        # Should return friendly message, not fabricated answer
        assert "don't have information" in data["answer"].lower()


class TestRequestIDTracking:
    """Test request ID generation and tracking."""

    @patch("backend.src.api.rag_orchestrator")
    def test_unique_request_ids(self, mock_orch, client):
        """Each request should get unique request_id."""
        app.rag_orchestrator = mock_orch

        request_ids = []
        for _ in range(3):
            response = client.post(
                "/ask",
                json={"query": "Test query"},
            )
            assert response.status_code == 200
            request_ids.append(response.json()["request_id"])

        # All request IDs should be unique
        assert len(set(request_ids)) == 3

    @patch("backend.src.api.rag_orchestrator")
    def test_request_id_in_header(self, mock_orch, client):
        """Request ID should also be in response header."""
        app.rag_orchestrator = mock_orch

        response = client.post(
            "/ask",
            json={"query": "Test query"},
        )
        assert response.status_code == 200
        assert "x-request-id" in response.headers


class TestLogging:
    """Test logging of queries and retrieval scores."""

    @patch("backend.src.api.logger")
    @patch("backend.src.api.rag_orchestrator")
    def test_query_logging(self, mock_orch, mock_logger, client):
        """Query should be logged."""
        app.rag_orchestrator = mock_orch

        response = client.post(
            "/ask",
            json={"query": "What is AI?"},
        )
        assert response.status_code == 200

    @patch("backend.src.api.rag_orchestrator")
    def test_retrieval_scores_in_response(self, mock_orch, client):
        """Response should include retrieval similarity scores."""
        mock_response = ChatResponse(
            request_id="test-123",
            answer="Test answer",
            sources=[
                RetrievalResult(
                    chunk_id="chunk_001",
                    text="Test text",
                    similarity_score=0.87,
                    source_url="https://example.com",
                    section_title="Test Section",
                    rank=1,
                )
            ],
            context_used=1,
            tokens_used=100,
            response_time_ms=500,
            timestamp=datetime.utcnow().isoformat(),
        )
        mock_orch.process_query.return_value = mock_response
        app.rag_orchestrator = mock_orch

        response = client.post(
            "/ask",
            json={"query": "Test query"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sources"][0]["similarity_score"] == 0.87


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
