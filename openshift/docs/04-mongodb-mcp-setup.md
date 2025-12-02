# MongoDB & MCP Server Setup

Deploy MongoDB database and MongoDB MCP server for agent integration.

## Overview

This guide deploys:
- **MongoDB** - Database with sample IT operations data
- **MongoDB MCP Server** - MCP interface for agent access

---

## Quick Start

### Using Deployment Script (Recommended)

```bash
cd openshift/scripts
./deploy-mongodb-mcp.sh
```

The script automatically:
- ✅ Creates MongoDB secret
- ✅ Deploys MongoDB with initialization
- ✅ Deploys MongoDB MCP server
- ✅ Creates routes
- ✅ Waits for readiness

---

## Step-by-Step Deployment

### Step 1: Create MongoDB Secret

```bash
oc create secret generic mongodb-secret \
  --from-literal=MONGO_USERNAME="admin" \
  --from-literal=MONGO_PASSWORD="password123" \
  --from-literal=MONGO_DATABASE="mcp_demo" \
  --from-literal=MONGO_CONNECTION_STRING="mongodb://admin:password123@mongodb:27017/mcp_demo?authSource=admin" \
  --namespace="my-first-model"
```

### Step 2: Create Init Script ConfigMap

```bash
oc apply -f manifests/mongodb/mongodb-init-configmap.yaml
```

This ConfigMap contains the initialization script that populates sample data.

### Step 3: Deploy MongoDB

```bash
oc apply -f manifests/mongodb/mongodb-deployment.yaml
```

**Wait for MongoDB to be ready:**
```bash
oc wait --for=condition=available deployment/mongodb -n my-first-model --timeout=300s
```

### Step 4: Deploy MongoDB MCP Server

```bash
oc apply -f manifests/mongodb/mongodb-mcp-server-deployment.yaml
```

**Wait for MCP server to be ready:**
```bash
oc wait --for=condition=available deployment/mongodb-mcp-server -n my-first-model --timeout=300s
```

### Step 5: Verify Deployment

```bash
# Check MongoDB
oc get pods -n my-first-model | grep mongodb

# Check MCP server
oc get pods -n my-first-model | grep mongodb-mcp-server

# Test MongoDB connection
oc exec -it deployment/mongodb -n my-first-model -- mongosh -u admin -p password123 --authenticationDatabase admin

# Test MCP server
oc logs deployment/mongodb-mcp-server -n my-first-model --tail=50
```

---

## MongoDB Initialization

The MongoDB deployment automatically runs an initialization script that creates:

### Databases
- `mcp_demo` - Main database for demonstrations

### Collections
- `incidents` - IT incident records
- `services` - IT service definitions
- `alerts` - Monitoring alerts

### Sample Data

The init script populates sample IT operations data for testing.

---

## MongoDB MCP Server

The MongoDB MCP server exposes MongoDB operations as MCP tools:

### Available Tools
- `list-databases` - List all databases
- `list-collections` - List collections in a database
- `count-documents` - Count documents in a collection
- `find-documents` - Query documents
- `insert-document` - Insert new document
- `update-document` - Update existing document

### Configuration

The MCP server is configured via environment variables:
- `MDB_MCP_CONNECTION_STRING` - MongoDB connection string
- `MDB_MCP_READ_ONLY` - Set to "true" for read-only mode
- `MDB_MCP_TRANSPORT` - Set to "http" for streamable HTTP

---

## Access Methods

### Inside Cluster (Service URL)

```bash
MCP_URL="http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000"
```

### Outside Cluster (Route URL)

```bash
MCP_URL=$(oc get route mongodb-mcp-server -n my-first-model -o jsonpath='{.spec.host}')
```

---

## Next Steps

After deploying MongoDB and MCP server:

1. **[Register MCP Server with LlamaStack](06-mcp-integration.md#registration)**
2. **[Create Agents with MCP Tools](07-agent-configuration.md)**

---

## Troubleshooting

### MongoDB Not Starting

```bash
# Check pod logs
oc logs deployment/mongodb -n my-first-model

# Check persistent volume
oc get pvc -n my-first-model | grep mongodb

# Check events
oc get events -n my-first-model --sort-by='.lastTimestamp' | grep mongodb
```

### MCP Server Connection Issues

```bash
# Check MCP server logs
oc logs deployment/mongodb-mcp-server -n my-first-model

# Test MongoDB connection from MCP server pod
oc exec deployment/mongodb-mcp-server -n my-first-model -- curl http://mongodb:27017
```

### Data Not Initialized

```bash
# Check init script execution
oc logs deployment/mongodb -n my-first-model | grep init

# Manually run init script
oc exec deployment/mongodb -n my-first-model -- mongosh -u admin -p password123 --authenticationDatabase admin < manifests/mongodb/init-mongo.js
```

---

**Need help?** → [Troubleshooting Guide](troubleshooting.md) | [Quick Reference](quick-reference.md)

