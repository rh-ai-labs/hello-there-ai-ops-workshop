#!/bin/bash
# Test script for Llama Stack deployment on OpenShift

set -e

NAMESPACE="${NAMESPACE:-my-first-model}"
SERVICE_NAME="${SERVICE_NAME:-lsd-llama-milvus-inline-service}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}🧪 Testing Llama Stack Deployment${NC}"
echo "=========================================="
echo ""

# Check pod status
check_pod_status() {
    echo -e "${BLUE}📊 Pod Status:${NC}"
    POD_STATUS=$(oc get pods -n "$NAMESPACE" -l app=llama-stack -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "")
    POD_NAME=$(oc get pods -n "$NAMESPACE" -l app=llama-stack -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    if [ "$POD_STATUS" = "Running" ]; then
        echo -e "   ${GREEN}✅ Pod is running: ${CYAN}${POD_NAME}${NC}"
        READY=$(oc get pods -n "$NAMESPACE" -l app=llama-stack -o jsonpath='{.items[0].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || echo "")
        if [ "$READY" = "True" ]; then
            echo -e "   ${GREEN}✅ Pod is ready${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Pod is not ready yet${NC}"
        fi
    else
        echo -e "   ${RED}❌ Pod status: ${POD_STATUS}${NC}"
    fi
    echo ""
}

# Check service status
check_service_status() {
    echo -e "${BLUE}🔌 Service Status:${NC}"
    if oc get svc "$SERVICE_NAME" -n "$NAMESPACE" &> /dev/null; then
        echo -e "   ${GREEN}✅ Service exists: ${CYAN}${SERVICE_NAME}${NC}"
        SERVICE_IP=$(oc get svc "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}' 2>/dev/null || echo "")
        SERVICE_PORT=$(oc get svc "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "")
        echo -e "   Cluster IP: ${CYAN}${SERVICE_IP}${NC}"
        echo -e "   Port: ${CYAN}${SERVICE_PORT}${NC}"
        
        # Check endpoints
        ENDPOINTS=$(oc get endpoints "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null || echo "")
        if [ -n "$ENDPOINTS" ]; then
            echo -e "   ${GREEN}✅ Service has endpoints: ${CYAN}${ENDPOINTS}${NC}"
        else
            echo -e "   ${RED}❌ Service has no endpoints${NC}"
        fi
        
        # Test service connectivity from within cluster
        echo -e "   Testing service connectivity..."
        POD_NAME=$(oc get pods -n "$NAMESPACE" -l app=llama-stack -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
        if [ -n "$POD_NAME" ]; then
            SERVICE_URL="http://${SERVICE_NAME}.${NAMESPACE}.svc.cluster.local:${SERVICE_PORT}"
            # Test /v1/models endpoint instead of /health (which may not exist)
            HTTP_CODE=$(oc exec "$POD_NAME" -n "$NAMESPACE" -- curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${SERVICE_URL}/v1/models" 2>/dev/null || echo "000")
            if [ "$HTTP_CODE" = "200" ]; then
                echo -e "   ${GREEN}✅ Service is accessible from pod (HTTP 200)${NC}"
            else
                echo -e "   ${YELLOW}⚠️  Service test returned: ${HTTP_CODE}${NC}"
            fi
        fi
    else
        echo -e "   ${RED}❌ Service not found: ${SERVICE_NAME}${NC}"
    fi
    echo ""
}

# Check route status
check_route_status() {
    echo -e "${BLUE}🌐 Route Status:${NC}"
    ROUTE_HOST=$(oc get route llamastack-route -n "$NAMESPACE" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
    if [ -n "$ROUTE_HOST" ]; then
        echo -e "   ${GREEN}✅ Route exists: ${CYAN}llamastack-route${NC}"
        echo -e "   Host: ${CYAN}${ROUTE_HOST}${NC}"
        
        ROUTE_URL="https://${ROUTE_HOST}"
        echo -e "   Testing route connectivity..."
        # Test /v1/models endpoint instead of /health (which may not exist)
        HTTP_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" --max-time 10 "${ROUTE_URL}/v1/models" 2>/dev/null || echo "000")
        if [ "$HTTP_CODE" = "200" ]; then
            echo -e "   ${GREEN}✅ Route is accessible externally (HTTP 200)${NC}"
            echo -e "   ${GREEN}✅ Route URL: ${CYAN}${ROUTE_URL}${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Route test returned: ${HTTP_CODE}${NC}"
        fi
    else
        echo -e "   ${YELLOW}⚠️  Route not found${NC}"
        echo -e "   ${CYAN}💡 Create route with: oc apply -f manifests/llamastack-route.yaml${NC}"
    fi
    echo ""
}

# Check if we can access Llama Stack
check_access() {
    # Try to get route URL first
    ROUTE_HOST=$(oc get route llamastack-route -n "$NAMESPACE" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
    if [ -n "$ROUTE_HOST" ]; then
        BASE_URL="https://$ROUTE_HOST"
        echo -e "${GREEN}✅ Found Route: ${CYAN}${BASE_URL}${NC}"
        export LLAMA_STACK_BASE_URL="$BASE_URL"
        return 0
    fi
    
    # Fallback to localhost (port-forward)
    if curl -s http://localhost:8321/v1/models > /dev/null 2>&1; then
        BASE_URL="http://localhost:8321"
        export LLAMA_STACK_BASE_URL="$BASE_URL"
        return 0
    fi
    
    echo -e "${YELLOW}⚠️  Llama Stack not accessible${NC}"
    echo -e "${CYAN}💡 Options:${NC}"
    echo "   1. Create Route: oc apply -f manifests/llamastack-route.yaml"
    echo "   2. Start port-forward: oc port-forward -n $NAMESPACE svc/$SERVICE_NAME 8321:8321"
    return 1
}

# Test health endpoint
test_health() {
    BASE_URL="${LLAMA_STACK_BASE_URL:-http://localhost:8321}"
    echo -e "${BLUE}1️⃣  Testing Health Endpoint${NC}"
    echo "   GET ${BASE_URL}/health"
    HTTP_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" --max-time 10 "${BASE_URL}/health" 2>/dev/null || echo "000")
    RESPONSE=$(curl -s -k "${BASE_URL}/health" 2>/dev/null || echo "")
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "   ${GREEN}✅ Health check passed (HTTP 200)${NC}"
        if [ -n "$RESPONSE" ]; then
            echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        fi
    elif [ "$HTTP_CODE" = "404" ]; then
        echo -e "   ${YELLOW}⚠️  /health endpoint not found (404) - trying /v1/health${NC}"
        HTTP_CODE_V1=$(curl -s -k -o /dev/null -w "%{http_code}" --max-time 10 "${BASE_URL}/v1/health" 2>/dev/null || echo "000")
        if [ "$HTTP_CODE_V1" = "200" ]; then
            echo -e "   ${GREEN}✅ /v1/health endpoint works${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Health endpoint not available - this is OK, service is still working${NC}"
        fi
    else
        echo -e "   ${YELLOW}⚠️  Health endpoint returned: ${HTTP_CODE}${NC}"
        if [ -n "$RESPONSE" ]; then
            echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        fi
    fi
    echo ""
}

# Test models endpoint
test_models() {
    BASE_URL="${LLAMA_STACK_BASE_URL:-http://localhost:8321}"
    echo -e "${BLUE}2️⃣  Testing Models Endpoint${NC}"
    echo "   GET ${BASE_URL}/v1/models"
    RESPONSE=$(curl -s -k "${BASE_URL}/v1/models" 2>/dev/null || echo "")
    if [ -n "$RESPONSE" ]; then
        echo -e "   ${GREEN}✅ Response:${NC}"
        echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        
        # Extract model count
        MODEL_COUNT=$(echo "$RESPONSE" | jq '.data | length' 2>/dev/null || echo "0")
        if [ "$MODEL_COUNT" -gt 0 ]; then
            echo -e "   ${GREEN}✅ Found $MODEL_COUNT model(s)${NC}"
        fi
    else
        echo -e "   ${RED}❌ No response${NC}"
        return 1
    fi
    echo ""
}

# Test chat completion endpoint
test_chat_completion() {
    BASE_URL="${LLAMA_STACK_BASE_URL:-http://localhost:8321}"
    echo -e "${BLUE}3️⃣  Testing Chat Completion Endpoint${NC}"
    echo "   POST ${BASE_URL}/v1/chat/completions"
    
    # Get first available LLM model (not embedding)
    MODELS_JSON=$(curl -s -k "${BASE_URL}/v1/models" 2>/dev/null || echo "")
    MODEL=$(echo "$MODELS_JSON" | jq -r '.data[] | select(.model_type == "llm") | .identifier' 2>/dev/null | head -1 || echo "")
    
    if [ -z "$MODEL" ] || [ "$MODEL" = "null" ]; then
        # Fallback to first model if no LLM found
        MODEL=$(echo "$MODELS_JSON" | jq -r '.data[0].identifier' 2>/dev/null || echo "")
    fi
    
    if [ -z "$MODEL" ] || [ "$MODEL" = "null" ]; then
        echo -e "   ${YELLOW}⚠️  No models available, skipping chat completion test${NC}"
        echo ""
        return 0
    fi
    
    echo -e "   Using model: ${CYAN}$MODEL${NC}"
    
    PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "user",
      "content": "Say hello in one sentence"
    }
  ],
  "max_tokens": 50
}
EOF
)
    
    RESPONSE=$(curl -s -k -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" 2>/dev/null || echo "")
    
    if [ -n "$RESPONSE" ]; then
        echo -e "   ${GREEN}✅ Response:${NC}"
        echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        
        # Extract content
        CONTENT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content' 2>/dev/null || echo "")
        if [ -n "$CONTENT" ] && [ "$CONTENT" != "null" ]; then
            echo -e "   ${GREEN}✅ Generated text: ${CYAN}$CONTENT${NC}"
        fi
    else
        echo -e "   ${RED}❌ No response${NC}"
        return 1
    fi
    echo ""
}

# Test agents endpoint (if available)
test_agents() {
    BASE_URL="${LLAMA_STACK_BASE_URL:-http://localhost:8321}"
    echo -e "${BLUE}4️⃣  Testing Agents Endpoint${NC}"
    echo "   GET ${BASE_URL}/v1/agents"
    RESPONSE=$(curl -s -k "${BASE_URL}/v1/agents" 2>/dev/null || echo "")
    if [ -n "$RESPONSE" ]; then
        HTTP_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" "${BASE_URL}/v1/agents" 2>/dev/null || echo "000")
        if [ "$HTTP_CODE" = "200" ]; then
            echo -e "   ${GREEN}✅ Agents endpoint available${NC}"
            echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        elif [ "$HTTP_CODE" = "404" ]; then
            echo -e "   ${YELLOW}⚠️  Agents endpoint not available (404) - this is normal if agents API is not enabled${NC}"
        else
            echo -e "   ${YELLOW}⚠️  Unexpected status: ${HTTP_CODE}${NC}"
        fi
    else
        echo -e "   ${YELLOW}⚠️  No response${NC}"
    fi
    echo ""
}

# Test RAG/ingestion endpoint (if available)
test_ingestion() {
    BASE_URL="${LLAMA_STACK_BASE_URL:-http://localhost:8321}"
    echo -e "${BLUE}5️⃣  Testing Ingestion Endpoint${NC}"
    echo "   GET ${BASE_URL}/v1/ingest"
    HTTP_CODE=$(curl -s -k -o /dev/null -w "%{http_code}" "${BASE_URL}/v1/ingest" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "405" ]; then
        echo -e "   ${GREEN}✅ Ingestion endpoint available (status: $HTTP_CODE)${NC}"
    elif [ "$HTTP_CODE" = "404" ]; then
        echo -e "   ${YELLOW}⚠️  Ingestion endpoint not available (404) - this is normal if RAG is not configured${NC}"
    else
        echo -e "   ${YELLOW}⚠️  Unexpected status: $HTTP_CODE${NC}"
    fi
    echo ""
}

# Main test execution
main() {
    # Check infrastructure first
    check_pod_status
    check_service_status
    check_route_status
    
    # Check access method
    if ! check_access; then
        echo -e "${RED}❌ Cannot access Llama Stack. Please set up Route or port-forward.${NC}"
        exit 1
    fi
    
    BASE_URL="${LLAMA_STACK_BASE_URL:-http://localhost:8321}"
    echo -e "${BLUE}📡 Testing API Endpoints via: ${CYAN}${BASE_URL}${NC}"
    echo ""
    
    # Run tests
    test_health
    test_models
    test_chat_completion
    test_agents
    test_ingestion
    
    echo -e "${GREEN}✅ Testing complete!${NC}"
    echo ""
    
    # Summary
    echo -e "${BLUE}📊 Summary:${NC}"
    POD_STATUS=$(oc get pods -n "$NAMESPACE" -l app=llama-stack -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "")
    SERVICE_EXISTS=$(oc get svc "$SERVICE_NAME" -n "$NAMESPACE" &> /dev/null && echo "yes" || echo "no")
    ROUTE_HOST=$(oc get route llamastack-route -n "$NAMESPACE" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
    
    echo -e "   Pod: ${GREEN}${POD_STATUS}${NC}"
    echo -e "   Service: ${GREEN}${SERVICE_EXISTS}${NC}"
    if [ -n "$ROUTE_HOST" ]; then
        echo -e "   Route: ${GREEN}✅ Available${NC} (https://${ROUTE_HOST})"
    else
        echo -e "   Route: ${YELLOW}⚠️  Not created${NC}"
    fi
    echo ""
    
    echo -e "${BLUE}📝 Next Steps:${NC}"
    echo "1. Use Llama Stack SDK in your Jupyter notebooks:"
    echo "   from llama_stack_client import LlamaStackClient"
    if [[ "$BASE_URL" == https://* ]]; then
        echo "   client = LlamaStackClient(base_url='$BASE_URL')"
    else
        echo "   client = LlamaStackClient(base_url='$BASE_URL')"
    fi
    echo ""
    echo "2. Or use the service URL directly from within the cluster:"
    SERVICE_FQDN="${SERVICE_NAME}.${NAMESPACE}.svc.cluster.local:8321"
    echo "   http://${SERVICE_FQDN}"
    echo ""
    if [[ "$BASE_URL" == https://* ]]; then
        echo "3. External Route URL: $BASE_URL"
    fi
}

main

