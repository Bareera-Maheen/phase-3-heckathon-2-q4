from mcp.server.lowlevel import Server
import mcp.types as types
from typing import List, Union
from src.mcp.utils import registry
import src.mcp.tools # Import to trigger registration

mcp_server = Server("todo-mcp-server")

@mcp_server.list_tools()
async def list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name=t['name'],
            description=t['description'],
            inputSchema=t['inputSchema']
        ) for t in registry.tools.values()
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    user_id = arguments.get("user_id")
    if not user_id:
        return [types.TextContent(type="text", text="Error: user_id is required")]

    if name not in registry.tool_implementations:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    func = registry.tool_implementations[name]
    # In some versions success, result = func(**arguments)
    # Based on src/agents/todo_agent.py, it returns (success, result)
    try:
        success, result = func(**arguments)
        return [types.TextContent(type="text", text=str(result) if success else f"Error: {result}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool: {str(e)}")]
