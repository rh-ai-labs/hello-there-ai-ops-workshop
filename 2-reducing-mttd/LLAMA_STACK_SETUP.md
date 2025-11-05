# 🚀 Llama Stack Setup and Running Guide

This guide provides step-by-step instructions to build, configure, and run the Llama Stack server with Ollama as your local LLM provider for Phase 2: Reference-Based Evaluation.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **uv** (Modern Python package manager - faster than pip)
- **Ollama** - Local LLM serving platform
- **Git** (for cloning repositories if needed)

> **Note:** This project uses `uv` for package management. If you haven't migrated yet, see [MIGRATE_TO_UV.md](./MIGRATE_TO_UV.md) for migration instructions.

---

## 🔧 Step 1: Install Ollama

Ollama allows you to run large language models locally on your machine.

### macOS Installation

```bash
# Download and install using Homebrew
brew install ollama

# Or download directly from https://ollama.com/download
```

### Linux Installation

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows Installation

Download the installer from [https://ollama.com/download](https://ollama.com/download) and follow the installation wizard.

### Verify Ollama Installation

```bash
ollama --version
```

---

## 🎯 Step 2: Download and Run Llama Models with Ollama

For this project, we'll use models suitable for both scenarios:

- **Scenario A**: Large general LLM (e.g., `llama3.2:70b` or `llama3.1:70b`)
- **Scenario B**: Smaller tuned LLM (e.g., `llama3.2:3b` or `llama3.1:8b`)

### Pull Models

```bash
# For Scenario B (smaller model - recommended for testing)
ollama pull llama3.2:3b

# For Scenario A (larger model - optional, requires more resources)
# ollama pull llama3.2:70b
```

### Start Ollama Service

```bash
# Start Ollama service (runs in background)
ollama serve

# In another terminal, verify it's running
ollama list
```

### Keep Model Loaded (Optional)

To keep a model loaded in memory for faster responses:

```bash
# Keep the 3B model loaded (60 minutes timeout)
ollama run llama3.2:3b --keepalive 60m
```

**Note:** Keep this terminal open or run it in the background.

---

## 📦 Step 3: Install uv (if not already installed)

uv is a fast Python package manager that replaces pip, venv, and pip-tools.

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew (macOS)
brew install uv

# Or using pip (temporary, just to install uv)
pip install uv
```

### Verify Installation

```bash
uv --version
```

---

## 📦 Step 4: Set Up Python Environment with uv

### Sync Dependencies

uv will automatically:
- Create a virtual environment (`.venv`)
- Install all dependencies from `pyproject.toml`
- Generate a lock file (`uv.lock`)

```bash
# Navigate to project directory
cd /Users/gsampaio/redhat/ai/ai-workshop/2-reducing-mttd

# Sync dependencies (creates .venv and installs everything)
uv sync

# Activate virtual environment (optional - uv run handles this automatically)
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

### Add Dependencies (if needed)

```bash
# Add a new package
uv add package-name

# Add with specific version
uv add "package-name>=1.0.0"
```

---

## 🏗️ Step 5: Build Llama Stack Server

Llama Stack provides a CLI tool to build and run the server. The server provides APIs for:
- `/eval` - Evaluation endpoints
- `/scoring` - Scoring functions
- `/datasetio` - Dataset management

### Verify Llama Stack Installation

Llama Stack should already be installed via `uv sync`. Verify:

```bash
# Using uv
uv run llama --version
# or
uv run python -m llama_stack --version

# Or if virtual environment is activated
llama --version
```

### Build Llama Stack Configuration

```bash
# Build the starter distribution (most common)
llama stack build --distro starter

# This creates configuration files in your working directory
```

**Alternative build methods:**

```bash
# Build with specific image type (venv, docker, etc.)
llama stack build --distro starter --image-type venv

# Build and run in one command
llama stack build --distro starter --run
```

---

## ⚙️ Step 6: Configure Environment Variables

Create a `.env` file in the project root or set environment variables:

```bash
# Set Ollama URL (default is http://localhost:11434)
export OLLAMA_URL=http://localhost:11434

# Llama Stack server port (default is 8321)
export LLAMA_STACK_PORT=8321

# Optional: API key for authentication (if needed)
export LLAMA_STACK_API_KEY=none
```

### Create `.env` File (Recommended)

Create `.env` file in `2-reducing-mttd/` directory:

```env
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL_SCENARIO_A=llama3.2:70b
OLLAMA_MODEL_SCENARIO_B=llama3.2:3b

# Llama Stack Configuration
LLAMA_STACK_PORT=8321
LLAMA_STACK_HOST=localhost
LLAMA_STACK_API_KEY=none

# Python Environment
PYTHONPATH=.
```

---

## 🚀 Step 7: Run Llama Stack Server

### Manual Start (with uv)

```bash
# Set environment variables
export OLLAMA_URL=http://localhost:11434

# Run Llama Stack server using uv
uv run llama stack run starter

# Or if virtual environment is activated
source .venv/bin/activate
llama stack run starter
```

The server should start and listen on `http://localhost:8321` by default.

### Using the Startup Script

We've created a startup script for convenience (see Step 7).

---

## ✅ Step 8: Verify Llama Stack is Running

### Check Server Health

```bash
# Test health endpoint
curl http://localhost:8321/health

# Expected response: {"status": "healthy"} or similar
```

### List Available Models

```bash
# Using curl
curl http://localhost:8321/v1/models

# Or using Ollama directly
ollama list
```

### Test API Endpoints

```bash
# Check if eval endpoint is available
curl http://localhost:8321/eval

# Check if scoring endpoint is available
curl http://localhost:8321/scoring

# Check if datasetio endpoint is available
curl http://localhost:8321/datasetio
```

---

## 📜 Step 9: Using the Startup Scripts

We've created convenient scripts to start Llama Stack. See the `scripts/` directory:

### Option 1: Start Script (Bash)

```bash
# Make script executable
chmod +x scripts/start_llama_stack.sh

# Run the script
./scripts/start_llama_stack.sh
```

### Option 2: Start Script (Python)

```bash
# Run Python script
python scripts/start_llama_stack.py
```

### What the Scripts Do

1. Check if Ollama is running
2. Verify models are available
3. Set environment variables
4. Start Llama Stack server
5. Provide status feedback

---

## 🔍 Troubleshooting

### Issue: Ollama not found

**Solution:**
```bash
# Verify Ollama is installed
which ollama

# If not found, reinstall Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
```

### Issue: Port 8321 already in use

**Solution:**
```bash
# Find process using port 8321
lsof -i :8321  # macOS/Linux
netstat -ano | findstr :8321  # Windows

# Kill the process or change port
export LLAMA_STACK_PORT=8322
```

### Issue: Llama Stack CLI not found

**Solution:**
```bash
# Sync dependencies with uv
uv sync

# Or add llama-stack explicitly
uv add llama-stack

# Verify installation
uv run llama --version
# or
uv pip list | grep llama-stack
```

### Issue: Cannot connect to Ollama

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve

# Verify OLLAMA_URL environment variable
echo $OLLAMA_URL
# Should output: http://localhost:11434
```

### Issue: Model not found

**Solution:**
```bash
# List available models
ollama list

# Pull the required model
ollama pull llama3.2:3b

# Verify model is available
ollama show llama3.2:3b
```

### Issue: Permission denied on scripts

**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Or run with explicit interpreter
bash scripts/start_llama_stack.sh
```

---

## 📚 Next Steps

Once Llama Stack is running successfully:

1. ✅ **Verify Setup**: Run health checks and test API endpoints
2. ✅ **Register Models**: Register your Ollama models in Llama Stack
3. ✅ **Register Dataset**: Upload `gt_close_notes.csv` via `/datasetio` API
4. ✅ **Configure Scoring Functions**: Set up evaluation metrics
5. ✅ **Proceed to Notebooks**: Start working on `03_reference_based_evaluation.ipynb`

---

## 🔗 Useful Resources

- **Llama Stack Documentation**: https://llama-stack.readthedocs.io/
- **Ollama Documentation**: https://ollama.readthedocs.io/
- **Llama Stack GitHub**: https://github.com/llamastack/llama-stack
- **Ollama Models**: https://ollama.com/library

---

## 📝 Configuration Files Location

After building Llama Stack, configuration files are typically created in:

- `llama-stack-config/` - Server configuration
- `.llama-stack/` - Cache and runtime files
- `dist/` - Distribution files (if using build command)

**Note:** These directories may be added to `.gitignore` to avoid committing generated files.

---

## 🎯 Quick Start Summary

For experienced users, here's the quickest path:

```bash
# 1. Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install Ollama and pull model
ollama pull llama3.2:3b
ollama serve &

# 3. Set up Python environment with uv
cd /Users/gsampaio/redhat/ai/ai-workshop/2-reducing-mttd
uv sync

# 4. Build and run Llama Stack
export OLLAMA_URL=http://localhost:11434
uv run llama stack build --distro starter --run

# 5. Verify (in another terminal)
curl http://localhost:8321/health
```

---

**Last Updated:** December 2024  
**Project:** AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA  
**Phase:** Phase 2 - Reference-Based Evaluation with Llama Stack APIs

