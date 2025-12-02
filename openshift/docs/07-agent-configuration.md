# Agent Configuration Guide

Configure LlamaStack agents with MCP tools and other capabilities.

## Overview

This guide covers:
- Creating agents with MCP toolgroups
- Configuring agent behavior
- Using agents with tools
- Best practices

---

## Basic Agent Creation

### Minimal Configuration

```python
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url=llamastack_url)

agent_config = {
    "model": "vllm-inference/llama-32-3b-instruct",
    "toolgroups": ["mcp::mongodb"],
    "sampling_params": {
        "max_tokens": 2000
    }
}

agent = client.alpha.agents.create(agent_config=agent_config)
```

---

## Agent Configuration Options

### Model Selection

```python
agent_config = {
    "model": "vllm-inference/llama-32-3b-instruct",  # vLLM model
    # OR
    "model": "ollama/llama3.2:3b",  # Ollama model (if available)
}
```

### Instructions

Guide agent behavior:

```python
agent_config = {
    "instructions": (
        "You are a helpful IT operations assistant. "
        "Always use MongoDB MCP tools to query the database when asked about data. "
        "Provide clear, concise answers based on the data you retrieve."
    ),
}
```

### Tool Groups

Specify which MCP toolgroups the agent can use:

```python
agent_config = {
    "toolgroups": [
        "mcp::mongodb",  # MongoDB tools
        # Add more toolgroups as needed
    ],
}
```

### Tool Choice

Control when agent uses tools:

```python
agent_config = {
    "tool_choice": "auto",  # Agent decides when to use tools (recommended)
    # OR
    "tool_choice": "required",  # Agent must use tools
    # OR
    "tool_choice": "none",  # Agent cannot use tools
}
```

### Sampling Parameters

Control response generation:

```python
agent_config = {
    "sampling_params": {
        "max_tokens": 2000,  # Maximum response length (MUST be > 0)
        "temperature": 0.7,  # Creativity (0.0-2.0, default: 1.0)
        "top_p": 0.9,  # Nucleus sampling (0.0-1.0)
    }
}
```

---

## Complete Example

### Agent with MongoDB MCP Tools

```python
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url=llamastack_url)

agent_config = {
    "model": "vllm-inference/llama-32-3b-instruct",
    "instructions": (
        "You are an IT operations assistant with access to MongoDB. "
        "When asked about databases, collections, or data, use the MongoDB MCP tools "
        "to query the database and provide accurate information."
    ),
    "toolgroups": ["mcp::mongodb"],
    "tool_choice": "auto",
    "sampling_params": {
        "max_tokens": 2000,
        "temperature": 0.7,
    }
}

# Create agent
agent = client.alpha.agents.create(agent_config=agent_config)

# Create session
session = client.alpha.agents.session.create(
    agent_id=agent.agent_id,
    session_name="it-ops-assistant"
)

# Query agent
turn_stream = client.alpha.agents.turn.create(
    agent_id=agent.agent_id,
    session_id=session.session_id,
    messages=[{"role": "user", "content": "What collections are in the mcp_demo database?"}],
    stream=True
)
```

---

## Using Agents

### Create Session

Sessions maintain conversation context:

```python
session = client.alpha.agents.session.create(
    agent_id=agent.agent_id,
    session_name="my-session"  # Optional, helps identify sessions
)
```

### Create Turn

A turn is one interaction with the agent:

```python
turn_stream = client.alpha.agents.turn.create(
    agent_id=agent.agent_id,
    session_id=session.session_id,
    messages=[
        {"role": "user", "content": "Your question here"}
    ],
    stream=True  # Enable streaming for real-time responses
)
```

### Retrieve Turn Results

```python
import httpx
import time

# Extract turn_id from stream
turn_id = None
for chunk in turn_stream:
    # Extract turn_id from stream chunks
    if hasattr(chunk, 'event') and chunk.event:
        # Process to get turn_id
        pass

# Wait for turn to complete
time.sleep(2)

# Retrieve turn
response = httpx.get(
    f"{llamastack_url}/v1alpha/agents/{agent.agent_id}/session/{session.session_id}/turn/{turn_id}",
    verify=False,
    timeout=30
)

data = response.json()
```

---

## Best Practices

### 1. Clear Instructions

Provide specific, actionable instructions:

```python
"instructions": "You are an IT operations assistant. Use MongoDB tools to query data. Always verify data before responding."
```

### 2. Appropriate Tool Choice

- **`auto`**: Let agent decide (recommended for most cases)
- **`required`**: Force tool usage (when tools are essential)
- **`none`**: Disable tools (for simple Q&A)

### 3. Token Limits

Set appropriate `max_tokens`:
- **Short responses**: 500-1000 tokens
- **Detailed responses**: 2000-4000 tokens
- **Long documents**: 4000+ tokens

### 4. Error Handling

```python
try:
    agent = client.alpha.agents.create(agent_config=agent_config)
except Exception as e:
    print(f"Error creating agent: {e}")
    # Handle error appropriately
```

### 5. Session Management

- **Reuse sessions** for related conversations
- **Create new sessions** for unrelated topics
- **Clean up** old sessions periodically

---

## Advanced Configuration

### Multiple Tool Groups

```python
agent_config = {
    "toolgroups": [
        "mcp::mongodb",
        "mcp::filesystem",  # If you have filesystem MCP server
        # Add more as needed
    ],
}
```

### Custom Temperature

Adjust creativity:

```python
"sampling_params": {
    "temperature": 0.1,  # More deterministic (for factual queries)
    # OR
    "temperature": 0.9,  # More creative (for brainstorming)
}
```

---

## Troubleshooting

### Agent Creation Fails

```python
# Check toolgroup exists
toolgroups = client.toolgroups.list()
print([tg.id for tg in toolgroups])

# Verify model is available
models = client.models.list()
print([m.id for m in models])
```

### Agent Not Using Tools

```python
# Check agent configuration
print(agent_config["toolgroups"])  # Should include MCP toolgroups
print(agent_config["tool_choice"])  # Should be "auto" or "required"
print(agent_config["sampling_params"]["max_tokens"])  # Must be > 0
```

### Tool Execution Errors

```python
# Check turn steps for tool errors
turn_data = get_turn_results(agent_id, session_id, turn_id)
for step in turn_data.get("steps", []):
    if step.get("type") == "tool_execution":
        print(step.get("tool_execution"))
```

---

## Next Steps

- **[MCP Integration Guide](06-mcp-integration.md)** - Complete MCP setup
- **[Quick Reference](quick-reference.md)** - Common configurations

---

**Need help?** → [Troubleshooting Guide](troubleshooting.md) | [Quick Reference](quick-reference.md)

