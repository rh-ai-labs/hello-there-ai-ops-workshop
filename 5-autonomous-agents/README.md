# Module 5: Autonomous Agents

This module demonstrates how to build autonomous agents using LlamaStack.

## Prerequisites

- **Python 3.12+** (required for llama-stack 0.3.1+)
  - OR Python 3.11 with llama-stack 0.2.12 (if server is also 0.2.12)
- LlamaStack server running (see main README)
- Ollama running with llama3.2:3b model

## Version Compatibility

**IMPORTANT**: The `llama-stack-client` version MUST match your `llama-stack` server version!

### Python 3.12+ (Recommended)
- Server: `llama-stack>=0.3.1`
- Client: `llama-stack-client>=0.3.1`

### Python 3.11
- Server: `llama-stack==0.2.12`
- Client: `llama-stack-client==0.2.12`

**If you get a version mismatch error:**
- Check your server version: Look at the error message or check the server logs
- If server is 0.3.1+ but you're using Python 3.11, you need to either:
  1. Upgrade to Python 3.12+ (recommended)
  2. Downgrade the server to 0.2.12

## Installation

### Option 1: Using Python 3.12+ (Recommended)

```bash
# Ensure you're using Python 3.12+
python --version  # Should show 3.12.x or higher

# Install from root requirements.txt
pip install -r requirements.txt
```

### Option 2: Using Python 3.11 with llama-stack 0.2.12

If your server is also 0.2.12:

```bash
pip install llama-stack==0.2.12 llama-stack-client==0.2.12
pip install duckduckgo-search termcolor fire
```

## Running the Notebooks

1. Start LlamaStack server (if not already running):
   ```bash
   python scripts/start_llama_stack.py
   ```

2. Verify server version matches client:
   ```python
   # In a Python shell or notebook
   import llama_stack_client
   print(f"Client version: {llama_stack_client.__version__}")
   # Check server version from error messages or server logs
   ```

3. Start Jupyter:
   ```bash
   jupyter notebook
   ```

4. Open `notebooks/02_building_simple_agent.ipynb`

## Troubleshooting

### Version Mismatch Error

If you see: `Client version X is not compatible with server version Y`

**Solution:**
1. Check your Python version: `python --version`
2. Check server version (from error message or logs)
3. Install matching versions:
   - Python 3.11: `pip install llama-stack==0.2.12 llama-stack-client==0.2.12`
   - Python 3.12+: `pip install llama-stack>=0.3.1 llama-stack-client>=0.3.1`

### Import Errors

If you get import errors in Jupyter:
1. Make sure packages are installed in the same Python environment Jupyter is using
2. Check which Python Jupyter is using: `import sys; print(sys.executable)`
3. Install packages using that Python: `!{sys.executable} -m pip install <package>`

### Missing Dependencies

If you see `ModuleNotFoundError: No module named 'fire'`:
```bash
pip install fire
```

## Notes

- The notebooks include automatic installation checks
- DuckDuckGo search is used (no API key required)
- All tools run client-side in your Python process
