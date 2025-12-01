# MongoDB and MongoDB MCP Server Deployment on OpenShift

This guide explains how to deploy MongoDB and the MongoDB MCP server on OpenShift for use with LlamaStack agents.

## Overview

The MongoDB MCP server provides agents with the ability to interact with MongoDB databases through the Model Context Protocol (MCP). This enables agents to:
- Query databases
- Insert documents
- Update records
- Perform database operations

## Prerequisites

- OpenShift cluster access
- `oc` CLI installed and configured
- Appropriate permissions to create deployments and services
- Storage class available for persistent volumes

## Quick Start

### Option 1: Using the Deployment Script (Recommended)

```bash
cd openshift/scripts
./deploy-mongodb-mcp.sh
```

### Option 2: Manual Deployment

1. **Create the MongoDB secret and init script:**

```bash
oc apply -f openshift/manifests/mongodb/mongodb-secret.yaml
oc apply -f openshift/manifests/mongodb/mongodb-init-configmap.yaml
```

2. **Deploy MongoDB:**

```bash
oc apply -f openshift/manifests/mongodb/mongodb-deployment.yaml
```

**Note:** The MongoDB container will automatically run the initialization script on first startup, populating the database with sample IT operations data (incidents, services, alerts).

3. **Deploy MongoDB MCP Server:**

```bash
oc apply -f openshift/manifests/mongodb/mongodb-mcp-server-deployment.yaml
```

4. **Wait for deployments to be ready:**

```bash
oc wait --for=condition=available deployment/mongodb -n my-first-model --timeout=300s
oc wait --for=condition=available deployment/mongodb-mcp-server -n my-first-model --timeout=300s
```

5. **Wait for deployments to be ready:**

```bash
oc wait --for=condition=available deployment/mongodb -n my-first-model --timeout=300s
oc wait --for=condition=available deployment/mongodb-mcp-server -n my-first-model --timeout=300s
```

6. **Register MongoDB MCP Server with LlamaStack:**

```bash
cd openshift/scripts
./register-mongodb-mcp.sh
```

This script will:
- Discover the LlamaStack route
- Discover the MongoDB MCP server route
- Register the MCP server as a toolgroup (`mcp::mongodb`) with LlamaStack

7. **Verify sample data was created:**

```bash
# Check MongoDB logs for initialization confirmation
oc logs -n my-first-model -l app=mongodb | grep -i "initialization\|sample data"

# Or connect and query
oc exec -it deployment/mongodb -n my-first-model -- mongosh -u admin -p --authenticationDatabase admin --eval "use mcp_demo; db.incidents.countDocuments()"
```

## Sample Data

The MongoDB deployment includes an **initialization script** that automatically populates the database with sample IT operations data when the container starts for the first time. This means:

- ✅ **No manual population needed** - Data is created automatically
- ✅ **Sample data ready** - Incidents, services, and alerts are pre-populated
- ✅ **Perfect for demos** - Ready to use with MongoDB MCP server immediately
- ✅ **Runs only once** - Script only executes on first initialization (when database is empty)

### Sample Data Collections

The initialization script creates three collections:

1. **incidents** - IT incident records (5 sample incidents)
   - Open and resolved incidents
   - Different priority levels (critical, high, medium)
   - Affected services tracking

2. **services** - Service status and metrics (5 sample services)
   - Service health status
   - CPU and memory usage
   - Service dependencies

3. **alerts** - System alerts and notifications (5 sample alerts)
   - Different severity levels
   - Open and resolved alerts
   - Metric tracking

### Re-populating Data

If you need to re-populate the data (e.g., after clearing the database), delete the PVC and redeploy:

```bash
# Delete PVC (this deletes all data)
oc delete pvc mongodb-pvc -n my-first-model

# Delete and recreate the deployment
oc delete deployment mongodb -n my-first-model
oc apply -f openshift/manifests/mongodb/mongodb-deployment.yaml

# The init script will run automatically on first startup
```

## Configuration

### MongoDB Secret

The secret contains:
- `MONGO_INITDB_ROOT_USERNAME`: MongoDB admin username (default: `admin`)
- `MONGO_INITDB_ROOT_PASSWORD`: MongoDB admin password (default: `changeme123`)
- `MONGO_CONNECTION_STRING`: Full connection string for the MCP server

**⚠️ Security Note:** Change the default password in production!

To update the password:

```bash
oc create secret generic mongodb-secret \
  --from-literal=MONGO_INITDB_ROOT_USERNAME='admin' \
  --from-literal=MONGO_INITDB_ROOT_PASSWORD='<your-secure-password>' \
  --from-literal=MONGO_CONNECTION_STRING='mongodb://admin:<your-secure-password>@mongodb:27017/mcp_demo?authSource=admin' \
  --namespace='my-first-model' \
  --dry-run=client -o yaml | oc apply -f -

# Restart deployments to pick up new secret
oc rollout restart deployment/mongodb -n my-first-model
oc rollout restart deployment/mongodb-mcp-server -n my-first-model
```

### Storage

The MongoDB deployment uses a PersistentVolumeClaim (PVC) for data persistence. The default storage class is `gp3-csi`. To use a different storage class:

```bash
# Edit mongodb-deployment.yaml and change storageClassName
# Or patch the PVC:
oc patch pvc mongodb-pvc -n my-first-model -p '{"spec":{"storageClassName":"<your-storage-class>"}}'
```

## Verification

