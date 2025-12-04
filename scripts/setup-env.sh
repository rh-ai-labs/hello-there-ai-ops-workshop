#!/bin/bash
# Setup .env file for LlamaStack notebooks
# Automatically detects environment and generates .env file
# Run from project root: ./scripts/setup-env.sh

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"
ENV_EXAMPLE="$PROJECT_DIR/.env.example"

echo -e "${BLUE}🔧 Setting up .env file for LlamaStack notebooks${NC}"
echo "=========================================="

# Detect if inside OpenShift/Kubernetes cluster
INSIDE_CLUSTER=false
if [ -d "/var/run/secrets/kubernetes.io/serviceaccount" ]; then
    INSIDE_CLUSTER=true
    echo -e "${GREEN}✅ Detected: Running inside OpenShift cluster${NC}"
elif [ -n "$KUBERNETES_SERVICE_HOST" ]; then
    INSIDE_CLUSTER=true
    echo -e "${GREEN}✅ Detected: Running inside Kubernetes cluster${NC}"
else
    echo -e "${YELLOW}📍 Detected: Running outside cluster${NC}"
fi

# Get namespace
if [ "$INSIDE_CLUSTER" = true ]; then
    # Try to read from service account
    if [ -f "/var/run/secrets/kubernetes.io/serviceaccount/namespace" ]; then
        NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
    else
        NAMESPACE="${NAMESPACE:-my-first-model}"
    fi
else
    NAMESPACE="${NAMESPACE:-my-first-model}"
fi

echo "📦 Namespace: $NAMESPACE"

# Function to get route URL
get_route_url() {
    local route_name=$1
    local namespace=$2
    
    if command -v oc &> /dev/null; then
        if oc whoami &> /dev/null; then
            local host=$(oc get route "$route_name" -n "$namespace" -o jsonpath='{.spec.host}' 2>/dev/null)
            if [ -n "$host" ]; then
                echo "https://$host"
                return 0
            fi
        fi
    fi
    return 1
}

# Function to get service URL
get_service_url() {
    local service_name=$1
    local namespace=$2
    local port=${3:-8321}
    
    echo "http://${service_name}.${namespace}.svc.cluster.local:${port}"
}

# Detect LlamaStack URL (always reset - ignore existing env vars)
if [ "$INSIDE_CLUSTER" = true ]; then
    # Inside cluster: use service URL
    LLAMA_STACK_URL=$(get_service_url "lsd-llama-milvus-inline-service" "$NAMESPACE" "8321")
    echo -e "${GREEN}✅ Detected LlamaStack service URL${NC}"
else
    # Outside cluster: try to get route
    if route_url=$(get_route_url "llamastack-route" "$NAMESPACE"); then
        LLAMA_STACK_URL="$route_url"
        echo -e "${GREEN}✅ Detected LlamaStack route URL${NC}"
    else
        echo -e "${RED}❌ Could not detect LlamaStack route${NC}"
        echo -e "${YELLOW}⚠️  Please set LLAMA_STACK_URL manually${NC}"
        echo "   💡 Get route URL: oc get route llamastack-route -n $NAMESPACE -o jsonpath='{.spec.host}'"
        echo "   💡 Or use port-forwarding: export LLAMA_STACK_URL='http://localhost:8321'"
        LLAMA_STACK_URL=""
    fi
fi

# Detect MongoDB MCP URL (always reset - ignore existing env vars)
if [ "$INSIDE_CLUSTER" = true ]; then
    # Inside cluster: use service URL
    MCP_MONGODB_URL=$(get_service_url "mongodb-mcp-server" "$NAMESPACE" "3000")
    echo -e "${GREEN}✅ Detected MongoDB MCP service URL${NC}"
else
    # Outside cluster: try to get route (try both possible route names)
    if route_url=$(get_route_url "mongodb-mcp-server" "$NAMESPACE"); then
        MCP_MONGODB_URL="$route_url"
        echo -e "${GREEN}✅ Detected MongoDB MCP route URL${NC}"
    elif route_url=$(get_route_url "mongodb-mcp-server-route" "$NAMESPACE"); then
        MCP_MONGODB_URL="$route_url"
        echo -e "${GREEN}✅ Detected MongoDB MCP route URL${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not detect MongoDB MCP route (optional)${NC}"
        MCP_MONGODB_URL=""
    fi
fi

# Get model (always reset to defaults - ignore existing env vars)
MODEL="vllm-inference/llama-32-3b-instruct"
OPENAI_MODEL="vllm-inference/llama-32-3b-instruct"

