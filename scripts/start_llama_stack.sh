#!/bin/bash

# Llama Stack Startup Script
# This script checks prerequisites and starts the Llama Stack server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory and find root (where pyproject.toml is)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
# Root directory is one level up (where pyproject.toml is located)
ROOT_DIR="$(dirname "$PROJECT_DIR")"

echo "🚀 Starting Llama Stack Server..."
echo "=================================="

# Step 1: Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv is not installed or not in PATH${NC}"
    echo "Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo -e "${GREEN}✅ uv found: $(uv --version)${NC}"

# Step 2: Sync dependencies with uv (creates .venv if needed)
# uv sync must be run from root directory where pyproject.toml is
cd "$ROOT_DIR"
echo -e "${YELLOW}⚠️  Syncing dependencies with uv...${NC}"
uv sync --quiet
echo -e "${GREEN}✅ Dependencies synced${NC}"

# Step 3: Activate virtual environment (uv creates .venv in root directory)
if [ -d "$ROOT_DIR/.venv" ]; then
    source "$ROOT_DIR/.venv/bin/activate"
    echo -e "${GREEN}✅ Activated virtual environment${NC}"
else
    echo -e "${RED}❌ Virtual environment not found at $ROOT_DIR/.venv${NC}"
    exit 1
fi

# Step 4: Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama is not installed or not in PATH${NC}"
    echo "Please install Ollama from https://ollama.com/download"
    exit 1
fi
echo -e "${GREEN}✅ Ollama found: $(ollama --version)${NC}"

# Step 5: Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama service not running. Starting Ollama...${NC}"
    ollama serve > /dev/null 2>&1 &
    sleep 3
    echo -e "${GREEN}✅ Ollama service started${NC}"
else
    echo -e "${GREEN}✅ Ollama service is running${NC}"
fi

# Step 6: Check if required models are available
echo "Checking for required models..."
MODEL_SCENARIO_B="llama3.2:3b"
if ollama list | grep -q "$MODEL_SCENARIO_B"; then
    echo -e "${GREEN}✅ Model $MODEL_SCENARIO_B is available${NC}"
else
    echo -e "${YELLOW}⚠️  Model $MODEL_SCENARIO_B not found. Pulling...${NC}"
    ollama pull "$MODEL_SCENARIO_B"
    echo -e "${GREEN}✅ Model $MODEL_SCENARIO_B pulled successfully${NC}"
fi

# Step 7: Set environment variables
export OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
export LLAMA_STACK_PORT="${LLAMA_STACK_PORT:-8321}"
export LLAMA_STACK_HOST="${LLAMA_STACK_HOST:-localhost}"

echo -e "${GREEN}✅ Environment variables set:${NC}"
echo "   OLLAMA_URL=$OLLAMA_URL"
echo "   LLAMA_STACK_PORT=$LLAMA_STACK_PORT"

# Step 8: Check if llama-stack is installed
if ! python -c "import llama_stack" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  llama-stack not installed. Installing with uv...${NC}"
    uv add llama-stack opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    echo -e "${GREEN}✅ llama-stack installed${NC}"
else
    echo -e "${GREEN}✅ llama-stack is installed${NC}"
fi

# Step 9: Check if port is available
if lsof -Pi :$LLAMA_STACK_PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port $LLAMA_STACK_PORT is already in use${NC}"
    echo "Please stop the service using that port or set LLAMA_STACK_PORT to a different value"
    exit 1
fi

# Step 10: Start Llama Stack server
echo ""
echo -e "${GREEN}🚀 Starting Llama Stack server on http://$LLAMA_STACK_HOST:$LLAMA_STACK_PORT${NC}"
echo "Press Ctrl+C to stop the server"
echo ""

# Change to project directory for running llama stack
cd "$PROJECT_DIR"

# Try to run Llama Stack using uv run (preferred) or directly
# uv run must be executed from root where pyproject.toml is
if command -v llama &> /dev/null; then
    llama stack run starter
elif (cd "$ROOT_DIR" && uv run llama stack run starter) 2>/dev/null; then
    # uv run handles environment automatically
    true
elif python -m llama_stack --help &> /dev/null; then
    python -m llama_stack run starter
else
    echo -e "${RED}❌ Could not find llama-stack CLI${NC}"
    echo "Try running: cd $ROOT_DIR && uv sync"
    exit 1
fi

