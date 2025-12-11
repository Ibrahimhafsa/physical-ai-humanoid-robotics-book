# RAG Agent API (Feature 004)

Retrieval-Augmented Generation (RAG) Agent API for the AI & Physical Robotics book chatbot.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Configure Environment

Copy `.env.example` to `.env` and set your API keys:

```bash
cp .env.example .env
# Edit .env with your API keys:
# - OPENAI_API_KEY (from OpenAI)
# - COHERE_API_KEY (from Cohere, for embeddings)
# - QDRANT_URL and QDRANT_API_KEY (from Qdrant Cloud)
```

### 3. Run the API Server

```bash
python -m uvicorn backend.src.api:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`

### 4. Test the API

#### Using cURL

```bash
# Simple query
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is physical AI?",
    "top_k": 5,
    "similarity_threshold": 0.7
  }'

# With optional parameters
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain kinematics and dynamics",
    "top_k": 5,
    "similarity_threshold": 0.5,
    "user_id": "user_123"
  }'
```

#### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={
        "query": "What is physical AI?",
        "top_k": 5,
        "similarity_threshold": 0.7,
    }
)

print(response.json())
```

#### Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI

## API Endpoints

### POST /ask

Process user query with retrieval-augmented response.

**Request:**
```json
{
  "query": "What is physical AI?",
  "top_k": 5,
  "similarity_threshold": 0.5,
  "user_id": "optional_user_id",
  "session_id": "optional_session_id",
  "metadata": {}
}
```

**Response:**
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "answer": "Physical AI refers to artificial intelligence systems embodied in physical agents...",
  "sources": [
    {
      "chunk_id": "chunk_001",
      "text": "Physical AI is...",
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

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-12T10:30:00Z"
}
```

### GET /docs

Interactive Swagger UI documentation.

## Error Responses

### 400 Bad Request
- Empty query
- Invalid `top_k` (must be 1-20)
- Invalid `similarity_threshold` (must be 0.0-1.0)

### 503 Service Unavailable
- Qdrant unreachable
- OpenAI API error
- Missing API keys

### 500 Internal Server Error
- Unexpected server error

## Features

✅ **Context-Grounded Responses**
- Agent responds ONLY using retrieved context
- System prompt prevents hallucination
- No external knowledge injection

✅ **Source Attribution**
- Returns similarity scores for all retrieved chunks
- Includes source URLs and section titles
- Enables fact-checking and verification

✅ **Token Management**
- Respects context window limits (6000 tokens default)
- Estimates tokens before LLM call
- Drops lower-relevance chunks if token budget exceeded

✅ **Request Tracking**
- Unique request_id for all responses
- Enables debugging and user support
- Included in error responses

✅ **Structured Logging**
- JSON-formatted logs for monitoring
- Request/response sanitization
- Performance metrics (latency, token usage)

## Running Tests

```bash
pytest tests/test_agent_api.py -v
```

## Integration with Feature 003

This API reuses components from Feature 003 (Book Embedding Pipeline):

- **QueryEmbedder**: Embeds user queries using Cohere API
- **QdrantRetriever**: Searches Qdrant for similar chunks
- **ContextExtractor**: Assembles context from retrieved chunks

## Architecture

```
POST /ask
  ↓
ChatRequest Validation
  ↓
QueryEmbedder (Cohere embeddings)
  ↓
QdrantRetriever (similarity search)
  ↓
ContextExtractor (context assembly)
  ↓
RAGAgent (OpenAI Agents SDK)
  ↓
ChatResponse (answer + sources + metadata)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_API_KEY | required | OpenAI API key |
| OPENAI_MODEL | gpt-3.5-turbo | OpenAI model to use |
| COHERE_API_KEY | required | Cohere embeddings API key |
| QDRANT_URL | http://localhost:6333 | Qdrant server URL |
| QDRANT_API_KEY | optional | Qdrant API key (for cloud) |
| QDRANT_COLLECTION | book_embeddings | Collection name |
| SIMILARITY_THRESHOLD | 0.5 | Minimum similarity score |
| TOP_K | 5 | Number of chunks to retrieve |
| MAX_CONTEXT_TOKENS | 6000 | Context window limit |
| LOG_LEVEL | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Performance Targets

- **Latency**: <3 seconds p95 (including Qdrant + LLM)
- **Token Usage**: <6000 tokens for 95% of requests
- **Concurrent Requests**: Handle 100+ spikes with rate limiting
- **Hallucination Rate**: 0% (context-only generation)

## Next Steps

1. **Integration Testing**: Test with live book content in Qdrant
2. **Performance Tuning**: Monitor latency and token usage
3. **Error Handling**: Implement circuit breakers and retries
4. **Rate Limiting**: Deploy with rate limiting (100 req/min default)
5. **Monitoring**: Setup logging, metrics, and alerting

## Troubleshooting

### Empty Results
- Verify Qdrant collection is populated (Feature 003)
- Check similarity_threshold (default 0.5)
- Verify chunk embeddings match query embedding dimension

### API Errors
- Check OPENAI_API_KEY is set and valid
- Verify Qdrant connection and collection exists
- Review logs: `LOG_LEVEL=DEBUG`

### Slow Responses
- Check network latency to Qdrant and OpenAI
- Reduce TOP_K or increase MAX_CONTEXT_TOKENS
- Profile with `response_time_ms` in response

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Agents API](https://platform.openai.com/)
- [Qdrant Documentation](https://qdrant.tech/)
- [Feature 003: Book Embedding Pipeline](../specs/003-retrieval-validation/)
