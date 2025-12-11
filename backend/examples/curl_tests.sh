#!/bin/bash

# Sample cURL tests for RAG Agent API (/ask endpoint)
# Usage: bash curl_tests.sh
# Assumes API running at http://localhost:8000

API_URL="http://localhost:8000"

echo "======================================================================"
echo "RAG Agent API - cURL Test Suite"
echo "======================================================================"
echo ""

# Test 1: Health Check
echo "[TEST 1] Health Check"
echo "GET $API_URL/health"
echo ""
curl -X GET "$API_URL/health" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 2: Simple Query
echo "[TEST 2] Simple Query - What is physical AI?"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is physical AI?",
    "top_k": 5,
    "similarity_threshold": 0.7
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 3: Query with User ID
echo "[TEST 3] Query with User ID and Session"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain kinematics and dynamics in humanoid robots",
    "top_k": 3,
    "similarity_threshold": 0.5,
    "user_id": "user_123",
    "session_id": "session_456"
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 4: Complex Query
echo "[TEST 4] Complex Query - Learning Methods"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main approaches to reinforcement learning in robotics?",
    "top_k": 5,
    "similarity_threshold": 0.6
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 5: Out-of-Scope Query (should return no results)
echo "[TEST 5] Out-of-Scope Query - Stock Market"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current stock market?",
    "top_k": 5,
    "similarity_threshold": 0.7
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 6: Empty Query (should return 400 error)
echo "[TEST 6] ERROR TEST - Empty Query"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "",
    "top_k": 5
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 7: Invalid top_k (should return 400 error)
echo "[TEST 7] ERROR TEST - Invalid top_k (0)"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is physical AI?",
    "top_k": 0
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 8: Invalid similarity_threshold (should return 400 error)
echo "[TEST 8] ERROR TEST - Invalid similarity_threshold (1.5)"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is physical AI?",
    "similarity_threshold": 1.5
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 9: Whitespace-only Query (should return error)
echo "[TEST 9] ERROR TEST - Whitespace-only Query"
echo "POST $API_URL/ask"
echo ""
curl -X POST "$API_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "   \n\t  ",
    "top_k": 5
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 10: Multiple Queries (Performance Test)
echo "[TEST 10] Performance Test - Multiple Queries"
echo ""
for i in {1..3}; do
  echo "Query $i of 3..."
  curl -s -X POST "$API_URL/ask" \
    -H "Content-Type: application/json" \
    -d '{
      "query": "What is physical AI?",
      "top_k": 5
    }' | jq '.response_time_ms'
done

echo ""
echo "======================================================================"
echo "Test Suite Complete"
echo "======================================================================"
echo ""
echo "Expected Results:"
echo "  Test 1-4: HTTP 200 (success)"
echo "  Test 5: HTTP 200 with empty sources and friendly message"
echo "  Test 6: HTTP 400 (validation error - empty query)"
echo "  Test 7: HTTP 400 or 422 (validation error - invalid top_k)"
echo "  Test 8: HTTP 400 or 422 (validation error - invalid threshold)"
echo "  Test 9: HTTP 400 or 422 (validation error - whitespace)"
echo "  Test 10: Response times should be <3000ms (3 seconds)"
echo ""

# Optional: Pretty-print a sample response
echo ""
echo "======================================================================"
echo "Sample Successful Response Format:"
echo "======================================================================"
cat << 'EOF'
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "answer": "Physical AI refers to artificial intelligence systems embodied in physical agents like robots...",
  "sources": [
    {
      "chunk_id": "chunk_001",
      "text": "Physical AI is the study of AI in physical systems...",
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
EOF

echo ""
