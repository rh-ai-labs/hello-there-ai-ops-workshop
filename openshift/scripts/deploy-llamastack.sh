#!/bin/bash
# Deployment script for Llama Stack on OpenShift
# This script creates the necessary secrets and deploys LlamaStackDistribution

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration - Update these values based on your OpenShift setup
NAMESPACE="${NAMESPACE:-my-first-model}"
VLLM_TLS_VERIFY="${VLLM_TLS_VERIFY:-false}"
VLLM_API_TOKEN="${VLLM_API_TOKEN:-fake}"

# Deployment type: "milvus-inline", "milvus-remote", or "faiss-inline"
DEPLOYMENT_TYPE="${DEPLOYMENT_TYPE:-milvus-inline}"

# Auto-detect vLLM URL and model if not provided
AUTO_DETECT_VLLM="${AUTO_DETECT_VLLM:-true}"

echo -e "${BLUE}🚀 Deploying Llama Stack to OpenShift${NC}"
echo "=========================================="
echo -e "Namespace: ${GREEN}${NAMESPACE}${NC}"
echo -e "Deployment Type: ${GREEN}${DEPLOYMENT_TYPE}${NC}"
echo ""

# Check if oc is installed
if ! command -v oc &> /dev/null; then
    echo -e "${RED}❌ OpenShift CLI (oc) is not installed${NC}"
    echo "Please install it from: https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html"
    exit 1
fi

# Check if logged in to OpenShift
if ! oc whoami &> /dev/null; then
    echo -e "${RED}❌ Not logged in to OpenShift${NC}"
    echo "Please log in using: oc login --token=<token> --server=<openshift_cluster_url>"
    exit 1
fi

echo -e "${GREEN}✅ Logged in as: $(oc whoami)${NC}"

# Ensure namespace exists first (needed for service discovery)
echo -e "${BLUE}📦 Checking namespace...${NC}"
if ! oc get namespace "${NAMESPACE}" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Namespace ${NAMESPACE} does not exist. Creating...${NC}"
    oc create namespace "${NAMESPACE}"
fi
echo -e "${GREEN}✅ Namespace ${NAMESPACE} exists${NC}"
echo ""