# Detect vLLM API Base URL (always reset - ignore existing env vars)
# Check if oc command is available
OC_AVAILABLE=false
if command -v oc &> /dev/null && oc whoami &> /dev/null; then
    OC_AVAILABLE=true
fi

if [ "$INSIDE_CLUSTER" = true ]; then
    # Inside cluster: try to find vLLM predictor service
    VLLM_SERVICE=""
    if [ "$OC_AVAILABLE" = true ]; then
        # Strategy 1: Use jsonpath to find predictor services
        VLLM_SERVICE=$(oc get svc -n "$NAMESPACE" -o jsonpath='{.items[?(@.metadata.name=~".*predictor.*")].metadata.name}' 2>/dev/null | head -1 || echo "")
        
        # Strategy 2: Fallback to grep if jsonpath fails
        if [ -z "$VLLM_SERVICE" ]; then
            VLLM_SERVICE=$(oc get svc -n "$NAMESPACE" 2>/dev/null | grep -i predictor | awk '{print $1}' | head -1 || echo "")
        fi
        
        # Strategy 3: Try specific known service names
        if [ -z "$VLLM_SERVICE" ]; then
            for svc_name in "llama-32-3b-instruct-predictor"; do
                if oc get svc "$svc_name" -n "$NAMESPACE" &>/dev/null; then
                    VLLM_SERVICE="$svc_name"
                    break
                fi
            done
        fi
    fi
    
    if [ -n "$VLLM_SERVICE" ]; then
        # Get port (prefer 8080, fallback to first port, then default to 8080)
        VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "$NAMESPACE" -o jsonpath='{.spec.ports[?(@.targetPort==8080 || @.port==8080)].targetPort}' 2>/dev/null || echo "")
        if [ -z "$VLLM_PORT" ] || [ "$VLLM_PORT" = "null" ]; then
            VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].targetPort}' 2>/dev/null || echo "")
        fi
        if [ -z "$VLLM_PORT" ] || [ "$VLLM_PORT" = "null" ]; then
            VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "8080")
        fi
        VLLM_API_BASE="http://${VLLM_SERVICE}.${NAMESPACE}.svc.cluster.local:${VLLM_PORT}/v1"
        echo -e "${GREEN}✅ Detected vLLM service URL: $VLLM_API_BASE${NC}"
    else
        echo -e "${RED}❌ Could not detect vLLM service - REQUIRED for Module 3${NC}"
        if [ "$OC_AVAILABLE" = false ]; then
            echo -e "${YELLOW}   💡 oc command not available or not authenticated${NC}"
        else
            echo -e "${YELLOW}   💡 Make sure the predictor service is deployed${NC}"
            echo -e "${YELLOW}   💡 Check: oc get svc -n $NAMESPACE | grep predictor${NC}"
        fi
        VLLM_API_BASE=""
    fi
