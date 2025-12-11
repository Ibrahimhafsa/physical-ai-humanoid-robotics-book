# Book Embedding Pipeline

Automated pipeline for crawling Docosaurus book content, extracting clean text, generating embeddings using Cohere API, and storing vectors in Qdrant Cloud for retrieval-augmented chatbot usage.

## Features

- **URL Discovery**: Automatically crawl Docosaurus sitemap or discover URLs via HTML parsing
- **Text Extraction**: Clean extraction from HTML pages, removing navigation, footers, scripts
- **Semantic Chunking**: Intelligent paragraph-based text splitting with token counting
- **Deduplication**: SHA256-based duplicate content detection (O(1) lookup)
- **Cohere Embeddings**: Batch processing for 4096-dimensional embeddings
- **Qdrant Storage**: Vector storage with metadata and similarity search
- **Idempotent Execution**: Resume from checkpoints, skip already-processed content
- **Comprehensive Logging**: Detailed JSON logs with statistics and error tracking

## Prerequisites

- **Python 3.11+**
- **UV Package Manager** (install from https://astral.sh/uv/)
- **Cohere API Key** (Free Tier at https://cohere.com)
- **Qdrant Cloud Account** (Free Tier at https://qdrant.io)
- **Internet Connection** (for API calls and book crawling)

## Quick Start

### 1. Install UV

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Setup Environment

```bash
# Create .env file
cp .env.example .env

# Edit with your API keys
# Required variables:
#   COHERE_API_KEY=your_key
#   QDRANT_URL=https://your-instance.qdrant.io
#   QDRANT_API_KEY=your_key
#   BOOK_ROOT_URL=https://your-book-url.com
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Run Pipeline

```bash
# Full pipeline (crawl, extract, embed, store)
uv run python src/main.py

# Dry-run (no API calls - test crawling and extraction)
uv run python src/main.py --dry-run

# Resume from checkpoint
uv run python src/main.py --resume

# Process limited pages (testing)
uv run python src/main.py --max-pages 5
```

## Configuration

### Environment Variables

Required:
- `COHERE_API_KEY` - Cohere API key
- `QDRANT_URL` - Qdrant Cloud instance URL
- `QDRANT_API_KEY` - Qdrant API key
- `BOOK_ROOT_URL` - Root URL of the Docusaurus book

Optional:
- `COHERE_MODEL` - Embedding model (default: `embed-3-large`)
- `QDRANT_COLLECTION` - Collection name (default: `book_embeddings`)
- `BATCH_SIZE` - Cohere batch size 1-100 (default: `8`)
- `MAX_PAGES` - Limit pages to process (default: all)
- `MAX_RETRIES` - Max retry attempts for transient failures (default: `3`)
- `RETRY_DELAY_MS` - Initial retry delay in milliseconds (default: `1000`)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: `INFO`)
- `OUTPUT_DIR` - Output directory for logs (default: `./embeddings_output`)

### Example .env

```bash
COHERE_API_KEY=abc-123-xyz-789
COHERE_MODEL=embed-3-large

QDRANT_URL=https://my-cluster-1234567.qdrant.io
QDRANT_API_KEY=qdrant_api_key_abc123xyz789
QDRANT_COLLECTION=book_embeddings

BOOK_ROOT_URL=https://humanoid-robotics-book.example.com

LOG_LEVEL=INFO
OUTPUT_DIR=./embeddings_output
BATCH_SIZE=8
```

## Usage Examples

### Basic Run

```bash
uv run python src/main.py
```

This will:
1. Crawl all URLs from the book
2. Extract clean text from each page
3. Create semantic chunks
4. Generate embeddings via Cohere
5. Store vectors in Qdrant
6. Save summary log to `embeddings_output/ingestion_log.json`

### Dry Run (No API Calls)

```bash
uv run python src/main.py --dry-run
```

Useful for testing crawling and extraction without consuming API quota.

### Resume Pipeline

```bash
uv run python src/main.py --resume
```

If pipeline was interrupted, this resumes from the last checkpoint:
- Skips already-processed URLs
- Continues with new/updated content
- Avoids duplicate ingestion

### Test on Sample

```bash
uv run python src/main.py --max-pages 10
```

Process only the first 10 pages (useful for testing).

### Debug Mode

```bash
LOG_LEVEL=DEBUG uv run python src/main.py
```

Verbose logging with detailed API call information.

## Output

Pipeline generates several output files in the `OUTPUT_DIR` (default: `./embeddings_output/`):

- **`ingestion_log.json`** - Complete summary with statistics, timings, and API usage
- **`chunks.json`** - Detailed log of all created chunks
- **`urls.json`** - List of all crawled URLs
- **`checkpoint.json`** - Resume checkpoint (auto-created)

### Example Ingestion Log

```json
{
  "run_id": "run-2025-12-12T10:30:00Z",
  "summary": {
    "urls_discovered": 150,
    "urls_fetched": 150,
    "chunks_created": 1250,
    "chunks_deduplicated": 5,
    "chunks_embedded": 1245,
    "vectors_stored": 1245
  },
  "performance": {
    "total_time_seconds": 2730
  },
  "api_usage": {
    "cohere_api_calls": 156,
    "cohere_tokens_used": 320000,
    "qdrant_upserts": 156
  }
}
```

## Architecture

### Modules

- **`config.py`** - Configuration management via environment variables
- **`crawler.py`** - Docosaurus URL discovery and page fetching
- **`extractor.py`** - HTML to clean text extraction
- **`chunker.py`** - Semantic text chunking with metadata
- **`deduplicator.py`** - Duplicate detection via SHA256 hashing
- **`retry_policy.py`** - Exponential backoff for transient failures
- **`embedder.py`** - Cohere embeddings generation with batching
- **`storage.py`** - Qdrant Cloud vector storage
- **`pipeline.py`** - Main orchestrator
- **`main.py`** - CLI entry point
- **`logger.py`** - Logging configuration
- **`models.py`** - Pydantic data models

### Data Flow

```
URL Discovery (sitemap)
    ↓
Page Fetching (HTTP GET)
    ↓
Text Extraction (HTML parsing)
    ↓
Semantic Chunking (paragraphs, ≤512 tokens)
    ↓
Deduplication Check (SHA256 hash)
    ↓
Cohere Embedding (batch mode, max 8 texts/call)
    ↓
Qdrant Storage (upsert with metadata)
    ↓
Ingestion Log (summary statistics)
```

## Performance

Typical performance for a 500-page book with ~5000 chunks:

| Phase | Duration | Notes |
|-------|----------|-------|
| URL Discovery | 1-2 min | Sitemap parsing + HTML crawl |
| Page Crawling | 5-10 min | HTTP GET requests |
| Text Extraction | 2-5 min | HTML parsing and cleaning |
| Chunking | 1-2 min | Semantic splitting |
| Embedding | 20-30 min | Cohere API calls (batched) |
| Storage | 2-5 min | Qdrant upserts |
| **Total** | **30-50 min** | |

## Troubleshooting

### Error: "COHERE_API_KEY not found"

- Ensure `.env` file exists in the `backend/` directory
- Check that `COHERE_API_KEY=...` is set (not empty)
- Run `source .env` to load variables

### Error: "Qdrant connection failed"

- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Test connectivity: `curl -H "api-key: YOUR_KEY" https://your-instance.qdrant.io/health`
- Ensure instance is running in Qdrant Cloud dashboard

### Error: "Rate limit exceeded (429)"

- Pipeline automatically retries with exponential backoff
- Check Cohere quota: Free Tier = 1M tokens/month
- If quota exceeded, wait for month to reset or upgrade

### Pipeline Interrupted?

Resume from checkpoint:

```bash
uv run python src/main.py --resume
```

This skips already-processed URLs and continues from last progress.

## Testing

Run tests with pytest:

```bash
uv run pytest tests/
```

Coverage:

```bash
uv run pytest --cov=src tests/
```

## Security Notes

- **API Keys**: Never commit `.env` file or hardcode keys
- **HTTPS**: All API calls use HTTPS
- **Logging**: API keys are masked in logs
- **Data**: Extracted text is ephemeral (not cached locally)

## License

MIT

## Support

For issues or questions, refer to:
- Feature specification: `../spec.md`
- Implementation plan: `../plan.md`
- Data model: `../data-model.md`
- API contracts: `../contracts/embeddings.openapi.yaml`
- Quickstart guide: `../quickstart.md`

---

**Happy embedding! 🚀**
