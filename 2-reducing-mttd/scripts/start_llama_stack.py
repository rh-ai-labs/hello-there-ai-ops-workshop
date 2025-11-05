#!/usr/bin/env python3
"""
Llama Stack Startup Script (Python version)
This script checks prerequisites and starts the Llama Stack server
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_status(message, status="info"):
    """Print colored status message"""
    if status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.NC}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.NC}")
    elif status == "info":
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.NC}")
    else:
        print(message)

def check_command(cmd, name):
    """Check if a command exists"""
    try:
        result = subprocess.run(
            ["which", cmd] if sys.platform != "win32" else ["where", cmd],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def run_command(cmd, check=True, capture_output=False):
    """Run a shell command"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return e

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def start_ollama():
    """Start Ollama service"""
    print_status("Starting Ollama service...", "info")
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        return check_ollama_running()
    except Exception as e:
        print_status(f"Failed to start Ollama: {e}", "error")
        return False

def check_model_available(model_name):
    """Check if a model is available in Ollama"""
    try:
        result = run_command(f"ollama list", capture_output=True)
        return model_name in result.stdout
    except Exception:
        return False

def pull_model(model_name):
    """Pull a model from Ollama"""
    print_status(f"Pulling model {model_name}...", "info")
    try:
        result = run_command(f"ollama pull {model_name}", capture_output=True)
        return result.returncode == 0
    except Exception as e:
        print_status(f"Failed to pull model: {e}", "error")
        return False

def check_port_available(port):
    """Check if a port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        return True
    except Exception:
        return False

def check_uv_installed():
    """Check if uv is installed"""
    return check_command("uv", "uv")

def find_root_directory(start_path):
    """Find root directory containing pyproject.toml"""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return None

def sync_dependencies(root_dir):
    """Sync dependencies using uv (must be run from root directory)"""
    print_status("Syncing dependencies with uv...", "info")
    try:
        # Run uv sync from root directory
        result = run_command(f"cd {root_dir} && uv sync --quiet", capture_output=True)
        return result.returncode == 0
    except Exception as e:
        print_status(f"Failed to sync dependencies: {e}", "error")
        return False

def get_venv_path(root_dir):
    """Get virtual environment path (uv creates .venv in root directory)"""
    if root_dir:
        venv_path = root_dir / ".venv"
        if venv_path.exists():
            return venv_path
    return None

def main():
    """Main function"""
    print("🚀 Starting Llama Stack Server...")
    print("=" * 50)
    
    # Get project directory and root directory (where pyproject.toml is)
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    root_dir = find_root_directory(project_dir)
    
    if not root_dir:
        print_status("Could not find root directory with pyproject.toml", "error")
        sys.exit(1)
    
    print_status(f"Project directory: {project_dir}", "info")
    print_status(f"Root directory: {root_dir}", "info")
    
    # Step 1: Check Python version
    python_version = sys.version_info
    if python_version < (3, 10):
        print_status(f"Python 3.10+ required. Found {python_version.major}.{python_version.minor}", "error")
        sys.exit(1)
    print_status(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}", "success")
    
    # Step 2: Check if uv is installed
    if not check_uv_installed():
        print_status("uv is not installed or not in PATH", "error")
        print_status("Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh", "info")
        sys.exit(1)
    
    uv_version = run_command("uv --version", capture_output=True)
    print_status(f"uv found: {uv_version.stdout.strip()}", "success")
    
    # Step 3: Sync dependencies with uv (from root directory)
    if not sync_dependencies(root_dir):
        print_status("Failed to sync dependencies", "error")
        sys.exit(1)
    print_status("Dependencies synced", "success")
    
    # Step 4: Get virtual environment path (in root directory)
    venv_path = get_venv_path(root_dir)
    if not venv_path:
        print_status(f"Virtual environment not found at {root_dir}/.venv", "error")
        sys.exit(1)
    print_status(f"Virtual environment found: {venv_path}", "success")
    
    # Step 5: Check if Ollama is installed
    if not check_command("ollama", "Ollama"):
        print_status("Ollama is not installed or not in PATH", "error")
        print_status("Please install Ollama from https://ollama.com/download", "info")
        sys.exit(1)
    
    ollama_version = run_command("ollama --version", capture_output=True)
    print_status(f"Ollama found: {ollama_version.stdout.strip()}", "success")
    
    # Step 6: Check if Ollama is running
    if not check_ollama_running():
        print_status("Ollama service not running. Starting...", "warning")
        if not start_ollama():
            print_status("Failed to start Ollama service", "error")
            sys.exit(1)
    print_status("Ollama service is running", "success")
    
    # Step 7: Check for required models
    model_scenario_b = "llama3.2:3b"
    print_status(f"Checking for model {model_scenario_b}...", "info")
    if not check_model_available(model_scenario_b):
        print_status(f"Model {model_scenario_b} not found. Pulling...", "warning")
        if not pull_model(model_scenario_b):
            print_status(f"Failed to pull model {model_scenario_b}", "error")
            sys.exit(1)
    print_status(f"Model {model_scenario_b} is available", "success")
    
    # Step 8: Set environment variables
    os.environ.setdefault("OLLAMA_URL", "http://localhost:11434")
    os.environ.setdefault("LLAMA_STACK_PORT", "8321")
    os.environ.setdefault("LLAMA_STACK_HOST", "localhost")
    
    llama_stack_port = int(os.environ["LLAMA_STACK_PORT"])
    print_status("Environment variables set:", "success")
    print(f"   OLLAMA_URL={os.environ['OLLAMA_URL']}")
    print(f"   LLAMA_STACK_PORT={llama_stack_port}")
    
    # Step 9: Check if llama-stack is installed
    try:
        import llama_stack
        print_status("llama-stack is installed", "success")
    except ImportError:
        print_status("llama-stack not installed. Installing with uv...", "warning")
        run_command("uv add llama-stack opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http")
        print_status("llama-stack installed", "success")
    
    # Step 10: Check if port is available
    if not check_port_available(llama_stack_port):
        print_status(f"Port {llama_stack_port} is already in use", "error")
        print_status("Please stop the service using that port or set LLAMA_STACK_PORT to a different value", "info")
        sys.exit(1)
    
    # Step 11: Start Llama Stack server
    print("")
    print_status(f"Starting Llama Stack server on http://{os.environ['LLAMA_STACK_HOST']}:{llama_stack_port}", "success")
    print_status("Press Ctrl+C to stop the server", "info")
    print("")
    
    # Change to project directory for running llama stack
    os.chdir(project_dir)
    
    # Try to run Llama Stack using uv run (preferred) or directly
    # uv run must be executed from root directory where pyproject.toml is
    if check_command("llama", "llama"):
        run_command("llama stack run starter", check=False)
    elif check_command("uv", "uv"):
        try:
            # Run from root directory
            run_command(f"cd {root_dir} && uv run llama stack run starter", check=False)
        except Exception as e:
            print_status("Could not run llama-stack via uv run", "warning")
            # Fallback to direct Python execution
            venv_python = venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
            if venv_python.exists():
                run_command(f"{venv_python} -m llama_stack run starter", check=False)
            else:
                print_status("Could not find llama-stack CLI", "error")
                print_status(f"Try running: cd {root_dir} && uv sync", "info")
                sys.exit(1)
    else:
        print_status("Could not find llama-stack CLI or uv", "error")
        print_status(f"Try running: cd {root_dir} && uv sync", "info")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print_status("Server stopped by user", "info")
        sys.exit(0)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")
        sys.exit(1)

