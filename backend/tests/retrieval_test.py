"""
Test suite for retrieval validation.

Tests the core retrieval functionality with predefined sample queries
and mock Cohere + Qdrant APIs.
"""

import json
import logging
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from retrieve import QueryEmbedder, QdrantRetriever, ContextExtractor


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_cohere_key():
    """Mock Cohere API key."""
    return "test-cohere-key-123"


@pytest.fixture
def mock_qdrant_url():
    """Mock Qdrant URL."""
    return "https://test-qdrant.example.com"


@pytest.fixture
def mock_qdrant_key():
    """Mock Qdrant API key."""
    return "test-qdrant-key-456"


@pytest.fixture
def sample_queries():
    """Sample test queries covering major book topics."""
    return [
        {
            "id": "q1",
            "text": "What is physical AI?",
            "topic": "foundational",
            "difficulty": "easy"
        },
        {
            "id": "q2",
            "text": "Explain kinematics and dynamics in humanoid robots",
            "topic": "mechanics",
            "difficulty": "medium"
        },
        {
            "id": "q3",
            "text": "What are the steps to set up a ROS 2 environment?",
            "topic": "setup",
            "difficulty": "medium"
        },
        {
            "id": "q4",
            "text": "How do you implement feedback control?",
            "topic": "control",
            "difficulty": "hard"
        },
        {
            "id": "q5",
            "text": "What is reinforcement learning?",
            "topic": "learning",
            "difficulty": "medium"
        },
        {
            "id": "q6",
            "text": "Describe the sim-to-real transfer problem",
            "topic": "simulation",
            "difficulty": "hard"
        },
        {
            "id": "q7",
            "text": "How do you use Gazebo for simulation?",
            "topic": "simulation",
            "difficulty": "medium"
        },
        {
            "id": "q8",
            "text": "What safety precautions are needed for humanoid robots?",
            "topic": "safety",
            "difficulty": "medium"
        },
        {
            "id": "q9",
            "text": "Explain imitation learning with examples",
            "topic": "learning",
            "difficulty": "hard"
        },
        {
            "id": "q10",
            "text": "What are the key differences between ROS 1 and ROS 2?",
            "topic": "middleware",
            "difficulty": "medium"
        }
    ]


@pytest.fixture
def mock_query_embedding():
    """Mock 4096-dimensional query embedding."""
    return [0.5] * 4096


@pytest.fixture
def mock_retrieval_results():
    """Mock retrieval results from Qdrant."""
    return [
        {
            "rank": 1,
            "similarity_score": 0.89,
            "chunk_id": "chunk_001",
            "source_url": "https://book.example.com/docs/01-fundamentals/physical-ai",
            "section_title": "Introduction to Physical AI",
            "text_excerpt": "Physical AI is the branch of artificial intelligence that deals with embodied systems..."
        },
        {
            "rank": 2,
            "similarity_score": 0.82,
            "chunk_id": "chunk_002",
            "source_url": "https://book.example.com/docs/01-fundamentals/embodied-intelligence",
            "section_title": "Embodied Intelligence Concepts",
            "text_excerpt": "Embodied intelligence refers to the intelligence that arises from having a body..."
        },
        {
            "rank": 3,
            "similarity_score": 0.76,
            "chunk_id": "chunk_003",
            "source_url": "https://book.example.com/docs/02-humanoid-robotics/overview",
            "section_title": "Humanoid Robotics Overview",
            "text_excerpt": "Humanoid robots are designed to mimic human form and behavior..."
        }
    ]


# ============================================================================
# QueryEmbedder Tests
# ============================================================================

