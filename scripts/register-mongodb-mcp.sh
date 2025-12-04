#!/bin/bash
#
# Register MongoDB MCP Server with LlamaStack
# This script registers the MongoDB MCP server as a toolgroup in LlamaStack
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="${NAMESPACE:-my-first-model}"
LLAMASTACK_ROUTE="${LLAMASTACK_ROUTE:-llamastack-route-my-first-model.apps.ocp.5pndc.sandbox5432.opentlc.com}"
MCP_SERVER_ROUTE="${MCP_SERVER_ROUTE:-mongodb-mcp-server-my-first-model.apps.ocp.5pndc.sandbox5432.opentlc.com}"
TOOLGROUP_ID="${TOOLGROUP_ID:-mcp::mongodb}"

echo -e "${BLUE}🔗 Registering MongoDB MCP Server with LlamaStack${NC}"
echo "=========================================="
echo ""

# Check if oc is installed
if ! command -v oc &> /dev/null; then
    echo -e "${RED}❌ OpenShift CLI (oc) is not installed${NC}"
    exit 1
fi

# Check if logged in to OpenShift
if ! oc whoami &> /dev/null; then
    echo -e "${RED}❌ Not logged in to OpenShift${NC}"
    echo "Please log in using: oc login --token=<token> --server=<openshift_cluster_url>"
    exit 1
fi

echo -e "${GREEN}✅ Logged in as: $(oc whoami)${NC}"
echo ""

