#!/bin/bash
#
# Deploy MongoDB and MongoDB MCP Server on OpenShift
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

echo -e "${BLUE}🚀 Deploying MongoDB and MongoDB MCP Server${NC}"
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

# Ensure namespace exists
echo -e "${BLUE}📦 Checking namespace...${NC}"
if ! oc get namespace "${NAMESPACE}" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Namespace ${NAMESPACE} does not exist. Creating...${NC}"
    oc create namespace "${NAMESPACE}"
fi
echo -e "${GREEN}✅ Namespace ${NAMESPACE} exists${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFESTS_DIR="${SCRIPT_DIR}/../manifests"

# Step 1: Create MongoDB secret and init script ConfigMap
echo -e "${BLUE}🔐 Step 1: Creating MongoDB secret and init script...${NC}"
oc apply -f "${MANIFESTS_DIR}/mongodb/mongodb-secret.yaml"
oc apply -f "${MANIFESTS_DIR}/mongodb/mongodb-init-configmap.yaml"
echo -e "${GREEN}✅ MongoDB secret and init script created${NC}"
echo ""

# Step 2: Deploy MongoDB
echo -e "${BLUE}📦 Step 2: Deploying MongoDB...${NC}"
oc apply -f "${MANIFESTS_DIR}/mongodb/mongodb-deployment.yaml"
echo -e "${GREEN}✅ MongoDB deployment created${NC}"
echo ""

# Wait for MongoDB to be ready
echo -e "${BLUE}⏳ Waiting for MongoDB to be ready...${NC}"
oc wait --for=condition=available deployment/mongodb -n "${NAMESPACE}" --timeout=300s || {
    echo -e "${YELLOW}⚠️  MongoDB not ready yet. Check status with:${NC}"
    echo "  oc get pods -n ${NAMESPACE} -l app=mongodb"
    echo "  oc logs -n ${NAMESPACE} -l app=mongodb"
}

echo -e "${GREEN}✅ MongoDB is ready${NC}"
echo ""

# Check if initialization script ran (look for init logs)
echo -e "${BLUE}📊 Checking database initialization...${NC}"
sleep 5  # Give MongoDB a moment to complete initialization
INIT_LOGS=$(oc logs "$MONGODB_POD" -n "$NAMESPACE" --tail=50 2>/dev/null | grep -i "initialization\|init\|sample data" || echo "")
if echo "$INIT_LOGS" | grep -q "Sample data initialization complete"; then
    echo -e "${GREEN}✅ Database initialized with sample data${NC}"
else
    echo -e "${YELLOW}⚠️  Initialization may still be in progress${NC}"
    echo "   Check logs: oc logs $MONGODB_POD -n $NAMESPACE | grep -i init"
fi
echo ""

# Step 3: Deploy MongoDB MCP Server
echo -e "${BLUE}📦 Step 3: Deploying MongoDB MCP Server...${NC}"
oc apply -f "${MANIFESTS_DIR}/mongodb/mongodb-mcp-server-deployment.yaml"
echo -e "${GREEN}✅ MongoDB MCP Server deployment created${NC}"
echo ""

# Wait for MCP server to be ready
echo -e "${BLUE}⏳ Waiting for MongoDB MCP Server to be ready...${NC}"
oc wait --for=condition=available deployment/mongodb-mcp-server -n "${NAMESPACE}" --timeout=300s || {
    echo -e "${YELLOW}⚠️  MCP Server not ready yet. Check status with:${NC}"
    echo "  oc get pods -n ${NAMESPACE} -l app=mongodb-mcp-server"
    echo "  oc logs -n ${NAMESPACE} -l app=mongodb-mcp-server"
}

echo -e "${GREEN}✅ MongoDB MCP Server is ready${NC}"
echo ""

# Show status
echo -e "${BLUE}📊 Deployment Status:${NC}"
echo ""
oc get pods -n "${NAMESPACE}" -l 'app in (mongodb,mongodb-mcp-server)'
echo ""
oc get svc -n "${NAMESPACE}" -l 'app in (mongodb,mongodb-mcp-server)'
echo ""

# Get MongoDB connection info
MONGO_SVC=$(oc get svc mongodb -n "${NAMESPACE}" -o jsonpath='{.metadata.name}' 2>/dev/null || echo "")
if [ -n "$MONGO_SVC" ]; then
    MONGO_HOST="${MONGO_SVC}.${NAMESPACE}.svc.cluster.local"
    echo -e "${BLUE}📝 MongoDB Connection Information:${NC}"
    echo "  Host: ${MONGO_HOST}"
    echo "  Port: 27017"
    echo "  Database: mcp_demo"
    echo "  Connection String: mongodb://admin:<password>@${MONGO_HOST}:27017/mcp_demo?authSource=admin"
    echo ""
    echo -e "${YELLOW}⚠️  Password is stored in mongodb-secret${NC}"
    echo "  Get password: oc get secret mongodb-secret -n ${NAMESPACE} -o jsonpath='{.data.MONGO_INITDB_ROOT_PASSWORD}' | base64 -d"
    echo ""
fi

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Verify MongoDB is accessible:"
echo "   oc exec -it deployment/mongodb -n ${NAMESPACE} -- mongosh -u admin -p"
echo ""
echo "2. Check MongoDB MCP Server logs:"
echo "   oc logs -n ${NAMESPACE} -l app=mongodb-mcp-server"
echo ""
echo "3. Configure LlamaStack to use the MongoDB MCP server"
echo "   (See notebook 04 for MCP integration examples)"
echo ""

