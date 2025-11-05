# Scripts Directory

This directory contains utility scripts for managing the Llama Stack server and related services.

## Available Scripts

### `start_llama_stack.sh`
Bash script to start the Llama Stack server with all prerequisites checked.

**Usage:**
```bash
./scripts/start_llama_stack.sh
```

**What it does:**
- Checks if uv is installed
- Syncs dependencies using `uv sync` (creates `.venv` if needed)
- Verifies Ollama installation and service
- Checks for required models and pulls them if missing
- Sets environment variables
- Starts Llama Stack server

### `start_llama_stack.py`
Python script with the same functionality as the bash script, but cross-platform compatible.

**Usage:**
```bash
python scripts/start_llama_stack.py
# or
./scripts/start_llama_stack.py
```

**What it does:**
- Same functionality as bash script
- Better error handling and cross-platform support
- Colored output for better readability

## Prerequisites

Before running the scripts, ensure:

1. **uv is installed** - https://docs.astral.sh/uv/ (scripts will check and guide you)
2. **Ollama is installed** - https://ollama.com/download
3. **Python 3.10+** is available
4. **pyproject.toml** exists in project root (created automatically by uv)

## Environment Variables

The scripts use the following environment variables (with defaults):

- `OLLAMA_URL` - Default: `http://localhost:11434`
- `LLAMA_STACK_PORT` - Default: `8321`
- `LLAMA_STACK_HOST` - Default: `localhost`

You can override these by setting them before running the scripts:

```bash
export OLLAMA_URL=http://localhost:11434
export LLAMA_STACK_PORT=8322
./scripts/start_llama_stack.sh
```

## Troubleshooting

### Script fails with "command not found"
Make sure the script is executable:
```bash
chmod +x scripts/start_llama_stack.sh
```

### Ollama not found
Install Ollama from https://ollama.com/download or ensure it's in your PATH.

### Port already in use
Either stop the service using the port or set a different port:
```bash
export LLAMA_STACK_PORT=8322
./scripts/start_llama_stack.sh
```

### Permission denied
On some systems, you may need to run with explicit interpreter:
```bash
bash scripts/start_llama_stack.sh
# or
python3 scripts/start_llama_stack.py
```

## Notes

- The scripts will automatically create a virtual environment if one doesn't exist
- Models will be automatically pulled if they're not available
- The scripts check for prerequisites before starting the server
- Use Ctrl+C to stop the server when running

