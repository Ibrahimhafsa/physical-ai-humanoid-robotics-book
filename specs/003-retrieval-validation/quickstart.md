# Quick Start Guide: Retrieval Pipeline Validation Suite

**Feature**: 003-retrieval-validation
**Date**: 2025-12-12
**Target Users**: Developers integrating RAG embeddings

---

## What Is This?

The Retrieval Validation Suite tests whether the Qdrant embedding collection accurately retrieves relevant chunks when queried. It helps ensure embedding quality before deploying a RAG chatbot.

**Why**: Without validation, your RAG chatbot may return irrelevant or low-quality answers, degrading user experience.

---

## Prerequisites

1. **Python 3.11+** installed
2. **Feature 002 (Book Embedding Pipeline)** completed and vectors stored in Qdrant
3. **Cohere API Key** (from .env, Feature 002 setup)
4. **Qdrant Cloud Instance** running with `book_embeddings` collection populated
5. **UV Package Manager** (from Feature 002 setup)

---

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
cd backend

# Sync dependencies (installs validation suite requirements)
uv sync
```

This installs Cohere SDK, Qdrant client, Pydantic, and other requirements.

### Step 2: Verify Configuration

Check that `.env` has these variables (from Feature 002):

```bash
cat .env | grep -E "COHERE_API_KEY|QDRANT_URL|QDRANT_API_KEY|QDRANT_COLLECTION"
```

Expected output:
```
COHERE_API_KEY=abc-123-xyz-789
QDRANT_URL=https://my-instance.qdrant.io
QDRANT_API_KEY=qdrant_api_key_abc123xyz789
QDRANT_COLLECTION=book_embeddings
```

If any are missing, copy from Feature 002 setup or update `.env`.

### Step 3: Test Connection (optional)

Run a dry-run to verify APIs without consuming quota:

```bash
uv run python src/main.py validate --dry-run
```

Expected output:
```
Loading predefined queries...
Query q1: What is physical AI?
  [dry-run mode - no API calls]
...
Validation complete (dry-run)
```

---

## Quick Start (10 minutes)

### Run Default Validation

Execute the predefined test queries (10 questions covering major book topics):

```bash
uv run python src/main.py validate
```

**What this does**:
1. Loads 10 predefined test queries (from `examples/predefined_queries.json`)
2. Embeds each query using Cohere API
3. Searches Qdrant for top-5 similar chunks per query
4. Records similarity scores and retrieved text
5. Generates `validation_report.json` with results

**Output** (will see summary like):
```
Validation Suite - Retrieval Accuracy Report
=============================================

Run ID:               run-2025-12-12T10:30:00Z
Timestamp:            2025-12-12 10:30:00 UTC
Total Queries:        10
Queries Executed:     10
Queries Failed:       0

Summary Statistics
------------------
Avg Similarity Score: 0.81
Min Similarity Score: 0.65
Max Similarity Score: 0.92

Relevance Assessment
--------------------
Relevant:             85%
Partially Relevant:   10%
Irrelevant:            5%

Result: PASS (≥80% relevant)
Duration: 23.5 seconds

