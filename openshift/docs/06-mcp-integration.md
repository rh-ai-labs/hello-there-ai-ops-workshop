# MCP Integration Guide

Complete guide for integrating MCP (Model Context Protocol) servers with LlamaStack agents.

## Overview

MCP allows LLMs to interact with external systems through a standardized protocol. This guide covers the complete integration process.

---

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  LlamaStack │────────▶│  MCP Server  │────────▶│  MongoDB    │
│   (Agent)   │  MCP    │  (Toolgroup) │  HTTP   │  (Database) │
└─────────────┘         └──────────────┘         └─────────────┘
```

**Flow:**
1. Agent decides to use a tool
2. LlamaStack forwards request to MCP server
3. MCP server executes operation (e.g., MongoDB query)
4. Results returned to agent
5. Agent uses results in response

---

## Prerequisites

- LlamaStack deployed and running
- MCP server deployed (e.g., MongoDB MCP server)
- OpenShift cluster access

---

## Step 1: Deploy MCP Server

MCP server is a separate service that exposes tools via MCP protocol.

### For MongoDB MCP Server

👉 **[See MongoDB MCP Setup Guide](04-mongodb-mcp-setup.md)**

**Key points:**
- MCP server runs as separate deployment
- Uses **streamable HTTP transport** (not SSE)
- Endpoint: `/mcp` (NOT `/sse`)
- Must be accessible from LlamaStack pods

---

## Step 2: Register MCP Server

Register the MCP server as a toolgroup in LlamaStack.

### Using Script (Recommended)

```bash
# From project root
./scripts/register-mongodb-mcp.sh
```

### Manual Registration

```bash
# Get MCP server URL (inside cluster)
MCP_URL="http://mongodb-mcp-server.my-first-model.svc.cluster.local:3000"

# Get LlamaStack URL
LLAMA_STACK_URL=$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')

# Register toolgroup
curl -k -X POST "https://${LLAMA_STACK_URL}/v1/toolgroups" \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": "model-context-protocol",
    "toolgroup_id": "mcp::mongodb",
    "mcp_endpoint": {
      "uri": "'"${MCP_URL}"'/mcp"
    }
  }'
```

**Key Points:**
- Use **service URL** (not route) - LlamaStack runs in-cluster
- Endpoint must be **`/mcp`** for streamable HTTP transport
- Toolgroup ID format: **`mcp::<name>`**

---

## Step 3: Verify Registration

```bash
# List toolgroups
curl -k "https://${LLAMA_STACK_URL}/v1/toolgroups"

# Get specific toolgroup
curl -k "https://${LLAMA_STACK_URL}/v1/toolgroups/mcp::mongodb"
```

---

## Step 4: Create Agent with MCP Tools

### Agent Configuration

```python
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url=llamastack_url)

agent_config = {
    "model": "vllm-inference/llama-32-3b-instruct",
    "instructions": "You have access to MongoDB through MCP tools.",
    "toolgroups": ["mcp::mongodb"],  # Include MCP toolgroup
    "tool_choice": "auto",  # Let agent decide when to use tools
    "sampling_params": {
        "max_tokens": 2000
    }
}

agent = client.alpha.agents.create(agent_config=agent_config)
```

**Key Points:**
- `toolgroups` must include `"mcp::mongodb"`
- `tool_choice="auto"` lets agent decide when to use tools
- `max_tokens` must be > 0

---

## Step 5: Use Agent with MCP Tools

### Create Session

```python
session = client.alpha.agents.session.create(
    agent_id=agent.agent_id,
    session_name="mongodb-test"
)
```

### Query Agent

```python
turn_stream = client.alpha.agents.turn.create(
    agent_id=agent.agent_id,
    session_id=session.session_id,
    messages=[{"role": "user", "content": "What collections are in the mcp_demo database?"}],
    stream=True
)
```

The agent will automatically:
1. Detect the query needs MongoDB access
2. Call MongoDB MCP tools
3. Use real data in response

---

## MCP Transport Types

### streamable-http (Recommended)

- **Endpoint**: `/mcp`
- **Protocol**: HTTP with streaming
- **Use case**: Web deployments, OpenShift

### stdio (Legacy)

- **Protocol**: Standard input/output
- **Use case**: Local scripts, command-line

### sse (Legacy)

- **Protocol**: Server-Sent Events
- **Use case**: Legacy deployments

---

## Available MCP Tools (MongoDB)

### Database Operations
- `list-databases` - List all databases
- `list-collections` - List collections in database

### Document Operations
- `count-documents` - Count documents in collection
- `find-documents` - Query documents
- `insert-document` - Insert new document
- `update-document` - Update existing document

---

## Troubleshooting

### Toolgroup Registration Fails

```bash
# Check MCP server is running
oc get pods -n my-first-model | grep mongodb-mcp-server

# Check MCP server logs
oc logs deployment/mongodb-mcp-server -n my-first-model

# Test MCP endpoint
oc exec deployment/mongodb-mcp-server -n my-first-model -- curl http://localhost:3000/mcp
```

### Agent Not Using Tools

```bash
# Verify toolgroup is registered
curl -k "https://${LLAMA_STACK_URL}/v1/toolgroups/mcp::mongodb"

# Check agent configuration
# Ensure toolgroups includes "mcp::mongodb"
# Ensure max_tokens > 0
```

### Tool Execution Errors

```bash
# Check MCP server logs
oc logs deployment/mongodb-mcp-server -n my-first-model --tail=100

# Check MongoDB connection
oc exec deployment/mongodb-mcp-server -n my-first-model -- curl http://mongodb:27017
```

---

## Best Practices

1. **Use service URLs** for in-cluster communication
2. **Test MCP server** before registering
3. **Monitor tool execution** in MCP server logs
4. **Use read-only mode** for production safety
5. **Implement error handling** in agent code

---

## Next Steps

- **[Agent Configuration Guide](07-agent-configuration.md)** - Configure agents with tools
- **[Quick Reference](quick-reference.md)** - Common MCP commands

---

**Need help?** → [Troubleshooting Guide](troubleshooting.md) | [Quick Reference](quick-reference.md)