### Check Pod Status

```bash
oc get pods -n my-first-model -l 'app in (mongodb,mongodb-mcp-server)'
```

Expected output:
```
NAME                                  READY   STATUS    RESTARTS   AGE
mongodb-xxxxxxxxxx-xxxxx              1/1     Running   0          2m
mongodb-mcp-server-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
```

### Test MongoDB Connection

```bash
# Get MongoDB pod name
MONGODB_POD=$(oc get pods -n my-first-model -l app=mongodb -o jsonpath='{.items[0].metadata.name}')

# Connect to MongoDB
oc exec -it $MONGODB_POD -n my-first-model -- mongosh -u admin -p

# Or use the connection string from the secret
oc exec -it $MONGODB_POD -n my-first-model -- mongosh "mongodb://admin:changeme123@localhost:27017/mcp_demo?authSource=admin"
```

### Check MongoDB MCP Server Logs

```bash
oc logs -n my-first-model -l app=mongodb-mcp-server --tail=50
```

## Connecting to LlamaStack

The MongoDB MCP server is configured to use **HTTP transport** and must be registered with LlamaStack as a toolgroup.

### Automatic Registration (Recommended)

Use the registration script:

```bash
cd openshift/scripts
./register-mongodb-mcp.sh
```

This script will:
1. Discover the LlamaStack route
2. Discover the MongoDB MCP server route
3. Register the MCP server as toolgroup `mcp::mongodb` with LlamaStack
4. Verify the registration

### Manual Registration

You can also register manually using curl:

```bash
# Get routes
LLAMASTACK_ROUTE=$(oc get route -n my-first-model -l app=llamastack -o jsonpath='{.items[0].spec.host}')
MCP_ROUTE=$(oc get route mongodb-mcp-server -n my-first-model -o jsonpath='{.spec.host}')

# Register the MCP server
curl -X POST "https://${LLAMASTACK_ROUTE}/v1/toolgroups" \
  -H "Content-Type: application/json" \
  --data "{
    \"provider_id\": \"model-context-protocol\",
    \"toolgroup_id\": \"mcp::mongodb\",
    \"mcp_endpoint\": {
      \"uri\": \"https://${MCP_ROUTE}/sse\"
    }
  }"
```

### Verify Registration

Check that the toolgroup is registered:

```bash
LLAMASTACK_ROUTE=$(oc get route -n my-first-model -l app=llamastack -o jsonpath='{.items[0].spec.host}')
curl -s "https://${LLAMASTACK_ROUTE}/v1/toolgroups" | jq '.[] | select(.identifier == "mcp::mongodb")'
```

### Using the MongoDB MCP Server in Agents

Once registered, add `mcp::mongodb` to the toolgroups list when creating agents:

```python
from llama_stack_client import LlamaStackClient
from llama_stack_client.types.agent_create_params import AgentConfig

client = LlamaStackClient(base_url="https://your-llamastack-route")

agent_config = AgentConfig(
    model="vllm-inference/llama-32-3b-instruct",
    instructions="You are a helpful assistant with access to MongoDB.",
    toolgroups=["mcp::mongodb", "builtin::websearch"],
    tool_choice="auto"
)
```

## Usage Examples

### Using MongoDB MCP Server with Agents

Once configured, agents can use MongoDB tools through the MCP server. Example queries:

```python
# In a notebook or script
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url="https://your-llamastack-route")

# The agent can now use MongoDB tools via MCP
# Example: "Query the users collection in MongoDB"
# The agent will use the MCP MongoDB tools to execute the query
```

## Troubleshooting

### MongoDB Pod Not Starting

```bash
# Check pod events
oc describe pod -l app=mongodb -n my-first-model

# Check logs
oc logs -n my-first-model -l app=mongodb --tail=100

# Check PVC status
oc get pvc mongodb-pvc -n my-first-model
```

### MongoDB MCP Server Connection Issues

```bash
# Check if MongoDB service is accessible
oc exec -it deployment/mongodb-mcp-server -n my-first-model -- \
  sh -c "nc -zv mongodb.my-first-model.svc.cluster.local 27017"

# Check MCP server logs
oc logs -n my-first-model -l app=mongodb-mcp-server --tail=100

# Verify connection string in secret
oc get secret mongodb-secret -n my-first-model -o jsonpath='{.data.MONGO_CONNECTION_STRING}' | base64 -d
```

### Storage Issues

```bash
# Check available storage classes
oc get storageclass

# Check PVC status
oc get pvc -n my-first-model

# If PVC is pending, check events
oc describe pvc mongodb-pvc -n my-first-model
```

## Security Considerations

1. **Change Default Password:** Always change the default MongoDB password in production
2. **Network Policies:** Consider adding network policies to restrict access
3. **RBAC:** Use appropriate service accounts with minimal permissions
4. **Encryption:** Enable TLS for MongoDB connections in production
5. **Backup:** Set up regular backups of the MongoDB data

## Cleanup

To remove the deployment:

```bash
# Delete deployments and services
oc delete deployment mongodb mongodb-mcp-server -n my-first-model
oc delete svc mongodb mongodb-mcp-server -n my-first-model

# Delete PVC (this will delete data!)
oc delete pvc mongodb-pvc -n my-first-model

# Delete secret
oc delete secret mongodb-secret -n my-first-model
```

## References

- [MongoDB MCP Server](https://quay.io/repository/mcp-servers/mongodb-mcp-server)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

