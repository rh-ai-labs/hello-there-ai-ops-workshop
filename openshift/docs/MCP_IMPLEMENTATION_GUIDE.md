# MCP (Model Context Protocol) Implementation Guide

Complete guide for implementing MCP server integration with LlamaStack, based on our MongoDB MCP implementation.

## Overview

MCP (Model Context Protocol) allows LLMs to interact with external systems through a standardized protocol. This guide documents the complete implementation process.

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  LlamaStack │────────▶│  MCP Server  │────────▶│  MongoDB    │
│   (Agent)   │  MCP    │  (Toolgroup) │  HTTP   │  (Database) │
└─────────────┘         └──────────────┘         └─────────────┘
```

## Implementation Steps

### Step 1: Deploy MCP Server

The MCP server is a separate service that exposes tools/resources/prompts via MCP protocol.

**For MongoDB MCP Server:**

```bash
# Deploy MongoDB (data source)
oc apply -f openshift/manifests/mongodb/mongodb-deployment.yaml

# Deploy MongoDB MCP Server (MCP interface)
oc apply -f openshift/manifests/mongodb/mongodb-mcp-server-deployment.yaml
```

**Key Configuration:**
- MCP server uses **streamable HTTP transport**
- Endpoint: `/mcp` (NOT `/sse`)
- Service URL: `http://mongodb-mcp-server.<namespace>.svc.cluster.local:3000`
- Must be accessible from LlamaStack pods

### Step 2: Register MCP Server with LlamaStack

LlamaStack needs to know about the MCP server. Registration creates a "toolgroup" that agents can use.

**Registration Process:**

```bash
# Get routes
LLAMASTACK_ROUTE=$(oc get route -n my-first-model -l app=llama-stack -o jsonpath='{.items[0].spec.host}')
MCP_SERVICE_URL="http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000"

# Register as toolgroup
curl -X POST "https://${LLAMASTACK_ROUTE}/v1/toolgroups" \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": "model-context-protocol",
    "toolgroup_id": "mcp::mongodb",
    "mcp_endpoint": {
      "uri": "http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000/mcp"
    }
  }'
```

**Critical Points:**
- ✅ Use **service URL** (not route) - LlamaStack runs in-cluster
- ✅ Endpoint must be `/mcp` for streamable HTTP transport
- ✅ Toolgroup ID format: `mcp::<name>`
- ✅ Provider ID: `model-context-protocol`

**Or use the registration script:**
```bash
cd openshift/scripts
./register-mongodb-mcp.sh
```

### Step 3: Verify Registration

```bash
# Check toolgroup is registered
curl -s "https://${LLAMASTACK_ROUTE}/v1/toolgroups" | \
  jq '.data[] | select(.identifier == "mcp::mongodb")'

# Verify endpoint
curl -s "https://${LLAMASTACK_ROUTE}/v1/toolgroups/mcp::mongodb" | \
  jq '.mcp_endpoint'
```

### Step 4: Create Agent with MCP Tools

Agents must explicitly include the toolgroup to use MCP tools.

**Via API:**

```bash
curl -X POST "https://${LLAMASTACK_ROUTE}/v1/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_config": {
      "model": "vllm-inference/llama-32-3b-instruct",
      "instructions": "You have access to MongoDB through MCP tools.",
      "toolgroups": ["mcp::mongodb"],
      "tool_choice": "auto",
      "sampling_params": {
        "max_tokens": 2000
      }
    }
  }'
```

**Via Python Client:**

```python
from llama_stack_client import LlamaStackClient
from llama_stack_client.types.agent_create_params import AgentConfig

client = LlamaStackClient(base_url="https://your-llamastack-route")

agent_config = AgentConfig(
    model="vllm-inference/llama-32-3b-instruct",
    instructions="You have access to MongoDB through MCP tools.",
    toolgroups=["mcp::mongodb"],
    tool_choice="auto"
)

agent = client.alpha.agents.create(agent_config=agent_config)
```

### Step 5: Use Agent with MCP Tools

Agents use sessions and turns to interact. The agent will automatically call MCP tools when needed.

**Create Session:**

```bash
SESSION_RESPONSE=$(curl -s -X POST \
  "https://${LLAMASTACK_ROUTE}/v1/agents/${AGENT_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"session_name": "test-session"}')

SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
```

**Create Turn (with streaming):**

```bash
curl -N -X POST \
  "https://${LLAMASTACK_ROUTE}/v1/agents/${AGENT_ID}/session/${SESSION_ID}/turn" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "messages": [{"role": "user", "content": "What databases are in MongoDB?"}],
    "stream": true
  }'
```

**The agent will:**
1. Receive the query
2. Decide to use MongoDB MCP tools
3. Call `list-databases` tool
4. Receive results from MongoDB
5. Generate response based on real data

## Key Learnings

### 1. Transport Protocol

**MongoDB MCP Server uses:**
- Transport: `streamable-http` (NOT SSE)
- Endpoint: `/mcp` (NOT `/sse`)
- Protocol: JSON-RPC 2.0 over HTTP

**Why `/mcp` not `/sse`:**
- Streamable HTTP is a different protocol than SSE
- `/sse` is for Server-Sent Events transport
- `/mcp` is for streamable HTTP transport
- MongoDB MCP server uses streamable HTTP

### 2. Endpoint URL