# Get LlamaStack route if not provided
if [ -z "$LLAMASTACK_ROUTE" ] || [ "$LLAMASTACK_ROUTE" = "llamastack-route-my-first-model.apps.ocp.5pndc.sandbox5432.opentlc.com" ]; then
    echo -e "${BLUE}🔍 Discovering LlamaStack route...${NC}"
    
    # Try multiple methods to find the route
    # Method 1: Try by name (most reliable)
    LLAMASTACK_ROUTE=$(oc get route llamastack-route -n "${NAMESPACE}" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
    
    # Method 2: Try by label app=llama-stack (with hyphen)
    if [ -z "$LLAMASTACK_ROUTE" ]; then
        LLAMASTACK_ROUTE=$(oc get route -n "${NAMESPACE}" -l app=llama-stack -o jsonpath='{.items[0].spec.host}' 2>/dev/null || echo "")
    fi
    
    # Method 3: Try by label app=llamastack (without hyphen)
    if [ -z "$LLAMASTACK_ROUTE" ]; then
        LLAMASTACK_ROUTE=$(oc get route -n "${NAMESPACE}" -l app=llamastack -o jsonpath='{.items[0].spec.host}' 2>/dev/null || echo "")
    fi
    
    # Method 4: Try finding route that points to a llama-stack service
    if [ -z "$LLAMASTACK_ROUTE" ]; then
        # Get all routes and check which one points to a llama-stack service
        for route_name in $(oc get route -n "${NAMESPACE}" -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
            service_name=$(oc get route "$route_name" -n "${NAMESPACE}" -o jsonpath='{.spec.to.name}' 2>/dev/null || echo "")
            if echo "$service_name" | grep -qi "llama\|lsd"; then
                LLAMASTACK_ROUTE=$(oc get route "$route_name" -n "${NAMESPACE}" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
                if [ -n "$LLAMASTACK_ROUTE" ]; then
                    break
                fi
            fi
        done
    fi
    
    # Method 5: Try finding any route with "llama" in the name
    if [ -z "$LLAMASTACK_ROUTE" ]; then
        # Get all routes and filter for llama
        for route_name in $(oc get route -n "${NAMESPACE}" -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
            if echo "$route_name" | grep -qi "llama"; then
                LLAMASTACK_ROUTE=$(oc get route "$route_name" -n "${NAMESPACE}" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
                if [ -n "$LLAMASTACK_ROUTE" ]; then
                    break
                fi
            fi
        done
    fi
    
    # Method 5: List all routes and let user know
    if [ -z "$LLAMASTACK_ROUTE" ]; then
        echo -e "${YELLOW}⚠️  Could not automatically find LlamaStack route${NC}"
        echo ""
        echo -e "${CYAN}Available routes in namespace ${NAMESPACE}:${NC}"
        oc get route -n "${NAMESPACE}" -o custom-columns=NAME:.metadata.name,HOST:.spec.host 2>/dev/null || echo "   (Could not list routes)"
        echo ""
        echo -e "${YELLOW}Please set LLAMASTACK_ROUTE environment variable:${NC}"
        echo "   export LLAMASTACK_ROUTE=<route-hostname>"
        echo "   ./register-mongodb-mcp.sh"
        exit 1
    fi
fi

echo -e "${GREEN}✅ LlamaStack route: ${LLAMASTACK_ROUTE}${NC}"

# Get MCP server URL
# IMPORTANT: LlamaStack runs inside the cluster, so it MUST use the internal service URL
# The external route may not be accessible from within the cluster or may have TLS issues
# Service URL is more reliable and doesn't require external routing

# Check if user explicitly wants to use route (not recommended)
USE_SERVICE_URL="${USE_SERVICE_URL:-true}"

if [ "$USE_SERVICE_URL" != "false" ]; then
    # Use service URL (default and recommended)
    echo -e "${BLUE}🔍 Using internal service URL for MCP server${NC}"
    echo -e "${CYAN}   (LlamaStack runs in-cluster, so service URL is required)${NC}"
    
    # Verify service exists
    if oc get svc mongodb-mcp-server -n "${NAMESPACE}" &>/dev/null; then
        # Get the service port (default to 3000)
        MCP_PORT=$(oc get svc mongodb-mcp-server -n "${NAMESPACE}" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "3000")
        MCP_SERVER_URL="http://mongodb-mcp-server.${NAMESPACE}.svc.cluster.local:${MCP_PORT}"
        echo -e "${GREEN}✅ Using service URL: ${MCP_SERVER_URL}${NC}"
    else
        echo -e "${RED}❌ MongoDB MCP server service not found${NC}"
        echo "   Service name: mongodb-mcp-server"
        echo "   Namespace: ${NAMESPACE}"
        echo ""
        echo "   Please ensure the MongoDB MCP server is deployed:"
        echo "   ./scripts/deploy-mongodb-mcp.sh"
        exit 1
    fi
else
    # Use external route (only if explicitly requested, not recommended)
    echo -e "${YELLOW}⚠️  Using external route (not recommended for in-cluster LlamaStack)${NC}"
    if [ -z "$MCP_SERVER_ROUTE" ] || [ "$MCP_SERVER_ROUTE" = "mongodb-mcp-server-my-first-model.apps.ocp.5pndc.sandbox5432.opentlc.com" ]; then
        echo -e "${BLUE}🔍 Discovering MongoDB MCP server route...${NC}"
        MCP_SERVER_ROUTE=$(oc get route mongodb-mcp-server -n "${NAMESPACE}" -o jsonpath='{.spec.host}' 2>/dev/null || echo "")
        if [ -z "$MCP_SERVER_ROUTE" ]; then
            echo -e "${YELLOW}⚠️  Could not find MongoDB MCP server route${NC}"
            echo "   Falling back to service URL..."
            MCP_SERVER_URL="http://mongodb-mcp-server.${NAMESPACE}.svc.cluster.local:3000"
        else
            MCP_SERVER_URL="https://${MCP_SERVER_ROUTE}"
        fi
    else
        MCP_SERVER_URL="https://${MCP_SERVER_ROUTE}"
    fi
    echo -e "${GREEN}✅ MCP Server URL: ${MCP_SERVER_URL}${NC}"
fi

echo ""

# Check if MCP server is accessible
echo -e "${BLUE}🔍 Checking MCP server accessibility...${NC}"
if echo "$MCP_SERVER_URL" | grep -q "\.svc\.cluster\.local"; then
    # Service URL - can only be accessed from inside cluster
    echo -e "${CYAN}   Service URL detected - accessibility check skipped${NC}"
    echo -e "${CYAN}   (Service URLs are only accessible from inside the cluster)${NC}"
    echo -e "${CYAN}   LlamaStack will be able to access it from within the cluster${NC}"
else
    # Route URL - can be checked from outside
    if curl -s -f -k "${MCP_SERVER_URL}/health" > /dev/null 2>&1 || curl -s -f -k "${MCP_SERVER_URL}" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ MCP server is accessible${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not verify MCP server accessibility${NC}"
        echo "   Continuing anyway (may be accessible from within cluster)..."
    fi
fi
echo ""

# Build the MCP endpoint URL
# MongoDB MCP server uses streamable HTTP transport, endpoint is /mcp (not /sse)
MCP_ENDPOINT="${MCP_SERVER_URL}/mcp"

echo -e "${BLUE}📋 Registration Details:${NC}"
echo "   Toolgroup ID: ${TOOLGROUP_ID}"
echo "   MCP Endpoint: ${MCP_ENDPOINT}"
echo "   LlamaStack URL: https://${LLAMASTACK_ROUTE}"
echo ""

# Check if toolgroup already exists
echo -e "${BLUE}🔍 Checking if toolgroup already exists...${NC}"
EXISTING_TG=$(curl -s "https://${LLAMASTACK_ROUTE}/v1/toolgroups/${TOOLGROUP_ID}" 2>/dev/null || echo "")

if echo "$EXISTING_TG" | grep -q "${TOOLGROUP_ID}"; then
    EXISTING_ENDPOINT=$(echo "$EXISTING_TG" | jq -r '.mcp_endpoint.uri' 2>/dev/null || echo "")
    echo -e "${YELLOW}⚠️  Toolgroup already exists with endpoint: ${EXISTING_ENDPOINT}${NC}"
    
    if [ "$EXISTING_ENDPOINT" != "$MCP_ENDPOINT" ]; then
        echo -e "${YELLOW}⚠️  Endpoint differs from desired endpoint${NC}"
        echo -e "${YELLOW}   Current: ${EXISTING_ENDPOINT}${NC}"
        echo -e "${YELLOW}   Desired: ${MCP_ENDPOINT}${NC}"
        echo ""
        echo -e "${BLUE}📝 Deleting old registration and creating new one...${NC}"
        
        # Delete old registration
        DELETE_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X DELETE "https://${LLAMASTACK_ROUTE}/v1/toolgroups/${TOOLGROUP_ID}" 2>/dev/null || echo "")
        DELETE_CODE=$(echo "$DELETE_RESPONSE" | grep "HTTP_CODE:" | sed 's/HTTP_CODE://')
        
        if [ "$DELETE_CODE" = "200" ] || [ "$DELETE_CODE" = "204" ] || [ "$DELETE_CODE" = "404" ]; then
            echo -e "${GREEN}   ✅ Deleted old registration${NC}"
        else
            echo -e "${YELLOW}   ⚠️  Delete returned ${DELETE_CODE}, continuing anyway...${NC}"
        fi
        
        sleep 1  # Brief pause before recreating
        # Fall through to create new registration
    else
        echo -e "${GREEN}✅ Toolgroup already registered with correct endpoint${NC}"
        echo ""
        echo -e "${BLUE}💡 If you're still having issues, try restarting LlamaStack:${NC}"
        echo "   oc rollout restart deployment -n ${NAMESPACE} -l app=llama-stack"
        exit 0
    fi
fi

# Register the MCP server (if not already handled above)
if [ -z "$REGISTER_RESPONSE" ]; then
    echo -e "${BLUE}📝 Registering MongoDB MCP server...${NC}"
    
    REGISTER_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "https://${LLAMASTACK_ROUTE}/v1/toolgroups" \
      -H "Content-Type: application/json" \
      --data "{
        \"provider_id\": \"model-context-protocol\",
        \"toolgroup_id\": \"${TOOLGROUP_ID}\",
        \"mcp_endpoint\": {
          \"uri\": \"${MCP_ENDPOINT}\"
        }
      }" 2>/dev/null || echo "")
fi

# Extract HTTP code and response body
if [ -n "$REGISTER_RESPONSE" ]; then
    HTTP_CODE=$(echo "$REGISTER_RESPONSE" | grep "HTTP_CODE:" | sed 's/HTTP_CODE://')
    RESPONSE_BODY=$(echo "$REGISTER_RESPONSE" | grep -v "HTTP_CODE:")
else
    HTTP_CODE=""
    RESPONSE_BODY=""
fi

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo -e "${GREEN}✅ Successfully registered MongoDB MCP server${NC}"
    echo ""
    if [ -n "$RESPONSE_BODY" ]; then
        echo -e "${CYAN}Response:${NC}"
        echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
    fi
elif [ "$HTTP_CODE" = "409" ] || [ "$HTTP_CODE" = "400" ]; then
    # Toolgroup might already exist, try to delete and recreate
    echo -e "${YELLOW}⚠️  Registration returned ${HTTP_CODE}, attempting to delete and recreate...${NC}"
    curl -s -X DELETE "https://${LLAMASTACK_ROUTE}/v1/toolgroups/${TOOLGROUP_ID}" > /dev/null 2>&1 || true
    sleep 1
    
    # Try again
    REGISTER_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "https://${LLAMASTACK_ROUTE}/v1/toolgroups" \
      -H "Content-Type: application/json" \
      --data "{
        \"provider_id\": \"model-context-protocol\",
        \"toolgroup_id\": \"${TOOLGROUP_ID}\",
        \"mcp_endpoint\": {
          \"uri\": \"${MCP_ENDPOINT}\"
        }
      }" 2>/dev/null || echo "")
    
    HTTP_CODE=$(echo "$REGISTER_RESPONSE" | grep "HTTP_CODE:" | sed 's/HTTP_CODE://')
    RESPONSE_BODY=$(echo "$REGISTER_RESPONSE" | grep -v "HTTP_CODE:")
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
        echo -e "${GREEN}✅ Successfully registered MongoDB MCP server${NC}"
    else
        echo -e "${RED}❌ Failed to register MCP server${NC}"
        echo "   HTTP Status: ${HTTP_CODE}"
        echo "   Response: ${RESPONSE_BODY}"
        exit 1
    fi
elif [ -n "$HTTP_CODE" ]; then
    echo -e "${RED}❌ Failed to register MCP server${NC}"
    echo "   HTTP Status: ${HTTP_CODE}"
    echo "   Response: ${RESPONSE_BODY}"
    exit 1
fi

echo ""
echo -e "${BLUE}🔍 Verifying registration...${NC}"

# List toolgroups to verify
TOOLGROUPS=$(curl -s "https://${LLAMASTACK_ROUTE}/v1/toolgroups" 2>/dev/null || echo "")

if echo "$TOOLGROUPS" | grep -q "${TOOLGROUP_ID}"; then
    echo -e "${GREEN}✅ MongoDB MCP server is registered${NC}"
    echo ""
    echo -e "${CYAN}Available toolgroups:${NC}"
    echo "$TOOLGROUPS" | jq -r '.[] | "  - \(.identifier) (\(.provider_id))"' 2>/dev/null || echo "$TOOLGROUPS"
else
    echo -e "${YELLOW}⚠️  Could not verify registration in toolgroups list${NC}"
    echo "   Toolgroups response:"
    echo "$TOOLGROUPS" | jq '.' 2>/dev/null || echo "$TOOLGROUPS"
fi

echo ""
echo -e "${GREEN}✅ Registration complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Verify connectivity from LlamaStack pod:"
echo "   ./verify-mcp-connectivity.sh"
echo ""
echo "2. Verify tools are available:"
echo "   curl -s https://${LLAMASTACK_ROUTE}/v1/toolgroups/${TOOLGROUP_ID} | jq"
echo ""
echo "3. If you previously registered with the route URL, you may need to:"
echo "   - Delete the old registration (if possible)"
echo "   - Restart LlamaStack pods to clear cache:"
echo "     oc rollout restart deployment -n ${NAMESPACE} -l app=llama-stack"
echo ""
echo "4. Use the toolgroup in your agents:"
echo "   Add '${TOOLGROUP_ID}' to the toolgroups list when creating agents"
echo ""
echo "5. Test with a Python script or notebook:"
echo "   ./test-mongodb-mcp-python.py"

