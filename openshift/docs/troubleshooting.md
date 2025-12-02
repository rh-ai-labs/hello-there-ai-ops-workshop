# Troubleshooting Guide

Solutions to common issues when deploying and using LlamaStack on OpenShift.

## 🔍 Quick Diagnostics

### Check Cluster Status

```bash
# Cluster info
oc cluster-info
oc get nodes

# Check operators
oc get operators -n openshift-operators

# Check namespaces
oc get namespaces | grep my-first-model
```

### Check Deployments

```bash
# All deployments
oc get deployments -n my-first-model

# Pod status
oc get pods -n my-first-model

# Events
oc get events -n my-first-model --sort-by='.lastTimestamp' | tail -20
```

---

## 🚨 Common Issues

### LlamaStack Not Accessible

**Symptoms:**
- Route returns 503 or connection refused
- Cannot connect to LlamaStack API

**Solutions:**

1. **Check pods are running**:
   ```bash
   oc get pods -n my-first-model | grep llamastack
   ```

2. **Check pod logs**:
   ```bash
   oc logs -n my-first-model -l app=llamastack --tail=100
   ```

3. **Check LlamaStackDistribution status**:
   ```bash
   oc describe llamastackdistribution -n my-first-model
   ```

4. **Check route**:
   ```bash
   oc get route llamastack-route -n my-first-model -o yaml
   ```

5. **Test from inside cluster**:
   ```bash
   oc run test-pod --image=curlimages/curl --rm -it -- \
     curl http://llamastack-service.my-first-model.svc.cluster.local:8321/v1/models
   ```

---

### MongoDB MCP Registration Fails

**Symptoms:**
- Toolgroup registration returns 400/500 error
- Agent cannot use MongoDB tools

**Solutions:**

1. **Verify MCP server is running**:
   ```bash
   oc get pods -n my-first-model | grep mongodb-mcp-server
   oc logs deployment/mongodb-mcp-server -n my-first-model
   ```

2. **Check endpoint URL**:
   - Must use service URL (not route) when LlamaStack runs in-cluster
   - Endpoint must be `/mcp` (not `/sse`)

3. **Test MCP endpoint**:
   ```bash
   oc exec deployment/mongodb-mcp-server -n my-first-model -- \
     curl http://localhost:3000/mcp
   ```

4. **Verify toolgroup format**:
   ```bash
   # Correct format
   {
     "provider_id": "model-context-protocol",
     "toolgroup_id": "mcp::mongodb",
     "mcp_endpoint": {
       "uri": "http://mongodb-mcp-server.namespace.svc.cluster.local:3000/mcp"
     }
   }
   ```

---

### Agent Not Using Tools

**Symptoms:**
- Agent responds without using tools
- No tool calls in turn steps

**Solutions:**

1. **Check agent configuration**:
   ```python
   # Verify toolgroups includes MCP toolgroup
   print(agent_config["toolgroups"])  # Should include "mcp::mongodb"
   
   # Verify tool_choice
   print(agent_config["tool_choice"])  # Should be "auto" or "required"
   
   # Verify max_tokens
   print(agent_config["sampling_params"]["max_tokens"])  # Must be > 0
   ```

2. **Check toolgroup is registered**:
   ```bash
   curl -k "https://${LLAMA_STACK_URL}/v1/toolgroups/mcp::mongodb"
   ```

3. **Check instructions**:
   - Instructions should guide agent to use tools
   - Example: "Always use MongoDB MCP tools to query the database"

4. **Check turn steps**:
   ```python
   # Look for tool_call steps in turn data
   for step in turn_data.get("steps", []):
       if step.get("type") == "tool_call":
           print("Tool was called!")
   ```

---

### GPU Nodes Not Coming Up

**Symptoms:**
- MachineSet created but nodes not appearing
- Machines in "Provisioning" state

**Solutions:**

1. **Check Machine status**:
   ```bash
   oc get machines -n openshift-machine-api | grep gpu
   oc describe machine <machine-name> -n openshift-machine-api
   ```

2. **Check AWS EC2 instances**:
   ```bash
   aws ec2 describe-instances --filters "Name=instance-type,Values=g6.4xlarge"
   ```

3. **Check quotas**:
   ```bash
   # Check vCPU quota for g6.4xlarge (16 vCPUs per instance)
   aws service-quotas get-service-quota \
     --service-code ec2 \
     --quota-code L-34B43A08
   ```

