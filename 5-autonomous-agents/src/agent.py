"""
Autonomous Agent Framework using LlamaStack

This module provides the core agent framework that combines
reasoning (LLM) with action-taking (tools) using llamastack.
"""

from typing import Dict, List, Optional, Any
import os
import json
import requests

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
    
    def __init__(
        self,
        tool_registry: ToolRegistry,
        memory: Optional[AgentMemory] = None,
        llamastack_url: Optional[str] = None,
        agent_id: Optional[str] = None,
        verbose: bool = True
    ):
        """
        Initialize autonomous agent.
        
        Args:
            tool_registry: Registry containing available tools
            memory: Optional memory system for learning
            llamastack_url: URL of llamastack server (default: http://localhost:8321)
            agent_id: Optional agent ID if agent already exists in llamastack
            verbose: Whether to print detailed execution logs
        """
        self.tool_registry = tool_registry
        self.memory = memory or AgentMemory()
        self.verbose = verbose
        
        # Initialize llamastack connection
        self.llamastack_url = llamastack_url or os.getenv("LLAMA_STACK_URL", "http://localhost:8321")
        self.agent_id = agent_id
        
        # Create or get agent in llamastack
        if not self.agent_id:
            self.agent_id = self._create_agent()
        else:
            self._verify_agent_exists()
    
    def _create_agent(self) -> str:
        """
        Create an agent in llamastack.
        
        Returns:
            Agent ID
        """
        # Get tools in llamastack format
        tools = self.tool_registry.get_tools_for_llamastack()
        
        # Agent instructions
        instructions = """You are an autonomous IT operations agent. Your job is to monitor IT services, identify problems, and take corrective actions.

When analyzing IT services:
1. First, check the status of services to understand the current state
2. Identify any problems (failed services, high CPU/memory, degraded performance)
3. Take appropriate corrective actions (restart failed services, scale overloaded services)
4. Verify that actions were successful
5. Provide a clear summary of what was done

Always be careful and thoughtful. Only take actions that are necessary and safe.
If you're unsure about an action, explain your reasoning."""
        
        # Create agent via llamastack API
        payload = {
            "instructions": instructions,
            "tools": tools,
            "model": {
                "provider": "ollama",
                "model": "llama3.2:3b"
            }
        }
        
        try:
            response = requests.post(
                f"{self.llamastack_url}/v1/agents",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            agent_data = response.json()
            agent_id = agent_data.get("id")
            
            if self.verbose:
                print(f"✅ Created agent in llamastack: {agent_id}")
            
            return agent_id
        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"⚠️  Could not connect to llamastack server at {self.llamastack_url}")
                print(f"   Error: {e}")
                print(f"   Falling back to local agent execution")
            # Fallback: return a placeholder ID for local execution
            return "local-agent"
    
    def _verify_agent_exists(self):
        """Verify that the agent exists in llamastack"""
        try:
            response = requests.get(
                f"{self.llamastack_url}/v1/agents/{self.agent_id}",
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            if self.verbose:
                print(f"⚠️  Agent {self.agent_id} not found, will use local execution")
    
    def _execute_tool_locally(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a tool locally (fallback when llamastack is not available).
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool
            
        Returns:
            Tool execution result
        """
        return self.tool_registry.execute_tool(tool_name, **tool_input)
    
    def _run_with_llamastack(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Run task using llamastack agent API.
        
        Args:
            task: Description of the task to perform
            context: Optional additional context
            
        Returns:
            Dictionary with execution results
        """
        # Build input with context
        input_text = task
        if context:
            input_text = f"Context: {context}\n\nTask: {task}"
        
        # Create a turn (interaction) with the agent
        payload = {
            "input": input_text
        }
        
        try:
            # Create a session/thread for this interaction
            session_response = requests.post(
                f"{self.llamastack_url}/v1/agents/{self.agent_id}/sessions",
                json={},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            session_response.raise_for_status()
            session_data = session_response.json()
            session_id = session_data.get("id")
            
            # Create a turn in the session
            turn_response = requests.post(
                f"{self.llamastack_url}/v1/agents/{self.agent_id}/sessions/{session_id}/turns",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=300  # 5 minutes for agent execution
            )
            turn_response.raise_for_status()
            turn_data = turn_response.json()
            
            # Get the result
            result = turn_data.get("output", "")
            
            # Extract tool calls if any
            tool_calls = turn_data.get("tool_calls", [])
            
            return {
                "success": True,
                "result": result,
                "session_id": session_id,
                "turn_id": turn_data.get("id"),
                "tool_calls": tool_calls
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    def _run_locally(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Run task using local execution (fallback).
        
        This implements a simple agent loop without llamastack server.
        
        Args:
            task: Description of the task to perform
            context: Optional additional context
            
        Returns:
            Dictionary with execution results
        """
        # Simple local agent implementation
        # In a real scenario, you'd use ollama directly or another LLM client
        
        input_text = task
        if context:
            input_text = f"Context: {context}\n\nTask: {task}"
        
        # For now, return a placeholder
        # In notebooks, we'll show how to use ollama directly for local execution
        return {
            "success": True,
            "result": f"Local agent execution for: {input_text}\n(Use llamastack server for full agent capabilities)",
            "mode": "local"
        }
    
    def run(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a task.
        
        Args:
            task: Description of the task to perform
            context: Optional additional context
            
        Returns:
            Dictionary with execution results
        """
        # Try llamastack first, fallback to local
        if self.agent_id != "local-agent" and self.llamastack_url.startswith("http"):
            result = self._run_with_llamastack(task, context)
        else:
            result = self._run_locally(task, context)
        
        # Remember this execution in memory
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
        """
        Analyze the current environment state.
        
        Returns:
            Dictionary with analysis results
        """
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
        # Check memory for similar problems
        if self.memory:
            similar_problems = self.memory.get_similar_problems(issue_description, limit=3)
            if similar_problems:
                context = "Similar problems solved before:\n"
                for prob in similar_problems:
                    context += f"- {prob.problem_description}: {'Solved' if prob.success else 'Failed'}\n"
            else:
                context = None
        else:
            context = None
        
        task = f"Remediate the following issue: {issue_description}"
        return self.run(task, context=context)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about agent's memory.
        
        Returns:
            Dictionary with memory statistics
        """
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
