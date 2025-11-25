"""
Autonomous Agent Framework using LlamaStack

This module provides the core agent framework that combines
reasoning (LLM) with action-taking (tools) using llamastack.
"""

from typing import Dict, List, Optional, Any
import os
import time

# Import llamastack SDK
try:
    from llama_stack_client import LlamaStackClient
except ImportError:
    raise ImportError(
        "llama_stack_client is required. Install it with: pip install llama-stack-client"
    )

# Handle both relative and absolute imports
try:
    from .tools import ToolRegistry
    from .memory import AgentMemory
except ImportError:
    from tools import ToolRegistry
    from memory import AgentMemory


class AutonomousAgent:
    """
    Autonomous agent that can reason about IT operations and take actions.
    
    The agent uses llamastack for LLM reasoning and a set of tools for actions.
    It follows a ReAct pattern: Reasoning + Acting.
    """
    
    # Default agent instructions
    DEFAULT_INSTRUCTIONS = """You are an autonomous IT operations agent. Your job is to monitor IT services, identify problems, and take corrective actions.

When analyzing IT services:
1. First, check the status of services to understand the current state
2. Identify any problems (failed services, high CPU/memory, degraded performance)
3. Take appropriate corrective actions (restart failed services, scale overloaded services)
4. Verify that actions were successful
5. Provide a clear summary of what was done

Always be careful and thoughtful. Only take actions that are necessary and safe.
If you're unsure about an action, explain your reasoning."""
    
    def __init__(
        self,
        tool_registry: ToolRegistry,
        memory: Optional[AgentMemory] = None,
        llamastack_url: Optional[str] = None,
        model: str = "ollama/llama3.2:3b",
        instructions: Optional[str] = None,
        verbose: bool = True
    ):
        """
        Initialize autonomous agent.
        
        Args:
            tool_registry: Registry containing available tools
            memory: Optional memory system for learning
            llamastack_url: URL of llamastack server (default: http://localhost:8321)
            model: Model identifier (default: ollama/llama3.2:3b)
            instructions: Custom agent instructions (uses default if not provided)
            verbose: Whether to print detailed execution logs
        """
        self.tool_registry = tool_registry
        self.memory = memory or AgentMemory()
        self.verbose = verbose
        
        # Initialize llamastack client
        self.llamastack_url = llamastack_url or os.getenv("LLAMA_STACK_URL", "http://localhost:8321")
        self.client = LlamaStackClient(base_url=self.llamastack_url)
        
        # Verify connection
        self._verify_connection()
        
        # Get tools and instructions
        tools = self.tool_registry.get_tools_for_llamastack()
        instructions = instructions or self.DEFAULT_INSTRUCTIONS
        
        # Create agent via API to get agent_id
        agent_response = self.client.alpha.agents.create(
            agent_config={
                "model": model,
                "instructions": instructions,
                "tools": tools
            }
        )
        
        self.agent_id = agent_response.agent_id
        
        if self.verbose:
            print(f"✅ Initialized agent with model: {model}")
            print(f"   Agent ID: {self.agent_id}")
    
    def _verify_connection(self):
        """Verify llamastack server is available."""
        try:
            self.client.models.list()
        except Exception as e:
            raise ConnectionError(
                f"Cannot connect to llamastack server at {self.llamastack_url}. "
                f"Please ensure llamastack is running. Error: {e}"
            )
    
    def _extract_content_from_chunk(self, chunk) -> tuple[str, Optional[str], List, bool]:
        """
        Extract content, turn_id, tool_calls, and completion status from a streaming chunk.
        
        Args:
            chunk: AgentTurnResponseStreamChunk object
            
        Returns:
            Tuple of (content, turn_id, tool_calls, is_complete)
        """
        content = ""
        turn_id = None
        tool_calls = []
        is_complete = False
        
        if not (hasattr(chunk, 'event') and chunk.event):
            return content, turn_id, tool_calls, is_complete
        
        event = chunk.event
        
        # Extract payload (contains the actual data)
        payload = self._get_payload_dict(event)
        if not payload:
            return content, turn_id, tool_calls, is_complete
        
        # Extract content from delta (streaming chunks)
        if 'delta' in payload and payload['delta']:
            delta = payload['delta']
            delta_dict = self._to_dict(delta)
            if delta_dict:
                # Try different content field names
                if 'content' in delta_dict and delta_dict['content']:
                    content = str(delta_dict['content'])
                elif 'text' in delta_dict and delta_dict['text']:
                    content = str(delta_dict['text'])
        
        # Extract turn_id
        if 'turn_id' in payload and payload['turn_id']:
            turn_id = payload['turn_id']
        elif hasattr(event, 'turn_id') and event.turn_id:
            turn_id = event.turn_id
        
        # Extract tool calls
        if 'tool_calls' in payload and payload['tool_calls']:
            tool_calls = payload['tool_calls'] if isinstance(payload['tool_calls'], list) else [payload['tool_calls']]
        
        # Check for completion
        event_type = payload.get('event_type') or getattr(event, 'event_type', None)
        if event_type in ['turn_complete', 'turn_end', 'complete', 'done']:
            is_complete = True
        
        return content, turn_id, tool_calls, is_complete
    
    def _get_payload_dict(self, event) -> Optional[Dict]:
        """Extract payload dictionary from event."""
        if not hasattr(event, 'payload') or not event.payload:
            return None
        
        payload = event.payload
        return self._to_dict(payload)
    
    def _to_dict(self, obj) -> Optional[Dict]:
        """Convert object to dictionary if possible."""
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, 'dict'):
            return obj.dict()
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return None
    
    def _run_with_llamastack(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Run task using llamastack agent API.
        
        Args:
            task: Description of the task to perform
            context: Optional additional context
            
        Returns:
            Dictionary with execution results
        """
        # Build messages
        input_text = f"Context: {context}\n\nTask: {task}" if context else task
        messages = [{"role": "user", "content": input_text}]
        
        try:
            # Create agent session
            session_name = f"session-{int(time.time())}"
            session_response = self.client.alpha.agents.session.create(
                agent_id=self.agent_id,
                session_name=session_name
            )
            session_id = session_response.session_id
            
            if self.verbose:
                print(f"📝 Created agent session: {session_id}")
            
            # Create turn and process streaming response
            turn_stream = self.client.alpha.agents.turn.create(
                agent_id=self.agent_id,
                session_id=session_id,
                messages=messages,
                stream=True
            )
            
            # Process streaming chunks
            result = ""
            turn_id = None
            tool_calls = []
            
            for chunk in turn_stream:
                chunk_content, chunk_turn_id, chunk_tool_calls, is_complete = self._extract_content_from_chunk(chunk)
                
                result += chunk_content
                if chunk_turn_id and not turn_id:
                    turn_id = chunk_turn_id
                if chunk_tool_calls:
                    tool_calls.extend(chunk_tool_calls)
                
                if is_complete:
                    break
            
            return {
                "success": True,
                "result": result.strip() or "Task completed (no output received)",
                "session_id": session_id,
                "turn_id": turn_id,
                "tool_calls": tool_calls
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    def run(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a task using llamastack.
        
        Args:
            task: Description of the task to perform
            context: Optional additional context
            
        Returns:
            Dictionary with execution results
            
        Raises:
            ConnectionError: If llamastack is not available
        """
        # Check if llamastack_url is valid (handle both string and URL object)
        url_str = str(self.llamastack_url) if self.llamastack_url else ""
        if not url_str or not url_str.startswith("http"):
            raise ConnectionError(
                "LlamaStack URL is not configured. Please set LLAMA_STACK_URL environment variable."
            )
        
        result = self._run_with_llamastack(task, context)
        
        # Store in memory
        if self.memory:
            self.memory.remember_action(
                action_type="agent_execution",
                action_params={"task": task, "context": context},
                result=result,
                success=result.get("success", False),
                context=context or ""
            )
        
        return result
    
    def analyze_environment(self) -> Dict[str, Any]:
        """Analyze the current environment state."""
        task = "Analyze the current state of all IT services. Check each service and identify any problems or issues that need attention."
        return self.run(task)
    
    def remediate_issue(self, issue_description: str) -> Dict[str, Any]:
        """
        Remediate a specific issue.
        
        Args:
            issue_description: Description of the issue to fix
            
        Returns:
            Dictionary with remediation results
        """
        context = None
        if self.memory:
            similar_problems = self.memory.get_similar_problems(issue_description, limit=3)
            if similar_problems:
                context = "Similar problems solved before:\n"
                context += "\n".join(
                    f"- {p.problem_description}: {'Solved' if p.success else 'Failed'}"
                    for p in similar_problems
                )
        
        task = f"Remediate the following issue: {issue_description}"
        return self.run(task, context=context)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about agent's memory."""
        if not self.memory:
            return {"error": "Memory not enabled"}
        
        return {
            "action_statistics": self.memory.get_action_statistics(),
            "total_actions": len(self.memory.action_history),
            "total_problems_solved": len([p for p in self.memory.problem_solutions if p.success]),
            "recent_actions": [
                {
                    "type": a.action_type,
                    "success": a.success,
                    "timestamp": a.timestamp
                }
                for a in self.memory.get_recent_actions(limit=5)
            ]
        }