else
    # Outside cluster: try to find vLLM route
    VLLM_SERVICE=""
    VLLM_ROUTE=""
    
    if [ "$OC_AVAILABLE" = true ]; then
        # First, find the predictor service (try multiple methods)
        # Strategy 1: Use jsonpath to find predictor services
        VLLM_SERVICE=$(oc get svc -n "$NAMESPACE" -o jsonpath='{.items[?(@.metadata.name=~".*predictor.*")].metadata.name}' 2>/dev/null | head -1 || echo "")
        
        # Strategy 2: Fallback to grep if jsonpath fails
        if [ -z "$VLLM_SERVICE" ]; then
            VLLM_SERVICE=$(oc get svc -n "$NAMESPACE" 2>/dev/null | grep -i predictor | awk '{print $1}' | head -1 || echo "")
        fi
        
        # Strategy 3: Try specific known service names
        if [ -z "$VLLM_SERVICE" ]; then
            for svc_name in "llama-32-3b-instruct-predictor"; do
                if oc get svc "$svc_name" -n "$NAMESPACE" &>/dev/null; then
                    VLLM_SERVICE="$svc_name"
                    break
                fi
            done
        fi
        
        if [ -n "$VLLM_SERVICE" ]; then
            # Try multiple strategies to find the route
            # Strategy 1: Find route that points to the predictor service
            VLLM_ROUTE=$(oc get route -n "$NAMESPACE" -o jsonpath="{.items[?(@.spec.to.name==\"$VLLM_SERVICE\")].spec.host}" 2>/dev/null | head -1 || echo "")
            
            # Strategy 2: Find route by name pattern using jsonpath
            if [ -z "$VLLM_ROUTE" ]; then
                VLLM_ROUTE=$(oc get route -n "$NAMESPACE" -o jsonpath='{.items[?(@.metadata.name=~".*predictor.*|.*inference.*|.*vllm.*")].spec.host}' 2>/dev/null | head -1 || echo "")
            fi
            
            # Strategy 3: Find route by name pattern using grep (more reliable for hostname extraction)
            if [ -z "$VLLM_ROUTE" ]; then
                # Get route name first, then extract hostname
                ROUTE_NAME=$(oc get route -n "$NAMESPACE" 2>/dev/null | grep -iE "predictor|inference|vllm" | awk '{print $1}' | head -1 || echo "")
                if [ -n "$ROUTE_NAME" ]; then
                    VLLM_ROUTE=$(oc get route "$ROUTE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
                fi
            fi
            
            # Strategy 4: Try common route naming patterns
            if [ -z "$VLLM_ROUTE" ]; then
                SERVICE_BASE=$(echo "$VLLM_SERVICE" | sed 's/-predictor$//' | sed 's/-service$//')
                for route_pattern in "${SERVICE_BASE}-route" "${SERVICE_BASE}" "vllm-route" "predictor-route" "vllm-predictor-route"; do
                    if route_url=$(get_route_url "$route_pattern" "$NAMESPACE" 2>/dev/null); then
                        VLLM_ROUTE="${route_url#https://}"
                        break
                    fi
                done
            fi
        fi
    fi
    
    if [ -z "$VLLM_SERVICE" ]; then
        echo -e "${RED}❌ Could not find vLLM predictor service${NC}"
        if [ "$OC_AVAILABLE" = false ]; then
            echo -e "${YELLOW}   💡 oc command not available or not authenticated${NC}"
        else
            echo -e "${YELLOW}   💡 Make sure the predictor service is deployed${NC}"
            echo -e "${YELLOW}   💡 Check: oc get svc -n $NAMESPACE | grep predictor${NC}"
        fi
        VLLM_API_BASE=""
    elif [ -n "$VLLM_ROUTE" ]; then
        VLLM_API_BASE="https://${VLLM_ROUTE}/v1"
        echo -e "${GREEN}✅ Detected vLLM route URL: $VLLM_API_BASE${NC}"
    else
        # No route found - use service URL as fallback (works with port-forwarding)
        VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "$NAMESPACE" -o jsonpath='{.spec.ports[?(@.targetPort==8080 || @.port==8080)].targetPort}' 2>/dev/null || echo "")
        if [ -z "$VLLM_PORT" ] || [ "$VLLM_PORT" = "null" ]; then
            VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].targetPort}' 2>/dev/null || echo "")
        fi
        if [ -z "$VLLM_PORT" ] || [ "$VLLM_PORT" = "null" ]; then
            VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "8080")
        fi
        SERVICE_URL="http://${VLLM_SERVICE}.${NAMESPACE}.svc.cluster.local:${VLLM_PORT}/v1"
        VLLM_API_BASE="$SERVICE_URL"
        echo -e "${YELLOW}⚠️  No vLLM route found - using service URL${NC}"
        echo -e "${YELLOW}   Service URL: $SERVICE_URL${NC}"
        echo -e "${YELLOW}   💡 Note: Service URL only works inside cluster or with port-forwarding${NC}"
        echo -e "${YELLOW}   💡 For external access, create a route:${NC}"
        echo -e "${BLUE}      oc create route edge vllm-predictor-route \\${NC}"
        echo -e "${BLUE}        --service=$VLLM_SERVICE \\${NC}"
        echo -e "${BLUE}        --port=$VLLM_PORT \\${NC}"
        echo -e "${BLUE}        -n $NAMESPACE${NC}"
        echo -e "${YELLOW}   Or use port-forwarding:${NC}"
        echo -e "${BLUE}      oc port-forward svc/$VLLM_SERVICE $VLLM_PORT:$VLLM_PORT -n $NAMESPACE${NC}"
        echo -e "${BLUE}      Then use: http://localhost:$VLLM_PORT/v1${NC}"
    fi
fi

# Ensure VLLM_API_BASE is set (use default fallback if not detected)
if [ -z "$VLLM_API_BASE" ]; then
    # Default fallback: use standard predictor service name and namespace
    DEFAULT_SERVICE="llama-32-3b-instruct-predictor"
    DEFAULT_PORT="80"
    VLLM_API_BASE="http://${DEFAULT_SERVICE}.${NAMESPACE}.svc.cluster.local:${DEFAULT_PORT}/v1"
    echo -e "${YELLOW}⚠️  Using default vLLM API Base URL: $VLLM_API_BASE${NC}"
    echo -e "${YELLOW}   💡 If this is incorrect, edit .env file or ensure the service is deployed${NC}"
    echo -e "${YELLOW}   💡 Note: Port 80 is default, but vLLM typically uses port 8080${NC}"