**For LlamaStack registration:**
- ✅ Use **service URL**: `http://mongodb-mcp-server.<namespace>.svc.cluster.local:3000/mcp`
- ❌ Don't use route URL (TLS/certificate issues)
- ✅ LlamaStack runs in-cluster, so service URL works best

### 3. Toolgroup Registration

**Required fields:**
```json
{
  "provider_id": "model-context-protocol",
  "toolgroup_id": "mcp::<name>",
  "mcp_endpoint": {
    "uri": "http://<service-url>:<port>/mcp"
  }
}
```

**Toolgroup ID format:**
- Format: `mcp::<name>`
- Examples: `mcp::mongodb`, `mcp::filesystem`, `mcp::github`

### 4. Agent Configuration

**Required in agent_config:**
- `toolgroups`: Array containing toolgroup IDs (e.g., `["mcp::mongodb"]`)
- `tool_choice`: `"auto"` (let agent decide) or `"required"` (force tool use)
- `sampling_params.max_tokens`: Must be > 0 (default 0 causes errors)

### 5. Agent Interaction Flow

```
User Query
    ↓
Agent receives query
    ↓
Agent decides to use tool
    ↓
Agent calls MCP tool (e.g., list-databases)
    ↓
LlamaStack forwards to MCP server
    ↓
MCP server executes tool (queries MongoDB)
    ↓
MCP server returns results
    ↓
Agent receives tool results
    ↓
Agent generates response using real data
```

## Testing

### Test 1: Verify MCP Server is Running

```bash
oc get pods -n my-first-model -l app=mongodb-mcp-server
oc logs -n my-first-model -l app=mongodb-mcp-server --tail=50
```

### Test 2: Verify Toolgroup Registration

```bash
./openshift/scripts/test-mongodb-mcp-simple.sh
```

### Test 3: Test Agent Querying Database

```bash
python3 openshift/scripts/test-mongodb-agent-live.py
```

## Common Issues and Solutions

### Issue 1: "Toolgroup not found"

**Symptoms:**
- Agent creation succeeds
- But agent can't use tools
- Error: "Toolgroup mcp::mongodb not found"

**Solutions:**
1. Verify toolgroup is registered: `curl .../v1/toolgroups | jq '.data[] | select(.identifier == "mcp::mongodb")'`
2. Check endpoint URL is correct (`/mcp` not `/sse`)
3. Restart LlamaStack: `oc rollout restart deployment -n my-first-model -l app=llama-stack`
4. Wait for pods to be ready before testing

### Issue 2: "Failed to connect via STREAMABLE_HTTP"

**Symptoms:**
- Toolgroup registered but tools don't work
- Logs show: "failed to connect via STREAMABLE_HTTP, falling back to SSE"

**Solutions:**
1. Verify endpoint is `/mcp` (not `/sse`)
2. Check MCP server is using streamable HTTP transport
3. Verify service URL is correct (use service, not route)

### Issue 3: "max_tokens must be at least 1"

**Symptoms:**
- Agent creation fails or queries fail
- Error: "max_tokens must be at least 1, got 0"

**Solutions:**
- Add `sampling_params.max_tokens` to agent config:
  ```json
  "sampling_params": {
    "max_tokens": 2000
  }
  ```

### Issue 4: Tool calls work but no results

**Symptoms:**
- Agent calls tools successfully
- But turn details don't show results

**Solutions:**
1. Wait longer for turn to complete (tools may take time)
2. Check MCP server logs for errors
3. Verify MongoDB is accessible from MCP server
4. Check tool arguments are correct format

## Files Created

### Deployment Scripts
- `openshift/scripts/deploy-mongodb-mcp.sh` - Deploys MongoDB and MCP server
- `openshift/scripts/register-mongodb-mcp.sh` - Registers MCP server with LlamaStack

### Testing Scripts
- `openshift/scripts/test-mongodb-mcp-simple.sh` - Validates registration
- `openshift/scripts/verify-mongodb-mcp-from-pod.sh` - Tests connectivity
- `openshift/scripts/test-mongodb-agent-live.py` - Shows agent querying MongoDB

### Documentation
- `openshift/docs/MONGODB_MCP_DEPLOYMENT.md` - Deployment guide
- `openshift/docs/MCP_IMPLEMENTATION_GUIDE.md` - This guide

## Summary Checklist

To implement MCP integration:

- [ ] **Deploy MCP Server**
  - [ ] Deploy the service/data source (e.g., MongoDB)
  - [ ] Deploy MCP server that exposes tools
  - [ ] Verify MCP server is running and accessible

- [ ] **Register MCP Server**
  - [ ] Get LlamaStack route
  - [ ] Get MCP server service URL
  - [ ] Register toolgroup with correct endpoint (`/mcp` for streamable HTTP)
  - [ ] Verify registration

- [ ] **Create Agent**
  - [ ] Include toolgroup in `toolgroups` array
  - [ ] Set `tool_choice` to `"auto"` or `"required"`
  - [ ] Set `sampling_params.max_tokens` > 0
  - [ ] Verify agent created successfully

- [ ] **Test Integration**
  - [ ] Create session
  - [ ] Create turn with query
  - [ ] Verify agent calls MCP tools
  - [ ] Verify tool results are returned
  - [ ] Verify agent generates response using real data

## Next Steps

Once MCP is working:
1. Refactor Notebook 04 to demonstrate MCP integration
2. Add examples of different MCP tools
3. Show tool execution flow
4. Demonstrate real-world use cases

