"""
Tool Definitions for Autonomous Agents

Tools are the actions that agents can take. This module defines
IT operations tools that agents can use with llamastack.
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

# Handle both relative and absolute imports
try:
    from .environment import SimulatedEnvironment
except ImportError:
    from environment import SimulatedEnvironment


@dataclass
class ITTool:
    """
    Represents an IT operations tool for llamastack.
    
    Tools define what actions an agent can take and how to execute them.
    """
    name: str
    description: str
    func: Callable
    parameters: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary for llamastack"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    def execute(self, **kwargs) -> str:
        """Execute the tool function"""
        return self.func(**kwargs)


def create_tools(environment: SimulatedEnvironment) -> Dict[str, ITTool]:
    """
    Create IT operations tools for the agent.
    
    Args:
        environment: The simulated environment to interact with
        
    Returns:
        Dictionary of tool name to ITTool instance
    """
    tools = {}
    
    # Check Service Status Tool
    def check_service_status(service_name: str) -> str:
        """Check the status of an IT service"""
        result = environment.get_service_status(service_name)
        if result is None:
            return f"Service '{service_name}' not found"
        return f"Service '{service_name}': Status={result['status']}, CPU={result['cpu_usage']:.1f}%, Memory={result['memory_usage']:.1f}%"
    
    tools["check_service_status"] = ITTool(
        name="check_service_status",
        description="Check the status of an IT service. Returns information about service health including CPU usage, memory usage, and current status. Use this to monitor service health and detect issues. Args: service_name (str) - The name of the service to check (e.g., 'web-server', 'database')",
        func=check_service_status,
        parameters={
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "The name of the service to check"
                }
            },
            "required": ["service_name"]
        }
    )
    
    # Restart Service Tool
    def restart_service(service_name: str) -> str:
        """Restart an IT service"""
        result = environment.restart_service(service_name)
        if result["success"]:
            return f"✅ {result['message']}. Restart count: {result.get('restart_count', 0)}"
        else:
            return f"❌ {result['message']}"
    
    tools["restart_service"] = ITTool(
        name="restart_service",
        description="Restart an IT service that is not working properly. Use this when a service has failed or is in a degraded state. This will stop and start the service, which may cause brief downtime. Args: service_name (str) - The name of the service to restart",
        func=restart_service,
        parameters={
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "The name of the service to restart"
                }
            },
            "required": ["service_name"]
        }
    )
    
    # Scale Service Tool
    def scale_service(service_name: str, replicas: int) -> str:
        """Scale a service"""
        if replicas < 1:
            return "❌ Error: Replicas must be at least 1"
        result = environment.scale_service(service_name, replicas)
        if result["success"]:
            return f"✅ {result['message']}. CPU: {result['cpu_usage']:.1f}%, Memory: {result['memory_usage']:.1f}%"
        else:
            return f"❌ {result['message']}"
    
    tools["scale_service"] = ITTool(
        name="scale_service",
        description="Scale a service by changing the number of replicas. Use this when a service is experiencing high load and needs more resources. Increasing replicas distributes load and improves performance. Args: service_name (str) - The name of the service to scale, replicas (int) - Number of replicas (minimum 1, recommended 2-5 for high load)",
        func=scale_service,
        parameters={
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "The name of the service to scale"
                },
                "replicas": {
                    "type": "integer",
                    "description": "Number of replicas (minimum 1)"
                }
            },
            "required": ["service_name", "replicas"]
        }
    )
    
    # Get All Services Tool
    def get_all_services() -> str:
        """Get status of all services"""
        services = environment.get_all_services()
        if not services:
            return "No services found"
        result_lines = ["All Services Status:"]
        for service in services:
            status_icon = "✅" if service["status"] == "running" else "⚠️" if service["status"] == "degraded" else "❌"
            result_lines.append(
                f"{status_icon} {service['name']}: {service['status']} "
                f"(CPU: {service['cpu_usage']:.1f}%, Memory: {service['memory_usage']:.1f}%)"
            )
        return "\n".join(result_lines)
    
    tools["get_all_services"] = ITTool(
        name="get_all_services",
        description="Get the status of all services in the environment. Use this to get an overview of the entire system health. Returns a list of all services with their current status and metrics. No arguments required.",
        func=get_all_services,
        parameters={
            "type": "object",
            "properties": {},
            "required": []
        }
    )
    
    return tools


class ToolRegistry:
    """
    Registry for managing available tools for llamastack agents.
    
    This class helps organize and provide tools to agents.
    """
    
    def __init__(self, environment: SimulatedEnvironment):
        """
        Initialize tool registry.
        
        Args:
            environment: The simulated environment to interact with
        """
        self.environment = environment
        self._tools: Dict[str, ITTool] = create_tools(environment)
    
    def get_tool(self, name: str) -> Optional[ITTool]:
        """
        Get a tool by name.
        
        Args:
            name: Name of the tool
            
        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)
    
    def get_all_tools(self) -> Dict[str, ITTool]:
        """Get all registered tools"""
        return self._tools
    
    def get_tools_for_llamastack(self) -> list[Dict[str, Any]]:
        """
        Get tools in llamastack format (OpenAI function calling format).
        
        Returns:
            List of tool definitions for llamastack API in OpenAI format
        """
        tools = []
        for tool in self._tools.values():
            # LlamaStack expects OpenAI function calling format
            tool_def = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            tools.append(tool_def)
        return tools
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """
        Execute a tool.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Arguments for the tool
            
        Returns:
            Result of tool execution
        """
        tool = self.get_tool(tool_name)
        if tool is None:
            return f"Tool '{tool_name}' not found"
        return tool.execute(**kwargs)
    
    def list_tools(self) -> list[Dict[str, str]]:
        """
        List all available tools with descriptions.
        
        Returns:
            List of tool information dictionaries
        """
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self._tools.values()
        ]

