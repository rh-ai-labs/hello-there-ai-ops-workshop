# Shared Configuration System

This document explains the centralized configuration system for LlamaStack used across all modules.

## Overview

All modules now use a shared configuration system located at `src/config.py` that:
- Auto-detects whether running inside or outside OpenShift
- Automatically discovers LlamaStack routes via `oc` command
- Loads configuration from `.env` file at the root
- Provides consistent configuration across all modules

## Setup

### 1. Run the Setup Script

From the project root, run:

```bash
./scripts/setup-env.sh
```

This script will:
- Detect if you're inside or outside OpenShift cluster
- Try to discover LlamaStack route via `oc` command
- Generate `.env` file with appropriate URLs
- Warn if configuration cannot be auto-detected

### 2. Manual Configuration (if needed)

If auto-detection fails, create `.env` file at the root:

```bash
# Copy example
cp .env.example .env

# Edit with your values
nano .env
```

Required variables:
- `LLAMA_STACK_URL` - URL to LlamaStack (route or service URL)
- `LLAMA_MODEL` - Model identifier (default: `vllm-inference/llama-32-3b-instruct`)
- `NAMESPACE` - OpenShift namespace (default: `my-first-model`)

Optional variables:
- `MCP_MONGODB_URL` - MongoDB MCP server URL (only needed for Module 5)

## Usage in Notebooks

All notebooks should import and use the shared config:

```python
import sys
from pathlib import Path

# Add root src directory to path
root_dir = Path("../..").resolve()  # Adjust path based on module depth
sys.path.insert(0, str(root_dir / "src"))

# Import centralized configuration
from config import LLAMA_STACK_URL, MODEL, CONFIG

# Use the configuration
llamastack_url = LLAMA_STACK_URL
model = MODEL

# Verify configuration is set
if not llamastack_url:
    raise ValueError(
        "LLAMA_STACK_URL is not configured!\n"
        "Please run: ./scripts/setup-env.sh"
    )

# Initialize client
from llama_stack_client import LlamaStackClient
client = LlamaStackClient(base_url=llamastack_url)
```

## Configuration Detection Logic

### Inside OpenShift Cluster
- Uses service URLs:
  - LlamaStack: `http://lsd-llama-milvus-inline-service.{NAMESPACE}.svc.cluster.local:8321`
  - MongoDB MCP: `http://mongodb-mcp-server.{NAMESPACE}.svc.cluster.local:3000`

### Outside OpenShift Cluster
- Tries to discover routes via `oc` command:
  - `oc get route llamastack-route -n {NAMESPACE} -o jsonpath='{.spec.host}'`
  - `oc get route mongodb-mcp-server-route -n {NAMESPACE} -o jsonpath='{.spec.host}'`
- Falls back to empty string (requires manual configuration)

### Priority Order
1. Environment variable (highest priority)
2. `.env` file
3. Auto-detection (OpenShift route/service)
4. Empty string (requires manual configuration)

## Module-Specific Notes

### Module 3 (RAG)
- Uses `LLAMA_STACK_URL` and `MODEL`
- No MongoDB MCP needed

### Module 4 (Fine-tuning)
- Does not use LlamaStack (uses Hugging Face directly)
- No configuration needed

### Module 5 (Autonomous Agents)
- Uses `LLAMA_STACK_URL` and `MODEL`
- Optionally uses `MCP_MONGODB_URL` for MongoDB MCP server

## Troubleshooting

### "LLAMA_STACK_URL is not configured"
1. Run `./scripts/setup-env.sh`
2. Check if `.env` file exists at root
3. Verify `oc` command works: `oc whoami`
4. Check route exists: `oc get route llamastack-route -n my-first-model`
5. Set manually: `export LLAMA_STACK_URL='https://your-route-url'`

### "Cannot connect to LlamaStack"
1. Verify URL is correct: `echo $LLAMA_STACK_URL`
2. Test connectivity: `curl $LLAMA_STACK_URL/health` (if endpoint exists)
3. Check OpenShift route is accessible
4. Verify SSL certificates if using HTTPS

### Inside Cluster but Wrong Service URL
- Check namespace: `oc project`
- Verify service exists: `oc get svc -n {NAMESPACE}`
- Check service name matches expected name

## Migration from Old Configuration

### Old Pattern (Module 3)
```python
base_url = os.getenv("REMOTE_BASE_URL", "http://localhost:8321")
```

### New Pattern
```python
from config import LLAMA_STACK_URL
llamastack_url = LLAMA_STACK_URL  # Auto-detected, no localhost fallback
```

### Old Pattern (Module 5)
```python
llamastack_url = os.getenv("LLAMA_STACK_URL", "https://hardcoded-url")
```

### New Pattern
```python
from config import LLAMA_STACK_URL, CONFIG
llamastack_url = LLAMA_STACK_URL  # Auto-detected from OpenShift
```

## Benefits

1. **Consistency**: All modules use the same configuration source
2. **Auto-detection**: Works automatically in OpenShift environments
3. **No localhost defaults**: Prevents accidental localhost connections
4. **Centralized**: One place to update configuration
5. **Environment-aware**: Adapts to cluster vs. local automatically