class TestQueryEmbedder:
    """Test suite for QueryEmbedder class."""

    def test_init(self, mock_cohere_key):
        """Test QueryEmbedder initialization."""
        embedder = QueryEmbedder(api_key=mock_cohere_key)
        assert embedder.api_key == mock_cohere_key
        assert embedder.model == "embed-3-large"
        assert embedder.batch_size == 8

    def test_embed_query_empty_string(self, mock_cohere_key):
        """Test that empty query raises ValueError."""
        embedder = QueryEmbedder(api_key=mock_cohere_key)
        with pytest.raises(ValueError, match="Query must be non-empty"):
            embedder.embed_query("")

    def test_embed_query_too_short(self, mock_cohere_key):
        """Test that too-short query raises ValueError."""
        embedder = QueryEmbedder(api_key=mock_cohere_key)
        with pytest.raises(ValueError, match="at least 3 characters"):
            embedder.embed_query("a b")

    @patch('cohere.ClientV2')
    def test_embed_query_success(self, mock_cohere_client, mock_cohere_key, mock_query_embedding):
        """Test successful query embedding."""
        # Mock the Cohere response
        mock_client_instance = MagicMock()
        mock_cohere_client.return_value = mock_client_instance
        mock_client_instance.embed.return_value.embeddings = [mock_query_embedding]

        embedder = QueryEmbedder(api_key=mock_cohere_key)
        result = embedder.embed_query("What is physical AI?")

        assert len(result) == 4096
        assert result == mock_query_embedding
        mock_client_instance.embed.assert_called_once()

    @patch('cohere.ClientV2')
    def test_embed_batch(self, mock_cohere_client, mock_cohere_key, mock_query_embedding):
        """Test batch embedding with multiple queries."""
        mock_client_instance = MagicMock()
        mock_cohere_client.return_value = mock_client_instance

        # Return embeddings for 3 queries
        mock_client_instance.embed.return_value.embeddings = [
            mock_query_embedding,
            mock_query_embedding,
            mock_query_embedding
        ]

        embedder = QueryEmbedder(api_key=mock_cohere_key, batch_size=2)
        queries = ["Query 1", "Query 2", "Query 3"]
        results = embedder.embed_batch(queries)

        assert len(results) == 3
        assert all(len(emb) == 4096 for emb in results)


# ============================================================================
# QdrantRetriever Tests
# ============================================================================

class TestQdrantRetriever:
    """Test suite for QdrantRetriever class."""

    def test_init(self, mock_qdrant_url, mock_qdrant_key):
        """Test QdrantRetriever initialization."""
        retriever = QdrantRetriever(url=mock_qdrant_url, api_key=mock_qdrant_key)
        assert retriever.url == mock_qdrant_url
        assert retriever.api_key == mock_qdrant_key
        assert retriever.collection_name == "book_embeddings"

    @patch('qdrant_client.QdrantClient')
    def test_verify_collection_exists(self, mock_qdrant_client, mock_qdrant_url, mock_qdrant_key):
        """Test collection verification."""
        mock_client_instance = MagicMock()
        mock_qdrant_client.return_value = mock_client_instance

        # Mock collection info response
        mock_collection_info = MagicMock()
        mock_collection_info.points_count = 1000
        mock_client_instance.get_collection.return_value = mock_collection_info

        retriever = QdrantRetriever(url=mock_qdrant_url, api_key=mock_qdrant_key)
        result = retriever.verify_collection_exists()

        assert result is True
        mock_client_instance.get_collection.assert_called_once()

    @patch('qdrant_client.QdrantClient')
    def test_verify_empty_collection(self, mock_qdrant_client, mock_qdrant_url, mock_qdrant_key):
        """Test that empty collection raises error."""
        mock_client_instance = MagicMock()
        mock_qdrant_client.return_value = mock_client_instance

        mock_collection_info = MagicMock()
        mock_collection_info.points_count = 0
        mock_client_instance.get_collection.return_value = mock_collection_info

        retriever = QdrantRetriever(url=mock_qdrant_url, api_key=mock_qdrant_key)

        with pytest.raises(ValueError, match="is empty"):
            retriever.verify_collection_exists()

    @patch('qdrant_client.QdrantClient')
    def test_search_similar_invalid_vector(self, mock_qdrant_client, mock_qdrant_url, mock_qdrant_key):
        """Test that invalid vector dimension raises error."""
        mock_client_instance = MagicMock()
        mock_qdrant_client.return_value = mock_client_instance

        retriever = QdrantRetriever(url=mock_qdrant_url, api_key=mock_qdrant_key)
        invalid_vector = [0.5] * 3000  # Wrong dimension

        with pytest.raises(ValueError, match="4096-D"):
            retriever.search_similar(invalid_vector)

    @patch('qdrant_client.QdrantClient')
    def test_search_similar_success(self, mock_qdrant_client, mock_qdrant_url, mock_qdrant_key,
                                     mock_query_embedding, mock_retrieval_results):
        """Test successful similarity search."""
        mock_client_instance = MagicMock()
        mock_qdrant_client.return_value = mock_client_instance

        # Mock search results
        mock_points = []
        for result in mock_retrieval_results:
            mock_point = MagicMock()
            mock_point.score = result["similarity_score"]
            mock_point.payload = {
                "chunk_id": result["chunk_id"],
                "url": result["source_url"],
                "section_title": result["section_title"],
                "text": result["text_excerpt"]
            }
            mock_points.append(mock_point)

        mock_client_instance.search.return_value = mock_points

        retriever = QdrantRetriever(url=mock_qdrant_url, api_key=mock_qdrant_key)
        results = retriever.search_similar(mock_query_embedding, top_k=3)

        assert len(results) == 3
        assert results[0]["rank"] == 1
        assert results[0]["similarity_score"] == 0.89
        assert results[0]["chunk_id"] == "chunk_001"


