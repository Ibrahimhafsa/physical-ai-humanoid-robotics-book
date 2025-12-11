#!/bin/bash

# Book Embedding Pipeline - Execution Script
# This script sets up the environment and runs the pipeline

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Book Embedding Pipeline${NC}"
echo "=========================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create a .env file with required variables:"
    echo "  - COHERE_API_KEY"
    echo "  - QDRANT_URL"
    echo "  - QDRANT_API_KEY"
    echo "  - BOOK_ROOT_URL"
    echo ""
    echo "You can use .env.example as a template:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your actual values"
    exit 1
fi

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: UV package manager not found${NC}"
    echo "Install UV from: https://astral.sh/uv/"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
    echo -e "${YELLOW}Dependencies not found, installing...${NC}"
    uv sync
fi

# Load environment
source .env

echo -e "${GREEN}Configuration:${NC}"
echo "  Book URL: $BOOK_ROOT_URL"
echo "  Qdrant Collection: ${QDRANT_COLLECTION:-book_embeddings}"
echo "  Batch Size: ${BATCH_SIZE:-8}"
echo ""

# Run pipeline
echo -e "${GREEN}Starting pipeline...${NC}"
echo ""

# Parse command-line arguments
ARGS=""
if [ "$1" == "--dry-run" ]; then
    ARGS="--dry-run"
    echo "Running in DRY-RUN mode (no API calls)"
    echo ""
fi

if [ "$1" == "--resume" ] || [ "$2" == "--resume" ]; then
    ARGS="$ARGS --resume"
    echo "Resuming from checkpoint..."
    echo ""
fi

# Run Python script
uv run python src/main.py $ARGS

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Pipeline completed successfully!${NC}"
    echo "Check embeddings_output/ for logs and checkpoints"
else
    echo -e "${RED}Pipeline failed${NC}"
    exit 1
fi