# Auto-detect vLLM URL and model (unless explicitly disabled or both are provided)
if [ "$AUTO_DETECT_VLLM" != "false" ] && ([ -z "$INFERENCE_MODEL" ] || [ -z "$VLLM_URL" ]); then
    echo -e "${BLUE}🔍 Auto-detecting vLLM configuration...${NC}"
    
    # Find vLLM service (look for predictor services)
    VLLM_SERVICE=$(oc get svc -n "${NAMESPACE}" -o jsonpath='{.items[?(@.metadata.name=~".*predictor.*")].metadata.name}' 2>/dev/null | head -1 || echo "")
    
    if [ -z "$VLLM_SERVICE" ]; then
        # Try alternative: look for services with "llama" or "vllm" in name
        VLLM_SERVICE=$(oc get svc -n "${NAMESPACE}" -o jsonpath='{.items[?(@.metadata.name=~".*llama.*|.*vllm.*")].metadata.name}' 2>/dev/null | head -1 || echo "")
    fi
    
    if [ -n "$VLLM_SERVICE" ]; then
        echo -e "${GREEN}   ✅ Found vLLM service: ${VLLM_SERVICE}${NC}"
        
        # Get service port (look for port 8080 or 80)
        VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "${NAMESPACE}" -o jsonpath='{.spec.ports[?(@.targetPort==8080 || @.port==8080)].targetPort}' 2>/dev/null || echo "")
        if [ -z "$VLLM_PORT" ] || [ "$VLLM_PORT" = "null" ]; then
            VLLM_PORT=$(oc get svc "$VLLM_SERVICE" -n "${NAMESPACE}" -o jsonpath='{.spec.ports[0].targetPort}' 2>/dev/null || echo "8080")
        fi
        
        # Build vLLM URL (use internal service URL)
        VLLM_URL="http://${VLLM_SERVICE}.${NAMESPACE}.svc.cluster.local:${VLLM_PORT}/v1"
        echo -e "${GREEN}   ✅ vLLM URL: ${VLLM_URL}${NC}"
        
        # Query vLLM to get available models
        echo -e "${BLUE}   🔍 Querying vLLM for available models...${NC}"
        
        # Try to query from a pod in the cluster (more reliable)
        QUERY_POD=$(oc get pods -n "${NAMESPACE}" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null | head -1 || echo "")
        
        if [ -n "$QUERY_POD" ]; then
            # Check if curl is available in the pod
            if oc exec -n "${NAMESPACE}" "$QUERY_POD" -- which curl > /dev/null 2>&1; then
                MODELS_JSON=$(oc exec -n "${NAMESPACE}" "$QUERY_POD" -- \
                    curl -s "${VLLM_URL}/models" 2>/dev/null || echo "")
            else
                # Try using a temporary debug pod
                MODELS_JSON=$(oc run -n "${NAMESPACE}" --rm -i --restart=Never --image=curlimages/curl:latest -- curl -s "${VLLM_URL}/models" 2>/dev/null || echo "")
            fi
        else
            # Fallback: try from local machine (might not work if service is internal-only)
            MODELS_JSON=$(curl -s -k "${VLLM_URL}/models" 2>/dev/null || echo "")
        fi
        
        if [ -n "$MODELS_JSON" ] && echo "$MODELS_JSON" | grep -q "data"; then
            # Extract first model ID
            INFERENCE_MODEL=$(echo "$MODELS_JSON" | jq -r '.data[0].id' 2>/dev/null || echo "")
            
            if [ -n "$INFERENCE_MODEL" ] && [ "$INFERENCE_MODEL" != "null" ]; then
                echo -e "${GREEN}   ✅ Found vLLM model: ${INFERENCE_MODEL}${NC}"
            else
                echo -e "${YELLOW}   ⚠️  Could not parse model ID from response${NC}"
                INFERENCE_MODEL="llama-32-3b-instruct"
                echo -e "${YELLOW}   Using default: ${INFERENCE_MODEL}${NC}"
            fi
        else
            echo -e "${YELLOW}   ⚠️  Could not query vLLM models endpoint${NC}"
            echo -e "${YELLOW}   Using default model identifier${NC}"
            INFERENCE_MODEL="llama-32-3b-instruct"
        fi
    else
        echo -e "${YELLOW}   ⚠️  Could not find vLLM service${NC}"
        echo -e "${YELLOW}   Using defaults (you may need to set VLLM_URL and INFERENCE_MODEL manually)${NC}"
        VLLM_URL="http://llama-32-3b-instruct-predictor.${NAMESPACE}.svc.cluster.local:8080/v1"
        INFERENCE_MODEL="llama-32-3b-instruct"
    fi
    echo ""
else
    # Use provided values or defaults (only if auto-detect is disabled)
    if [ -z "$VLLM_URL" ]; then
        VLLM_URL="http://llama-32-3b-instruct-predictor.${NAMESPACE}.svc.cluster.local:8080/v1"
    fi
    if [ -z "$INFERENCE_MODEL" ]; then
        INFERENCE_MODEL="llama-32-3b-instruct"
    fi
fi

# Display final configuration
echo -e "${BLUE}📋 Final Configuration:${NC}"
echo -e "   Model: ${CYAN}${INFERENCE_MODEL}${NC}"
echo -e "   vLLM URL: ${CYAN}${VLLM_URL}${NC}"
echo ""

echo -e "${BLUE}📦 Checking namespace...${NC}"
if ! oc get namespace "${NAMESPACE}" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Namespace ${NAMESPACE} does not exist. Creating...${NC}"
    oc create namespace "${NAMESPACE}"
fi
echo -e "${GREEN}✅ Namespace ${NAMESPACE} exists${NC}"

# Create or update secret
echo -e "${BLUE}🔐 Creating inference model secret...${NC}"
if [ -f "${SECRETS_DIR}/llama-stack-inference-model-secret.yaml" ]; then
    # Use manifest file if it exists
    oc apply -f "${SECRETS_DIR}/llama-stack-inference-model-secret.yaml"
else
    # Create from command line
    oc create secret generic llama-stack-inference-model-secret \
      --from-literal=INFERENCE_MODEL="${INFERENCE_MODEL}" \
      --from-literal=VLLM_URL="${VLLM_URL}" \
      --from-literal=VLLM_TLS_VERIFY="${VLLM_TLS_VERIFY}" \
      --from-literal=VLLM_API_TOKEN="${VLLM_API_TOKEN}" \
      --namespace="${NAMESPACE}" \
      --dry-run=client -o yaml | oc apply -f -
fi

echo -e "${GREEN}✅ Secret created/updated${NC}"