# ============================================================================
# ContextExtractor Tests
# ============================================================================

class TestContextExtractor:
    """Test suite for ContextExtractor class."""

    def test_extract_context_empty(self):
        """Test extracting context from empty results."""
        result = ContextExtractor.extract_context([])
        assert result == "No context found"

    def test_extract_context_single_result(self, mock_retrieval_results):
        """Test extracting context from single result."""
        result = ContextExtractor.extract_context([mock_retrieval_results[0]])
        assert len(result) > 0
        assert "Physical AI" in result

    def test_extract_context_multiple_results(self, mock_retrieval_results):
        """Test extracting context from multiple results."""
        result = ContextExtractor.extract_context(mock_retrieval_results)
        assert len(result) > 0
        assert "Physical AI" in result or "Embodied" in result or "Humanoid" in result

    def test_extract_context_max_length(self, mock_retrieval_results):
        """Test that context respects max_length."""
        result = ContextExtractor.extract_context(mock_retrieval_results, max_length=50)
        assert len(result) <= 53  # 50 + "..."

    def test_format_results_empty(self):
        """Test formatting empty results."""
        result = ContextExtractor.format_results([])
        assert result == "No results found"

    def test_format_results_with_results(self, mock_retrieval_results):
        """Test formatting retrieval results."""
        result = ContextExtractor.format_results(mock_retrieval_results)
        assert "Rank 1" in result
        assert "0.89" in result
        assert "chunk_001" in result


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests with mocked APIs."""

    @patch('qdrant_client.QdrantClient')
    @patch('cohere.ClientV2')
    def test_end_to_end_validation(self, mock_cohere_client, mock_qdrant_client,
                                     mock_cohere_key, mock_qdrant_url, mock_qdrant_key,
                                     sample_queries, mock_query_embedding, mock_retrieval_results):
        """Test end-to-end validation flow."""
        # Setup mocks
        mock_cohere_instance = MagicMock()
        mock_cohere_client.return_value = mock_cohere_instance
        mock_cohere_instance.embed.return_value.embeddings = [mock_query_embedding]

        mock_qdrant_instance = MagicMock()
        mock_qdrant_client.return_value = mock_qdrant_instance

        mock_collection_info = MagicMock()
        mock_collection_info.points_count = 1000
        mock_qdrant_instance.get_collection.return_value = mock_collection_info

        # Mock search results
        mock_points = []
        for result in mock_retrieval_results:
            mock_point = MagicMock()
            mock_point.score = result["similarity_score"]
            mock_point.payload = {
                "chunk_id": result["chunk_id"],
                "url": result["source_url"],
                "section_title": result["section_title"],
                "text": result["text_excerpt"]
            }
            mock_points.append(mock_point)

        mock_qdrant_instance.search.return_value = mock_points

        # Run validation
        embedder = QueryEmbedder(api_key=mock_cohere_key)
        retriever = QdrantRetriever(url=mock_qdrant_url, api_key=mock_qdrant_key)

        # Test a few sample queries
        for query in sample_queries[:3]:
            embedding = embedder.embed_query(query["text"])
            assert len(embedding) == 4096

            results = retriever.search_similar(embedding, top_k=3)
            assert len(results) > 0
            assert results[0]["similarity_score"] >= 0.7


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
