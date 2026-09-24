"""List MCP tools"""

import json
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="python", args=["math_fastmcp_server.py"]))
)

with stdio_mcp_client:
    tools = stdio_mcp_client.list_tools_sync()

    for mcp_tool in tools:
        print("-" * 50)
        print(mcp_tool.tool_name)
        print("-" * 50)
        print(json.dumps(mcp_tool.tool_spec, indent=4))