fi

# Generate .env file
echo ""
echo -e "${BLUE}📝 Generating .env file...${NC}"

cat > "$ENV_FILE" << EOF
# LlamaStack Configuration
# Auto-generated by scripts/setup-env.sh
# Environment: $([ "$INSIDE_CLUSTER" = true ] && echo "Inside OpenShift cluster" || echo "Outside OpenShift cluster")
# Generated: $(date)

# LlamaStack URL
# Inside cluster: Service URL (auto-detected)
# Outside cluster: Route URL (auto-detected via oc command)
# If auto-detection fails, set manually:
# LLAMA_STACK_URL=https://llamastack-route-my-first-model.apps.ocp.example.com
LLAMA_STACK_URL=$LLAMA_STACK_URL

# Model identifier
# Use the full identifier from LlamaStack
LLAMA_MODEL=$MODEL

# OpenShift namespace
NAMESPACE=$NAMESPACE

# MongoDB MCP Server URL (optional, only needed for Module 4 - AI Agents)
# Inside cluster: Service URL (auto-detected)
# Outside cluster: Route URL (auto-detected via oc command)
# If auto-detection fails, set manually:
# MCP_MONGODB_URL=https://mongodb-mcp-server-route-my-first-model.apps.ocp.example.com
MCP_MONGODB_URL=$MCP_MONGODB_URL

# vLLM API Base URL (REQUIRED for Module 3 - AI Evaluation, Notebook 05)
# Inside cluster: Service URL (auto-detected)
# Outside cluster: Route URL (auto-detected via oc command)
# If auto-detection fails, set manually:
# VLLM_API_BASE=https://model-predictor-route-my-first-model.apps.ocp.example.com/v1
VLLM_API_BASE=$VLLM_API_BASE

# OpenAI-compatible model name (for vLLM, used in Module 3 - AI Evaluation, Notebook 05)
OPENAI_MODEL=$OPENAI_MODEL
EOF

echo -e "${GREEN}✅ .env file created: $ENV_FILE${NC}"
echo ""
echo "📋 Configuration:"
echo "   LlamaStack URL: ${LLAMA_STACK_URL:-<not set - please configure>}"
echo "   MongoDB MCP URL: ${MCP_MONGODB_URL:-<not set - optional (Module 4)>}"
echo "   vLLM API Base: ${VLLM_API_BASE:-<not set - REQUIRED (Module 3)>}"
echo "   Model: $MODEL"
echo "   OpenAI Model: $OPENAI_MODEL"
echo "   Namespace: $NAMESPACE"
echo ""

if [ -z "$LLAMA_STACK_URL" ]; then
    echo -e "${RED}⚠️  WARNING: LLAMA_STACK_URL is not set!${NC}"
    echo "   Please configure it manually:"
    echo "   1. Edit $ENV_FILE"
    echo "   2. Or set: export LLAMA_STACK_URL='https://<your-route>'"
    echo ""
fi

if [ -z "$VLLM_API_BASE" ]; then
    echo -e "${RED}⚠️  WARNING: VLLM_API_BASE is not set!${NC}"
    echo -e "${RED}   This is REQUIRED for Module 3 (AI Evaluation)${NC}"
    echo "   Please configure it manually:"
    echo "   1. Create a route for the predictor service (see instructions above)"
    echo "   2. Or edit $ENV_FILE and set VLLM_API_BASE"
    echo "   3. Or set: export VLLM_API_BASE='https://<route-host>/v1'"
    echo ""
elif [[ "$VLLM_API_BASE" == http://*.svc.cluster.local* ]] && [ "$INSIDE_CLUSTER" != true ]; then
    echo -e "${YELLOW}⚠️  NOTE: Using vLLM service URL (not route)${NC}"
    echo -e "${YELLOW}   This works if you're using port-forwarding or VPN${NC}"
    echo -e "${YELLOW}   For external access, consider creating a route (see instructions above)${NC}"
    echo ""
fi

echo "💡 To override any value, edit $ENV_FILE directly"
echo "💡 This script always resets all variables - it does not preserve existing env vars"
echo "💡 To use custom values, edit $ENV_FILE after running this script"
