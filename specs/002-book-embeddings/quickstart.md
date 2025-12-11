# Quickstart: Book Embedding Pipeline

**Feature**: 002-book-embeddings | **Date**: 2025-12-12

This guide walks you through setting up and running the Book Embedding Pipeline locally.

## Prerequisites

- **Python 3.11+** installed
- **UV package manager** (modern Python package manager; faster than pip)
- **Cohere API key** (Free Tier; get at [cohere.com](https://cohere.com))
- **Qdrant Cloud account** (Free Tier; register at [qdrant.io](https://qdrant.io))
- **Internet connection** (for API calls and book crawling)

## Step 1: Install UV

UV is a fast, Rust-based Python package manager that handles dependency locking and reproducibility.

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (using PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verify Installation

```bash
uv --version
```

## Step 2: Clone or Download the Repository

```bash
cd /path/to/ai-physical-robotics-book
git checkout 002-book-embeddings
```

## Step 3: Set Up Environment Variables

Create a `.env` file in the `backend/` directory with your API credentials.

### Template (`.env`)

```bash
# Cohere API Configuration
COHERE_API_KEY=<your_cohere_api_key>
COHERE_MODEL=embed-3-large

# Qdrant Cloud Configuration
QDRANT_URL=https://<your-instance-name>.qdrant.io
QDRANT_API_KEY=<your_qdrant_api_key>
QDRANT_COLLECTION=book_embeddings

# Book Configuration
BOOK_ROOT_URL=https://example.com  # URL of deployed Docusaurus book

# Optional: Logging and Debugging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
OUTPUT_DIR=./embeddings_output  # Directory for logs and checkpoints
```

### Getting API Keys

**Cohere API Key**:
1. Go to [cohere.com](https://cohere.com)
2. Sign up or log in
3. Navigate to **Dashboard** → **API Keys**
4. Copy your API key and add to `.env`

**Qdrant Cloud**:
1. Go to [qdrant.io/cloud](https://qdrant.io/cloud)
2. Create a free cluster
3. Click on your cluster and go to **Settings** → **API Keys**
4. Copy the API key and URL; add to `.env`

### Example `.env` File

```bash
COHERE_API_KEY=abc-123-xyz-789
COHERE_MODEL=embed-3-large

QDRANT_URL=https://my-cluster-1234567.qdrant.io
QDRANT_API_KEY=qdrant_api_key_abc123xyz789
QDRANT_COLLECTION=book_embeddings

BOOK_ROOT_URL=https://humanoid-robotics-book.example.com

LOG_LEVEL=INFO
OUTPUT_DIR=./embeddings_output
```

## Step 4: Install Dependencies

Navigate to the `backend/` directory and use UV to install dependencies.

```bash
cd backend/
uv sync
```

This command:
- Reads `pyproject.toml` (project manifest)
- Installs all dependencies (httpx, beautifulsoup4, cohere, qdrant-client, pydantic, python-dotenv, pytest)
- Creates a `uv.lock` file (locked versions for reproducibility)

## Step 5: Run the Pipeline

### Basic Run (All URLs)

```bash
# From backend/ directory
uv run python src/main.py
```

Output:
- Crawls all URLs from the Docusaurus sitemap
- Extracts text from each page
- Generates embeddings via Cohere API
- Stores vectors in Qdrant Cloud
- Produces JSON logs in `./embeddings_output/`

### Dry Run (No API Calls)

To test crawling and extraction without calling Cohere/Qdrant APIs:

```bash
uv run python src/main.py --dry-run
```

This validates:
- URL discovery (sitemap parsing)
- Text extraction quality
- Chunk creation
- Deduplication logic

**Without hitting external APIs**

### Limited Scope (Testing)

To test on a subset of pages:

```bash
uv run python src/main.py --max-pages 5
```

Useful for validating setup before full pipeline run.

## Step 6: Verify Output

After the pipeline completes, check the `embeddings_output/` directory:

```bash
ls -la embeddings_output/
```

Expected files:
- `ingestion_log.json` — Summary of crawl, chunks, vectors, timings, and errors
- `chunks.json` — Detailed log of each chunk created
- `urls.json` — List of all crawled URLs
- `checkpoint.json` — Resume state (used if pipeline interrupted)

### Inspect Ingestion Log

```bash
cat embeddings_output/ingestion_log.json | python -m json.tool | head -50
```

Key metrics:
- `summary.urls_discovered` — Total pages found
- `summary.chunks_embedded` — Total chunks embedded
- `summary.vectors_stored` — Total vectors in Qdrant
- `performance.total_time_seconds` — End-to-end duration
- `api_usage.cohere_tokens_used` — Tokens consumed (check quota)

### Verify in Qdrant

Check collection size in Qdrant Cloud dashboard:
1. Go to [qdrant.io/cloud](https://qdrant.io/cloud)
2. Click your cluster
3. View **Collections** → `book_embeddings`
4. Verify point count matches `vectors_stored` in log (±0.1% variance)

## Step 7: Test Retrieval (Optional)

Once vectors are stored, test similarity search:

```bash
uv run python src/main.py --test-search "What is physical AI?"
```

This:
1. Embeds your query with Cohere
2. Searches Qdrant for similar chunks
3. Returns top 5 results with similarity scores

Example output:
```
Query: "What is physical AI?"
Results:
  1. URL: https://example.com/docs/fundamentals/physical-ai
     Score: 0.89
     Text: "Physical AI is the branch of artificial intelligence..."
  2. URL: https://example.com/docs/intro/embodied-intelligence
     Score: 0.84
     Text: "Embodied intelligence refers to systems that..."
```

## Troubleshooting

### Error: "COHERE_API_KEY not found"

- Ensure `.env` file exists in `backend/` directory
- Check that `COHERE_API_KEY=...` is set (not empty)
- Run `source .env` (on Linux/macOS) or manually export variables on Windows

### Error: "Qdrant connection failed"

- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Test connectivity: `curl -H "api-key: YOUR_KEY" https://your-instance.qdrant.io/health`
- Ensure instance is running in Qdrant Cloud dashboard

### Error: "Rate limit exceeded (429)"

- Pipeline automatically retries with exponential backoff
- Check Cohere quota: `FREE_TIER_TOKENS_PER_MONTH = 1,000,000`
- Estimate tokens: (num_chunks × avg_tokens_per_chunk)
- If quota exceeded, wait for month to reset or upgrade to paid tier

### Pipeline Interrupted?

Resume from checkpoint:

```bash
uv run python src/main.py --resume
```

This:
- Reads `checkpoint.json`
- Skips already-processed URLs
- Continues from last unprocessed page

### Output Directory Full?

Clean up old runs:

```bash
rm -rf embeddings_output/
```

Or specify custom output directory in `.env`:

```bash
OUTPUT_DIR=/path/to/custom/directory
```

## Performance Expectations

### Timing Estimates (500-page book with ~5k chunks)

| Phase | Time |
|-------|------|
| URL Discovery (sitemap) | ~30–60 seconds |
| Page Crawling & Extraction | ~5–10 minutes |
| Embedding Generation (Cohere) | ~20–30 minutes |
| Qdrant Storage | ~2–5 minutes |
| **Total** | **~30–50 minutes** |

### Performance Tips

1. **Batch Size**: Default 8 chunks/Cohere API call is optimized; increase only if quota allows
2. **Network**: Stable internet connection speeds up crawling and API calls
3. **Dry Run First**: Test with `--dry-run` before full pipeline to validate setup
4. **Monitor Quota**: Check `api_usage.cohere_tokens_used` in log to stay within Free Tier

## What's Next?

### For Chatbot Integration

1. Store the ingestion log and vector collection name in your chatbot config
2. When users ask questions:
   - Embed the question with Cohere
   - Search Qdrant for similar chunks (top 5–10)
   - Pass retrieved chunks as context to LLM (e.g., GPT, Claude)
3. LLM generates answer grounded in book content

### For Re-running on Book Updates

If the Docusaurus book content is updated:

```bash
# Remove old vectors (optional; Qdrant upsert will replace them)
# Or keep for history; Qdrant handles duplicate IDs via upsert

# Run pipeline again
uv run python src/main.py
```

Pipeline automatically:
- Detects new URLs
- Re-embeds updated content
- Skips unchanged pages (via content hash deduplication)

### For Troubleshooting & Debugging

Enable debug logging:

```bash
LOG_LEVEL=DEBUG uv run python src/main.py
```

This produces verbose logs:
- HTTP requests/responses
- Text extraction details
- API call timing
- Deduplication checks

## Support

For issues, questions, or improvements:
- Check `embeddings_output/ingestion_log.json` for detailed error logs
- Review `data-model.md` for entity and schema reference
- Consult `contracts/embeddings.openapi.yaml` for API contract details
- Open an issue on the repository (link TBD)

## Summary

You've successfully set up the Book Embedding Pipeline! The workflow:

```
1. Configure API keys (.env)
2. Install dependencies (uv sync)
3. Run pipeline (uv run python src/main.py)
4. Check output logs and verify Qdrant collection
5. (Optional) Test retrieval with --test-search
6. Use embeddings in chatbot or downstream system
```

Happy embedding! 🚀