Report saved to: validation_report.json
```

### Interpret Results

| Metric | Good | Poor | Action |
|--------|------|------|--------|
| Avg Similarity | >0.75 | <0.65 | Review embedding quality |
| Min Similarity | >0.65 | <0.5 | Low-quality retrievals; review queries |
| Relevant % | ≥80% | <70% | Check chunk quality or update queries |
| Pass/Fail | PASS | FAIL | PASS allows RAG deployment |

**PASS Result**: ✅ Safe to deploy RAG chatbot with these embeddings.

**FAIL Result**: ⚠️ Review low-scoring queries and improve embeddings before deployment.

---

## Custom Query Validation (15 minutes)

### Create Custom Query File

Create `my_queries.json`:

```json
{
  "test_queries": [
    {
      "id": "q1",
      "text": "How do you use Gazebo for simulation?",
      "topic": "simulation",
      "difficulty": "medium",
      "expected_chapters": ["03-control-simulation"]
    },
    {
      "id": "q2",
      "text": "What safety precautions are needed for humanoid robots?",
      "topic": "safety",
      "difficulty": "hard",
      "expected_chapters": ["02-humanoid-robotics"]
    }
  ],
  "metadata": {
    "name": "my_custom_set",
    "created_at": "2025-12-12T00:00:00Z",
    "description": "Custom validation for simulation and safety chapters"
  }
}
```

### Run Validation

```bash
uv run python src/main.py validate --queries my_queries.json --output my_report.json
```

### Review Report

```bash
# View summary only
uv run python src/main.py report --input my_report.json --summary-only

# Export to CSV for spreadsheet
uv run python src/main.py validate --queries my_queries.json --format csv
```

---

## Filtering Results (Advanced)

### Filter by Chapter

Validate only retrieval for "Control Systems" chapter:

```bash
uv run python src/main.py validate --filter-section "Control Systems"
```

This retrieves only chunks from the specified section, testing chapter-specific embedding quality.

### Filter by URL Pattern

Validate only results from specific pages:

```bash
uv run python src/main.py validate --filter-url "chapter-3"
```

### Filter by Chunk Index Range

Test chunks 100-500:

```bash
uv run python src/main.py validate --filter-chunks "100-500"
```

---

## Interactive Relevance Assessment

Manually label query results as relevant/irrelevant:

```bash
uv run python src/main.py validate --assess-manually
```

For each retrieved chunk, you'll be prompted:

```
Relevant? (y/n/p/skip):
y = relevant
n = irrelevant
p = partially relevant
skip = no assessment
```

Your assessments are saved in the report as `relevance_assessment` and `relevance_notes`. Useful for:
- Evaluating retrieval quality with domain expertise
- Building ground-truth data for improving embeddings
- Debugging specific queries

---

## Common Workflows

### Workflow 1: Pre-Deployment Validation

```bash
# 1. Run predefined queries
uv run python src/main.py validate

# 2. Check result - if FAIL, investigate
uv run python src/main.py report --input validation_report.json

# 3. Review low-scoring queries
cat validation_report.json | jq '.results[] | select(.error != null)'

# 4. If PASS, deploy; if FAIL, debug embeddings or queries
```

### Workflow 2: Debugging Low-Quality Results

```bash
# 1. Find failing queries
uv run python src/main.py validate --output debug_report.json

# 2. Filter by specific chapter where you see failures
uv run python src/main.py validate --filter-section "Chapter 3" --output chapter3_report.json

# 3. Manually assess retrieved chunks
uv run python src/main.py validate --filter-section "Chapter 3" --assess-manually

# 4. Review manual assessments to identify patterns
cat chapter3_report.json | jq '.results[].relevance_assessment' | sort | uniq -c
```

### Workflow 3: Regression Testing

After updating embeddings, re-run validation to compare:

```bash
# Before update
uv run python src/main.py validate --output before.json

# [Update embeddings...]

# After update
uv run python src/main.py validate --output after.json

# Compare
diff <(jq '.summary' before.json) <(jq '.summary' after.json)
```

---

## Troubleshooting

### Error: "Cannot reach Cohere API"

**Cause**: Invalid API key or network issue

**Solution**:
1. Check `COHERE_API_KEY` in `.env`
2. Verify internet connection
3. Check Cohere status: https://status.cohere.com

```bash
# Test Cohere connection
uv run python -c "import cohere; c = cohere.ClientV2(api_key='$COHERE_API_KEY'); print('Connected')"
```

### Error: "Qdrant collection not found"

**Cause**: Feature 002 (embedding pipeline) not completed or collection not created

**Solution**:
1. Run Feature 002 embedding pipeline first: `uv run python src/main.py` (in embedding pipeline directory)
2. Verify collection exists: Check Qdrant dashboard → Collections → `book_embeddings`

### Error: "Query file not found"

**Cause**: Wrong path to custom query file

**Solution**:
```bash
# Use absolute path or verify relative path
uv run python src/main.py validate --queries "$(pwd)/my_queries.json"

