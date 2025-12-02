# MCP Implementation - Quick Reference

## What We Learned

### 1. MCP Server Deployment
- MCP server is a separate service that exposes tools via MCP protocol
- Uses **streamable HTTP transport** (not SSE)
- Endpoint: `/mcp` (NOT `/sse`)
- Must be accessible from LlamaStack pods

### 2. Registration Process
```bash
# Register MCP server as toolgroup
POST /v1/toolgroups
{
  "provider_id": "model-context-protocol",
  "toolgroup_id": "mcp::mongodb",
  "mcp_endpoint": {
    "uri": "http://mongodb-mcp-server.<namespace>.svc.cluster.local:3000/mcp"
  }
}
```

**Key Points:**
- Use service URL (not route) - LlamaStack runs in-cluster
- Endpoint must be `/mcp` for streamable HTTP
- Toolgroup ID format: `mcp::<name>`

### 3. Agent Configuration
```json
{
  "agent_config": {
    "model": "...",
    "instructions": "...",
    "toolgroups": ["mcp::mongodb"],
    "tool_choice": "auto",
    "sampling_params": {
      "max_tokens": 2000
    }
  }
}
```

**Required:**
- `toolgroups`: Array with toolgroup IDs
- `sampling_params.max_tokens`: Must be > 0

### 4. Agent Interaction
- Create session: `POST /v1/agents/{agent_id}/session`
- Create turn: `POST /v1/agents/{agent_id}/session/{session_id}/turn` (with `stream: true`)
- Agent automatically calls MCP tools when needed
- Tool results are returned to agent
- Agent generates response using real data

## Complete Flow

1. **Deploy** MCP server (e.g., MongoDB MCP server)
2. **Register** MCP server with LlamaStack (creates toolgroup)
3. **Create** agent with toolgroup in `toolgroups` array
4. **Query** agent - it will use MCP tools automatically
5. **Agent** calls tools → gets results → generates response

## Testing

```bash
# 1. Verify registration
./openshift/scripts/test-mongodb-mcp-simple.sh

# 2. Test agent querying database
python3 openshift/scripts/test-mongodb-agent-live.py
```

## Common Mistakes

1. ❌ Using `/sse` endpoint (should be `/mcp` for streamable HTTP)
2. ❌ Using route URL instead of service URL
3. ❌ Forgetting `max_tokens` in agent config
4. ❌ Not including toolgroup in `toolgroups` array
5. ❌ Not waiting for LlamaStack to refresh after registration

