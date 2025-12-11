"""
CLI script for retrieval validation.

Runs predefined test queries against Qdrant collection and generates
a console report showing retrieval accuracy with similarity scores,
source URLs, and chunk IDs.
"""

import json
import logging
import os
import sys
from datetime import datetime
from typing import List

from retrieve import QueryEmbedder, QdrantRetriever, ContextExtractor


def setup_logging(log_level: str = "INFO") -> None:
    """Configure JSON logging to console and file."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('validation.log')
        ]
    )


def load_predefined_queries() -> List[dict]:
    """
    Load predefined test queries from examples/predefined_queries.json.

    Returns:
        List of query dicts with id, text, topic, difficulty, etc.
    """
    queries_path = os.path.join(os.path.dirname(__file__), "..", "examples", "predefined_queries.json")

    if not os.path.exists(queries_path):
        # Return hardcoded fallback queries if file doesn't exist
        return [
            {"id": "q1", "text": "What is physical AI?", "topic": "foundational", "difficulty": "easy"},
            {"id": "q2", "text": "Explain kinematics and dynamics in humanoid robots", "topic": "mechanics", "difficulty": "medium"},
            {"id": "q3", "text": "What are the steps to set up a ROS 2 environment?", "topic": "setup", "difficulty": "medium"},
            {"id": "q4", "text": "How do you implement feedback control?", "topic": "control", "difficulty": "hard"},
            {"id": "q5", "text": "What is reinforcement learning?", "topic": "learning", "difficulty": "medium"},
        ]

    try:
        with open(queries_path, 'r') as f:
            data = json.load(f)
            queries = data.get("test_queries", [])
            logging.info(f"Loaded {len(queries)} predefined queries from {queries_path}")
            return queries
    except Exception as e:
        logging.error(f"Failed to load predefined queries: {e}")
        return []


def validate_retrieval(top_k: int = 5, dry_run: bool = False) -> dict:
    """
    Execute retrieval validation with predefined queries.

    Args:
        top_k: Number of results to retrieve per query
        dry_run: If True, skip API calls and return mock results

    Returns:
        Validation report dict with results and summary
    """
    # Load configuration from environment
    cohere_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    qdrant_collection = os.getenv("QDRANT_COLLECTION", "book_embeddings")

    if not all([cohere_key, qdrant_url, qdrant_key]):
        raise ValueError(
            "Missing required environment variables: "
            "COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY"
        )

    # Initialize services
    embedder = QueryEmbedder(api_key=cohere_key)
    retriever = QdrantRetriever(url=qdrant_url, api_key=qdrant_key, collection_name=qdrant_collection)

    # Verify collection exists
    if not dry_run:
        try:
            retriever.verify_collection_exists()
        except Exception as e:
            logging.error(f"Collection verification failed: {e}")
            raise

    # Load test queries
    queries = load_predefined_queries()
    if not queries:
        raise ValueError("No test queries available")

    # Execute validation
    results = []
    relevance_scores = []
    start_time = datetime.now()

    for query_obj in queries:
        query_id = query_obj.get("id")
        query_text = query_obj.get("text")

        logging.info(f"Processing query {query_id}: {query_text}")

        try:
            if dry_run:
                # Mock embedding for dry-run
                query_vector = [0.1] * 4096
                logging.info("[dry-run] Skipping Cohere embedding")
            else:
                # Embed query via Cohere
                query_vector = embedder.embed_query(query_text)

            if dry_run:
                # Mock retrieval results
                retrieved_chunks = [
                    {
                        "rank": 1,
                        "similarity_score": 0.85,
                        "chunk_id": f"chunk_{query_id}_1",
                        "source_url": "https://book.example.com/docs/chapter-1",
                        "section_title": "Introduction",
                        "text_excerpt": f"Mock result for {query_text}"
                    }
                ]
                logging.info("[dry-run] Skipping Qdrant search")
            else:
                # Search Qdrant
                retrieved_chunks = retriever.search_similar(
                    query_vector=query_vector,
                    top_k=top_k,
                    score_threshold=0.5
                )

            if not retrieved_chunks:
                logging.warning(f"Query {query_id} returned no results")
                relevance_scores.append(0.0)
            else:
                top_score = retrieved_chunks[0]["similarity_score"]
                relevance_scores.append(top_score)

                # Flag low-relevance results
                if top_score < 0.7:
                    logging.warning(f"Query {query_id} low score: {top_score:.3f}")

            results.append({
                "query_id": query_id,
                "query_text": query_text,
                "retrieved_chunks": len(retrieved_chunks),
                "results": retrieved_chunks,
                "error": None
            })

        except Exception as e:
            logging.error(f"Query {query_id} failed: {e}")
            results.append({
                "query_id": query_id,
                "query_text": query_text,
                "retrieved_chunks": 0,
                "results": [],
                "error": str(e)
            })

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Calculate summary statistics
    successful_queries = len([r for r in results if r["error"] is None])
    avg_score = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
    relevant_count = sum(1 for score in relevance_scores if score >= 0.7)
    relevant_percent = (relevant_count / len(relevance_scores) * 100) if relevance_scores else 0.0

    report = {
        "validation_id": f"run-{start_time.isoformat()}",
        "timestamp": start_time.isoformat(),
        "total_queries": len(queries),
        "queries_executed": successful_queries,
        "queries_failed": len(queries) - successful_queries,
        "results": results,
        "summary": {
            "avg_similarity_score": round(avg_score, 3),
            "min_similarity_score": round(min(relevance_scores)) if relevance_scores else 0.0,
            "max_similarity_score": round(max(relevance_scores), 3) if relevance_scores else 0.0,
            "relevant_results_percent": round(relevant_percent, 1),
            "pass_fail": relevant_percent >= 80.0
        },
        "duration_seconds": duration
    }

    return report


def print_console_report(report: dict) -> None:
    """Print validation report to console in human-readable format."""
    print("\n" + "=" * 70)
    print("RETRIEVAL VALIDATION REPORT")
    print("=" * 70)
    print(f"\nRun ID:            {report['validation_id']}")
    print(f"Timestamp:         {report['timestamp']}")
    print(f"Total Queries:     {report['total_queries']}")
    print(f"Executed:          {report['queries_executed']}")
    print(f"Failed:            {report['queries_failed']}")
    print(f"Duration:          {report['duration_seconds']:.1f} seconds")

    print("\n" + "-" * 70)
    print("SUMMARY STATISTICS")
    print("-" * 70)
    summary = report["summary"]
    print(f"Avg Similarity:    {summary['avg_similarity_score']:.3f}")
    print(f"Min Similarity:    {summary['min_similarity_score']:.3f}")
    print(f"Max Similarity:    {summary['max_similarity_score']:.3f}")
    print(f"Relevant Results:  {summary['relevant_results_percent']:.1f}%")

    status = "✅ PASS" if summary["pass_fail"] else "❌ FAIL"
    print(f"Status:            {status} (≥80% relevant = PASS)")

    print("\n" + "-" * 70)
    print("PER-QUERY RESULTS")
    print("-" * 70)

    for result in report["results"]:
        query_id = result["query_id"]
        query_text = result["query_text"][:60]
        error = result["error"]

        if error:
            print(f"\n❌ {query_id}: {query_text}...")
            print(f"   Error: {error}")
        else:
            retrieved = result["retrieved_chunks"]
            if retrieved > 0:
                top_score = result["results"][0]["similarity_score"]
                top_url = result["results"][0]["source_url"][:50]
                status_icon = "✅" if top_score >= 0.7 else "⚠️"
                print(f"\n{status_icon} {query_id}: {query_text}...")
                print(f"   Results: {retrieved} chunks")
                print(f"   Top score: {top_score:.3f}")
                print(f"   Top URL: {top_url}")
            else:
                print(f"\n❌ {query_id}: No results found")

    print("\n" + "=" * 70)
    print()


def main():
    """Main entry point for validation script."""
    import argparse

    parser = argparse.ArgumentParser(description="Retrieval Pipeline Validation Suite")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results per query (default: 5)")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, use mock data")
    parser.add_argument("--log-level", default="INFO", help="Logging level (default: INFO)")
    parser.add_argument("--output", help="Save report to JSON file")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    try:
        # Run validation
        logger.info(f"Starting retrieval validation (dry_run={args.dry_run})")
        report = validate_retrieval(top_k=args.top_k, dry_run=args.dry_run)

        # Print console report
        print_console_report(report)

        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {args.output}")

        # Exit with status
        exit_code = 0 if report["summary"]["pass_fail"] else 1
        sys.exit(exit_code)

    except Exception as e:
        logger.error(f"Validation failed: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
