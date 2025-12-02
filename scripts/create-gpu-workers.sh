#!/bin/bash
# Create GPU worker nodes (g6.4xlarge) for OpenShift cluster
# This script creates 2x g6.4xlarge worker nodes across 2 availability zones

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Creating GPU Worker Nodes (g6.4xlarge)${NC}"
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

# Get cluster information
echo -e "${BLUE}📋 Detecting cluster configuration...${NC}"
CLUSTER_NAME=$(oc get machineset -n openshift-machine-api -o jsonpath='{.items[0].metadata.labels.machine\.openshift\.io/cluster-api-cluster}' 2>/dev/null || echo "")
REGION=$(oc get infrastructure cluster -o jsonpath='{.status.platformStatus.aws.region}' 2>/dev/null || echo "us-east-2")
AMI_ID=$(oc get machineset -n openshift-machine-api -o jsonpath='{.items[0].spec.template.spec.providerSpec.value.ami.id}' 2>/dev/null || echo "")

if [ -z "$CLUSTER_NAME" ]; then
    echo -e "${RED}❌ Could not detect cluster name${NC}"
    echo "   Please ensure you have access to openshift-machine-api namespace"
    exit 1
fi

if [ -z "$AMI_ID" ]; then
    echo -e "${YELLOW}⚠️  Could not detect AMI ID${NC}"
    echo "   You may need to update the MachineSet manifest with the correct AMI ID"
fi

echo -e "${GREEN}✅ Cluster: ${CLUSTER_NAME}${NC}"
echo -e "${GREEN}✅ Region: ${REGION}${NC}"
if [ -n "$AMI_ID" ]; then
    echo -e "${GREEN}✅ AMI ID: ${AMI_ID}${NC}"
fi
echo ""

# Get availability zones
echo -e "${BLUE}📋 Detecting availability zones...${NC}"
AZS=$(oc get machineset -n openshift-machine-api -o jsonpath='{range .items[*]}{.spec.template.spec.providerSpec.value.placement.availabilityZone}{"\n"}{end}' | sort -u)
AZ_COUNT=$(echo "$AZS" | wc -l | tr -d ' ')
echo -e "${GREEN}✅ Found ${AZ_COUNT} availability zone(s)${NC}"

# Select first 2 AZs for GPU nodes
AZ_ARRAY=($(echo "$AZS" | head -2))
if [ ${#AZ_ARRAY[@]} -lt 2 ]; then
    echo -e "${YELLOW}⚠️  Only ${#AZ_ARRAY[@]} availability zone(s) available${NC}"
    echo "   Creating MachineSet for available zone(s) only"
fi

echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST_FILE="${SCRIPT_DIR}/../openshift/manifests/infrastructure/gpu-worker-machineset.yaml"

# Check if manifest exists
if [ ! -f "$MANIFEST_FILE" ]; then
    echo -e "${RED}❌ Manifest file not found: ${MANIFEST_FILE}${NC}"
    exit 1
fi

# Update manifest with detected values
echo -e "${BLUE}📝 Updating manifest with cluster-specific values...${NC}"

# Create temporary manifest with updated values
TEMP_MANIFEST=$(mktemp)
cp "$MANIFEST_FILE" "$TEMP_MANIFEST"

# Update cluster name in manifest
sed -i.bak "s/ocp-xf56d/${CLUSTER_NAME}/g" "$TEMP_MANIFEST"
rm -f "${TEMP_MANIFEST}.bak"

# Update AMI ID if detected
if [ -n "$AMI_ID" ]; then
    sed -i.bak "s/id: ami-082a55a580d5538ed/id: ${AMI_ID}/g" "$TEMP_MANIFEST"
    rm -f "${TEMP_MANIFEST}.bak"
fi

# Update region if different
if [ "$REGION" != "us-east-2" ]; then
    sed -i.bak "s/region: us-east-2/region: ${REGION}/g" "$TEMP_MANIFEST"
    sed -i.bak "s/us-east-2a/${AZ_ARRAY[0]}/g" "$TEMP_MANIFEST"
    if [ ${#AZ_ARRAY[@]} -ge 2 ]; then
        sed -i.bak "s/us-east-2b/${AZ_ARRAY[1]}/g" "$TEMP_MANIFEST"
    fi
    rm -f "${TEMP_MANIFEST}.bak"
fi

# Update subnet names
for i in "${!AZ_ARRAY[@]}"; do
    AZ="${AZ_ARRAY[$i]}"
    SUBNET_PATTERN="${CLUSTER_NAME}-subnet-private-${AZ}"
    if [ $i -eq 0 ]; then
        sed -i.bak "s/ocp-xf56d-subnet-private-us-east-2a/${SUBNET_PATTERN}/g" "$TEMP_MANIFEST"
    elif [ $i -eq 1 ]; then
        sed -i.bak "s/ocp-xf56d-subnet-private-us-east-2b/${SUBNET_PATTERN}/g" "$TEMP_MANIFEST"
    fi
done
rm -f "${TEMP_MANIFEST}.bak" 2>/dev/null || true

echo -e "${GREEN}✅ Manifest updated${NC}"
echo ""

# Apply MachineSets
echo -e "${BLUE}🚀 Creating GPU worker MachineSets...${NC}"
oc apply -f "$TEMP_MANIFEST"

# Clean up temp file
rm -f "$TEMP_MANIFEST"

echo ""
echo -e "${GREEN}✅ GPU worker MachineSets created!${NC}"
echo ""
echo -e "${BLUE}📊 Monitoring node creation...${NC}"
echo "   This may take 5-10 minutes..."
echo ""

# Wait for machines to be created
TIMEOUT=600  # 10 minutes
ELAPSED=0
INTERVAL=10

while [ $ELAPSED -lt $TIMEOUT ]; do
    READY_COUNT=$(oc get machineset -n openshift-machine-api -l machine.openshift.io/cluster-api-cluster=${CLUSTER_NAME} -o jsonpath='{range .items[?(@.metadata.name=~".*gpu.*")]}{.status.readyReplicas}{"\n"}{end}' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
    DESIRED_COUNT=$(oc get machineset -n openshift-machine-api -l machine.openshift.io/cluster-api-cluster=${CLUSTER_NAME} -o jsonpath='{range .items[?(@.metadata.name=~".*gpu.*")]}{.spec.replicas}{"\n"}{end}' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
    
    if [ "$READY_COUNT" -eq "$DESIRED_COUNT" ] && [ "$DESIRED_COUNT" -gt 0 ]; then
        echo ""
        echo -e "${GREEN}✅ All GPU nodes are ready!${NC}"
        echo ""
        echo -e "${BLUE}📋 GPU Worker Nodes:${NC}"
        oc get nodes -l node-role.kubernetes.io/gpu=true
        echo ""
        echo -e "${GREEN}✅ Setup complete!${NC}"
        exit 0
    fi
    
    echo -e "   ⏳ Progress: ${READY_COUNT}/${DESIRED_COUNT} nodes ready (${ELAPSED}s elapsed)..."
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
done

echo ""
echo -e "${YELLOW}⚠️  Timeout waiting for nodes to be ready${NC}"
echo "   Check status with: oc get machineset -n openshift-machine-api"
echo "   Check nodes with: oc get nodes -l node-role.kubernetes.io/gpu=true"
echo ""

