"""
Centralized configuration for LlamaStack and related services.

This module provides a shared configuration system for all modules.
Loads configuration from .env file at the root or environment variables.
Auto-detects OpenShift vs localhost environment.
"""

import os
from pathlib import Path

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    # Load .env file from the root directory
    root_dir = Path(__file__).parent.parent
    env_path = root_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
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
VLLM_API_BASE = os.getenv("VLLM_API_BASE", "").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "vllm-inference/llama-32-3b-instruct")
INSIDE_CLUSTER = is_inside_openshift()

# Auto-detect URLs if not explicitly set
# Priority: 1) Environment variable, 2) OpenShift detection, 3) localhost fallback
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
                # Don't default to localhost - require explicit configuration
                LLAMA_STACK_URL = ""
        except Exception:
            # Don't default to localhost - require explicit configuration
            LLAMA_STACK_URL = ""

if not MCP_MONGODB_URL:
    if INSIDE_CLUSTER:
        MCP_MONGODB_URL = f"http://mongodb-mcp-server.{NAMESPACE}.svc.cluster.local:3000"
    else:
        # Try route or leave empty (don't default to localhost)
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
                MCP_MONGODB_URL = ""
        except Exception:
            MCP_MONGODB_URL = ""

# Auto-detect vLLM URL if not explicitly set
if not VLLM_API_BASE:
    if INSIDE_CLUSTER:
        # Inside cluster: try to find vLLM predictor service
        try:
            import subprocess
            # Look for predictor services (vLLM inference models)
            result = subprocess.run(
                ["oc", "get", "svc", "-n", NAMESPACE,
                 "-o", "jsonpath={.items[?(@.metadata.name=~'.*predictor.*')].metadata.name}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout:
                vllm_service = result.stdout.strip().split()[0] if result.stdout.strip() else None
                if vllm_service:
                    VLLM_API_BASE = f"http://{vllm_service}.{NAMESPACE}.svc.cluster.local:8080/v1"
        except Exception:
            pass
    else:
        # Outside cluster: try to find vLLM route
        try:
            import subprocess
            # Try common route patterns for vLLM/inference models
            route_patterns = ["*-predictor-route", "*-inference-route", "*-vllm-route"]
            for pattern in route_patterns:
                result = subprocess.run(
                    ["oc", "get", "route", "-n", NAMESPACE,
                     "-o", "jsonpath={.items[?(@.metadata.name=~'"+pattern+"')].spec.host}"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout:
                    host = result.stdout.strip().split()[0] if result.stdout.strip() else None
                    if host:
                        VLLM_API_BASE = f"https://{host}/v1"
                        break
        except Exception:
            pass

# Export configuration dict for easy access
CONFIG = {
    "llamastack_url": LLAMA_STACK_URL,
    "mcp_mongodb_url": MCP_MONGODB_URL,
    "vllm_api_base": VLLM_API_BASE,
    "openai_model": OPENAI_MODEL,
    "model": MODEL,
    "namespace": NAMESPACE,
    "inside_cluster": INSIDE_CLUSTER,
}