# Check file exists
ls -la my_queries.json
```

### Low Similarity Scores (<0.65)

**Cause**: Query or embedding quality issues

**Troubleshooting**:
1. Run interactive assessment: `--assess-manually`
2. Review retrieved chunks manually in the report
3. Check if query is clear and specific (not too vague)
4. Verify embeddings were generated with same Cohere model (`embed-3-large`)
5. Consider re-running Feature 002 with more/better book content

---

## Output Files

After running validation, check:

- **`validation_report.json`**: Full report with all query results
  - Schema: See `specs/003-retrieval-validation/data-model.md`
  - Useful for: Programmatic analysis, CI/CD integration

- **`validation.log`**: Detailed execution log
  - Format: JSON
  - Contains: All API calls, timing, warnings

- **CSV export** (if `--format csv`):
  - One row per result
  - Columns: query_id, query_text, rank, similarity_score, source_url, relevance_assessment
  - Useful for: Spreadsheet analysis, trend tracking

---

## Next Steps

### If Validation PASSES (✅ PASS):
1. Proceed with RAG chatbot deployment
2. Use these embeddings in agent integration (Feature 004)
3. Monitor chatbot accuracy in production; compare with validation results

### If Validation FAILS (❌ FAIL):
1. **Review low-scoring queries**: Which queries scored <0.7?
   ```bash
   jq '.results[] | select(.error == null and .results[0].similarity_score < 0.7)' validation_report.json
   ```

2. **Improve query clarity**: Reword vague questions
3. **Check chunk quality**: Are retrieved chunks actually relevant?
   - Run with `--assess-manually` to assess manually
   - Check if book source content is clear and well-written
4. **Re-embed if needed**: Re-run Feature 002 with improvements
5. **Retry validation**: Re-run this suite after changes

---

## Performance Expectations

Typical validation run for 10 queries:

| Phase | Duration | Notes |
|-------|----------|-------|
| Query Embedding (Cohere) | 2-5 sec | 10 queries, batch requests |
| Qdrant Search | 1-3 sec | Per-query similarity search |
| Report Generation | <1 sec | JSON/CSV writing |
| **Total** | **5-15 sec** | Varies by network + API load |

Scaling to 100 queries: ~50-150 seconds (linear scaling).

---

## Integration with Feature 004 (RAG Agent)

Once validation passes, the same Qdrant collection + Cohere model are used by the chatbot agent:

```python
# Feature 004 will use same config
from config import settings
from retrieval_client import QdrantRetriever

retriever = QdrantRetriever(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
    collection=settings.qdrant_collection
)

# During agent chat, retriever is called for every user query
relevant_chunks = retriever.search(user_query, top_k=5)
```

Validation ensures that `retriever.search()` returns high-quality results.

---

## Further Documentation

- **Full Specification**: `specs/003-retrieval-validation/spec.md`
- **Data Model**: `specs/003-retrieval-validation/data-model.md`
- **CLI Interface**: `specs/003-retrieval-validation/contracts/cli-interface.md`
- **Implementation Plan**: `specs/003-retrieval-validation/plan.md`
- **Feature 002 (Embeddings)**: `specs/002-book-embeddings/README.md`
- **Constitution**: `.specify/memory/constitution.md`

---

## Support & Feedback

If you encounter issues or have suggestions:
1. Check this quickstart for common problems
2. Review the troubleshooting section
3. File an issue: https://github.com/humanoid-robotics/ai-physical-robotics-book/issues
4. Tag: `003-retrieval-validation`

Happy validating! 🚀
