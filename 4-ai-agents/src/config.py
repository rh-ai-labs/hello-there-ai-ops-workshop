"""
Centralized configuration for LlamaStack and related services.

Loads configuration from .env file or environment variables.
Simple and explicit - no magic auto-detection.
"""

import os
from pathlib import Path

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    # Load .env file from the notebooks directory or parent directory
    env_paths = [
        Path(__file__).parent.parent / ".env",  # 4-ai-agents/.env
        Path(__file__).parent / ".env",         # src/.env (fallback)
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    # python-dotenv not installed, just use environment variables
    pass

# Suppress SSL warnings for OpenShift self-signed certificates
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass


def is_inside_openshift() -> bool:
    """
    Detect if we're running inside an OpenShift/Kubernetes cluster.
    
    Returns:
        True if running inside cluster, False otherwise
    """
    # Check for Kubernetes service account (most reliable indicator)
    if Path("/var/run/secrets/kubernetes.io/serviceaccount").exists():
        return True
    
    # Check for KUBERNETES_SERVICE_HOST environment variable
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        return True
    
    return False


# Configuration values - simple and explicit
# Environment variables take precedence (set via .env file or system env)
LLAMA_STACK_URL = os.getenv("LLAMA_STACK_URL", "").rstrip("/")
MODEL = os.getenv("LLAMA_MODEL", "vllm-inference/llama-32-3b-instruct")
NAMESPACE = os.getenv("NAMESPACE", "my-first-model")
MCP_MONGODB_URL = os.getenv("MCP_MONGODB_URL", "").rstrip("/")
INSIDE_CLUSTER = is_inside_openshift()

# Auto-detect URLs if not explicitly set
if not LLAMA_STACK_URL:
    if INSIDE_CLUSTER:
        # Inside cluster: use service URL
        LLAMA_STACK_URL = f"http://lsd-llama-milvus-inline-service.{NAMESPACE}.svc.cluster.local:8321"
    else:
        # Outside cluster: try to get route via oc command
        try:
            import subprocess
            result = subprocess.run(
                ["oc", "get", "route", "llamastack-route", "-n", NAMESPACE,
                 "-o", "jsonpath={.spec.host}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout:
                LLAMA_STACK_URL = f"https://{result.stdout.strip()}"
            else:
                LLAMA_STACK_URL = "http://localhost:8321"
        except Exception:
            LLAMA_STACK_URL = "http://localhost:8321"

if not MCP_MONGODB_URL:
    if INSIDE_CLUSTER:
        MCP_MONGODB_URL = f"http://mongodb-mcp-server.{NAMESPACE}.svc.cluster.local:3000"
    else:
        # Try route or default to localhost
        try:
            import subprocess
            result = subprocess.run(
                ["oc", "get", "route", "mongodb-mcp-server-route", "-n", NAMESPACE,
                 "-o", "jsonpath={.spec.host}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout:
                MCP_MONGODB_URL = f"https://{result.stdout.strip()}"
            else:
                MCP_MONGODB_URL = "http://localhost:3000"
        except Exception:
            MCP_MONGODB_URL = "http://localhost:3000"

# Export configuration dict for easy access
CONFIG = {
    "llamastack_url": LLAMA_STACK_URL,
    "mcp_mongodb_url": MCP_MONGODB_URL,
    "model": MODEL,
    "namespace": NAMESPACE,
    "inside_cluster": INSIDE_CLUSTER,
}