# Deploy LlamaStackDistribution based on type
echo -e "${BLUE}🚀 Deploying LlamaStackDistribution (${DEPLOYMENT_TYPE})...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFESTS_DIR="${SCRIPT_DIR}/../manifests/llamastack"
SECRETS_DIR="${SCRIPT_DIR}/../manifests/secrets"

case "${DEPLOYMENT_TYPE}" in
    milvus-inline)
        CR_FILE="${MANIFESTS_DIR}/llamastackdistribution-inline-milvus.yaml"
        ;;
    faiss-inline)
        CR_FILE="${MANIFESTS_DIR}/llamastackdistribution-inline-faiss.yaml"
        ;;
    milvus-remote)
        CR_FILE="${MANIFESTS_DIR}/llamastackdistribution-remote-milvus.yaml"
        # Check if Milvus secret exists
        if ! oc get secret milvus-secret -n "${NAMESPACE}" &> /dev/null; then
            echo -e "${YELLOW}⚠️  Milvus secret not found. Creating from template...${NC}"
            echo -e "${YELLOW}⚠️  Please update milvus-secret.yaml with your actual Milvus credentials${NC}"
            oc apply -f "${SECRETS_DIR}/milvus-secret.yaml" || {
                echo -e "${RED}❌ Failed to create Milvus secret${NC}"
                echo "Please create it manually with your Milvus credentials"
                exit 1
            }
        fi
        ;;
    *)
        echo -e "${RED}❌ Unknown deployment type: ${DEPLOYMENT_TYPE}${NC}"
        echo "Valid options: milvus-inline, faiss-inline, milvus-remote"
        exit 1
        ;;
esac

if [ ! -f "${CR_FILE}" ]; then
    echo -e "${RED}❌ CR file not found: ${CR_FILE}${NC}"
    exit 1
fi

# Update namespace in CR file if needed (in case it's different)
sed "s/namespace: my-first-model/namespace: ${NAMESPACE}/g" "${CR_FILE}" | oc apply -f -

echo -e "${GREEN}✅ LlamaStackDistribution deployed${NC}"

# Wait for pod to be ready
echo -e "${BLUE}⏳ Waiting for Llama Stack pod to be ready...${NC}"
oc wait --for=condition=ready pod -l app=llama-stack -n "${NAMESPACE}" --timeout=300s || {
    echo -e "${YELLOW}⚠️  Pod not ready yet. Check status with:${NC}"
    echo "  oc get pods -n ${NAMESPACE}"
    echo "  oc logs -l app=llama-stack -n ${NAMESPACE}"
}

# Show pod status
echo ""
echo -e "${BLUE}📊 Pod Status:${NC}"
oc get pods -n "${NAMESPACE}" -l app=llama-stack

# Create Route for external access (optional)
CREATE_ROUTE="${CREATE_ROUTE:-true}"
if [ "$CREATE_ROUTE" = "true" ]; then
    echo -e "${BLUE}🌐 Creating Route for external access...${NC}"
    ROUTE_FILE="${MANIFESTS_DIR}/llamastack-route.yaml"
    if [ -f "${ROUTE_FILE}" ]; then
        sed "s/namespace: my-first-model/namespace: ${NAMESPACE}/g" "${ROUTE_FILE}" | oc apply -f -
        echo -e "${GREEN}✅ Route created${NC}"
        
        # Get route URL
        ROUTE_URL=$(oc get route llamastack-route -n "${NAMESPACE}" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
        if [ -n "$ROUTE_URL" ]; then
            ROUTE_FULL_URL="https://${ROUTE_URL}"
            echo -e "${GREEN}✅ Route URL: ${CYAN}${ROUTE_FULL_URL}${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Route file not found, skipping route creation${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Check pod logs: oc logs -l app=llama-stack -n ${NAMESPACE}"
echo "2. Check service: oc get svc -n ${NAMESPACE}"
if [ "$CREATE_ROUTE" = "true" ] && [ -n "$ROUTE_URL" ]; then
    echo "3. Access externally via Route: ${ROUTE_FULL_URL}"
    echo "4. Or port forward for local access: oc port-forward -n ${NAMESPACE} svc/lsd-llama-milvus-inline-service 8321:8321"
else
    echo "3. Create Route for external access: oc apply -f ${MANIFESTS_DIR}/llamastack-route.yaml"
    echo "4. Or port forward to access locally: oc port-forward -n ${NAMESPACE} svc/lsd-llama-milvus-inline-service 8321:8321"
fi

