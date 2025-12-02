# Quick Reference

Quick reference card for common OpenShift deployment tasks.

## 🚀 Quick Commands

### Deploy Everything

```bash
# 1. Deploy LlamaStack
./scripts/deploy-llamastack.sh

# 2. Deploy MongoDB & MCP
./scripts/deploy-mongodb-mcp.sh

# 3. Register MCP
./scripts/register-mongodb-mcp.sh
```

### Get URLs

```bash
# LlamaStack URL
oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}'

# MongoDB MCP URL (service)
echo "http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000"

# MongoDB MCP URL (route)
oc get route mongodb-mcp-server -n my-first-model -o jsonpath='{.spec.host}'
```

### Check Status

```bash
# LlamaStack pods
oc get pods -n my-first-model | grep llamastack

# MongoDB pods
oc get pods -n my-first-model | grep mongodb

# GPU nodes
oc get nodes -l node-role.kubernetes.io/gpu=true

# MachineSets
oc get machineset -n openshift-machine-api | grep gpu
```

---

## 📋 Common Configurations

### Agent Configuration

```python
agent_config = {
    "model": "vllm-inference/llama-32-3b-instruct",
    "instructions": "You have access to MongoDB through MCP tools.",
    "toolgroups": ["mcp::mongodb"],
    "tool_choice": "auto",
    "sampling_params": {"max_tokens": 2000}
}
```

### Register MCP Toolgroup

```bash
curl -k -X POST "https://${LLAMA_STACK_URL}/v1/toolgroups" \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": "model-context-protocol",
    "toolgroup_id": "mcp::mongodb",
    "mcp_endpoint": {
      "uri": "http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000/mcp"
    }
  }'
```

### Create GPU Worker Nodes

```bash
./scripts/create-gpu-workers.sh
```

---

## 🔍 Troubleshooting Commands

### Check Logs

```bash
# LlamaStack logs
oc logs -n my-first-model -l app=llamastack --tail=100

# MongoDB logs
oc logs deployment/mongodb -n my-first-model --tail=100

# MCP server logs
oc logs deployment/mongodb-mcp-server -n my-first-model --tail=100
```

### Check Events

```bash
oc get events -n my-first-model --sort-by='.lastTimestamp' | tail -20
```

### Test Connectivity

```bash
# Test LlamaStack API
curl -k https://$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')/v1/models

# Test MongoDB MCP (from inside cluster)
oc run test-pod --image=curlimages/curl --rm -it -- \
  curl http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000/mcp
```

---

## 📊 Resource Queries

### Check Resources

```bash
# CPU/Memory usage
oc top nodes
oc top pods -n my-first-model

# GPU usage
oc describe node <gpu-node> | grep nvidia.com/gpu

# Storage
oc get pvc -n my-first-model
```

### Scale Resources

```bash
# Scale GPU nodes
oc scale machineset ocp-xf56d-worker-gpu-us-east-2a -n openshift-machine-api --replicas=2

# Scale deployments
oc scale deployment mongodb -n my-first-model --replicas=2
```

---

## 🔐 Secrets Management

### Create Secrets

```bash
# MongoDB secret
oc create secret generic mongodb-secret \
  --from-literal=MONGO_USERNAME="admin" \
  --from-literal=MONGO_PASSWORD="password123" \
  --namespace="my-first-model"

# Inference model secret
oc create secret generic llama-stack-inference-model-secret \
  --from-literal=INFERENCE_MODEL="llama-32-3b-instruct" \
  --from-literal=VLLM_URL="http://..." \
  --from-literal=VLLM_API_TOKEN="token" \
  --namespace="my-first-model"
```

### View Secrets

```bash
oc get secrets -n my-first-model
oc get secret mongodb-secret -n my-first-model -o yaml
```

---

## 🗑️ Cleanup Commands

### Delete Deployments

```bash
# Delete LlamaStackDistribution
oc delete llamastackdistribution -n my-first-model --all

# Delete MongoDB
oc delete deployment mongodb mongodb-mcp-server -n my-first-model

# Delete GPU nodes
oc delete machineset -n openshift-machine-api -l machine.openshift.io/cluster-api-machineset=*gpu*
```

### Delete Namespace

```bash
oc delete namespace my-first-model
```

---

## 📚 Documentation Links

- [Getting Started](01-getting-started.md)
- [LlamaStack Deployment](03-llamastack-deployment.md)
- [MongoDB & MCP Setup](04-mongodb-mcp-setup.md)
- [MCP Integration](06-mcp-integration.md)
- [Troubleshooting](troubleshooting.md)

---

**Need more?** → [Full Documentation Index](../README.md)

