import subprocess
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create MCP server instance
mcp_server = Server("terminal-mcp-server")

# Define safe commands (whitelist approach for security)
SAFE_COMMANDS = {
    "ls", "pwd", "whoami", "date", "uptime", 
    "df", "du", "free", "ps", "top", "htop",
    "cat", "head", "tail", "grep", "find",
    "echo", "uname", "hostname", "env"
}

def is_safe_command(command: str) -> bool:
    """Check if command is in the safe whitelist."""
    cmd_parts = command.strip().split()
    if not cmd_parts:
        return False
    base_cmd = cmd_parts[0]
    return base_cmd in SAFE_COMMANDS

@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="execute_terminal_command",
            description="Execute a safe terminal command. Supported commands: ls, pwd, whoami, date, uptime, df, du, free, ps, top, cat, head, tail, grep, find, echo, uname, hostname, env. Returns command output or error message.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The terminal command to execute (must be from safe whitelist)"
                    }
                },
                "required": ["command"]
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "execute_terminal_command":
        command = arguments.get("command", "")
        
        if not command:
            return [TextContent(type="text", text="Error: No command provided")]
        
        if not is_safe_command(command):
            return [TextContent(
                type="text",
                text=f"Error: Command '{command.split()[0]}' is not in the safe whitelist. Allowed commands: {', '.join(sorted(SAFE_COMMANDS))}"
            )]
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            
            output = result.stdout if result.stdout else result.stderr
            return_code = result.returncode
            
            response = f"Command: {command}\n"
            response += f"Return code: {return_code}\n"
            response += f"Output:\n{output}"
            
            return [TextContent(type="text", text=response)]
            
        except subprocess.TimeoutExpired:
            return [TextContent(type="text", text=f"Error: Command '{command}' timed out after 10 seconds")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error executing command: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