4. **Check AMI ID**:
   ```bash
   # Verify AMI ID matches your region
   oc get machineset -n openshift-machine-api -o jsonpath='{.items[0].spec.template.spec.providerSpec.value.ami.id}'
   ```

5. **Check subnet/security groups**:
   ```bash
   oc describe machine <machine-name> -n openshift-machine-api | grep -A 10 "Provider Status"
   ```

---

### MongoDB Connection Issues

**Symptoms:**
- MCP server cannot connect to MongoDB
- Connection timeout errors

**Solutions:**

1. **Check MongoDB is running**:
   ```bash
   oc get pods -n my-first-model | grep mongodb
   oc logs deployment/mongodb -n my-first-model
   ```

2. **Test connection from MCP server**:
   ```bash
   oc exec deployment/mongodb-mcp-server -n my-first-model -- \
     curl http://mongodb:27017
   ```

3. **Check connection string**:
   ```bash
   oc get secret mongodb-secret -n my-first-model -o jsonpath='{.data.MONGO_CONNECTION_STRING}' | base64 -d
   ```

4. **Check network policies**:
   ```bash
   oc get networkpolicies -n my-first-model
   ```

---

### Tool Execution Errors

**Symptoms:**
- Tools are called but return errors
- MCP error messages in agent responses

**Solutions:**

1. **Check MCP server logs**:
   ```bash
   oc logs deployment/mongodb-mcp-server -n my-first-model --tail=100
   ```

2. **Check MongoDB logs**:
   ```bash
   oc logs deployment/mongodb -n my-first-model --tail=100
   ```

3. **Verify tool arguments**:
   ```python
   # Check tool call arguments in turn steps
   for step in turn_data.get("steps", []):
       if step.get("type") == "tool_call":
           print(step.get("tool_call", {}).get("arguments"))
   ```

4. **Test tool manually**:
   ```bash
   # Test MongoDB connection
   oc exec deployment/mongodb -n my-first-model -- \
     mongosh -u admin -p password123 --authenticationDatabase admin
   ```

---

## 🔧 Advanced Troubleshooting

### Enable Debug Logging

```bash
# LlamaStack
oc set env deployment/llamastack LOG_LEVEL=DEBUG -n my-first-model

# MongoDB MCP Server
oc set env deployment/mongodb-mcp-server LOG_LEVEL=DEBUG -n my-first-model
```

### Check Resource Usage

```bash
# Node resources
oc top nodes

# Pod resources
oc top pods -n my-first-model

# Describe node for details
oc describe node <node-name>
```

### Network Debugging

```bash
# Test service connectivity
oc run debug-pod --image=nicolaka/netshoot --rm -it -- \
  curl http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000

# Check DNS resolution
oc run debug-pod --image=nicolaka/netshoot --rm -it -- \
  nslookup mongodb-mcp-server.my-first-model.svc.cluster.local
```

---

## 📞 Getting More Help

### Collect Diagnostics

```bash
# Save cluster state
oc get all -n my-first-model -o yaml > cluster-state.yaml
oc get events -n my-first-model > events.log
oc logs -n my-first-model --all-containers=true > all-logs.log
```

### Useful Information to Collect

- Cluster version: `oc version`
- Node information: `oc get nodes -o wide`
- Operator status: `oc get operators -n openshift-operators`
- Resource usage: `oc top nodes` and `oc top pods -n my-first-model`

---

## 🎯 Issue-Specific Solutions

### "Shield not served by provider"

**Cause**: Safety shield not properly registered

**Solution**:
```bash
# List available shields
oc get shields -n my-first-model

# Check shield registration
curl -k "https://${LLAMA_STACK_URL}/v1/shields"
```

### "Toolgroup not found"

**Cause**: MCP server not registered

**Solution**:
```bash
# Re-register toolgroup
./scripts/register-mongodb-mcp.sh

# Verify registration
curl -k "https://${LLAMA_STACK_URL}/v1/toolgroups/mcp::mongodb"
```

### "Connection refused"

**Cause**: Service not accessible

**Solution**:
- Check pods are running
- Check service exists: `oc get svc -n my-first-model`
- Check route exists: `oc get route -n my-first-model`
- Verify network policies allow traffic

---

**Still stuck?** → Review [Getting Started Guide](01-getting-started.md) or check [Quick Reference](quick-reference.md)

