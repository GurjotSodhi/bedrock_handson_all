"""Agent that discovers and registers MCP tools from an AgentCore gateway."""

import uuid
from typing import Annotated

from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client


from strands import Agent, tool
from strands.tools.mcp import MCPClient, MCPAgentTool
from mcp.types import Tool as MCPTool

SYSTEM_PROMPT = """Only perform mathematical operations using a tool.
If you don't have the right tools yet, find and add the tools you need.

You MUST use tools for ALL mathematical calculations, including:
- Basic arithmetic (addition, subtraction, multiplication, division)
- Powers and exponents (squaring, cubing, etc.)
- Roots (square root, cube root, etc.)
- Trigonometric operations
- Any other numerical computation

Do NOT calculate results mentally or manually.
Even simple operations like 2+2, x², or 1/y must be performed using the appropriate tool.

If you find yourself writing out a calculation or showing arithmetic work
without invoking a tool, STOP and use a tool instead."""


class GatewaySearchAgent:
    """Wraps a Strands agent with dynamic tool discovery via MCP gateway."""

    def __init__(self, gateway_url: str):
        """Initialize the agent with an MCP gateway connection."""

        self.mcp_client = MCPClient(
            lambda: aws_iam_streamablehttp_client(
                endpoint=gateway_url, aws_region="us-west-2", aws_service="bedrock-agentcore"
            )
        )

        self.agent = Agent(
            tools=[self.find_and_add_tools],
            system_prompt=SYSTEM_PROMPT,
            model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        )

    @tool(description="Performs a semantic search for tools and adds them to your available tools.")
    def find_and_add_tools(
        self,
        tool_to_find: Annotated[
            str, "A short description of the tool to be found. Optimize this for a semantic search."
        ],
    ):
        """Search for MCP tools by description and register them with the agent."""
        print(f"tool_to_find: {tool_to_find}")

        search_result = self.mcp_client.call_tool_sync(
            tool_use_id=str(uuid.uuid4()), name="x_amz_bedrock_agentcore_search", arguments={"query": tool_to_find}
        )

        found_tool_names = []

        for t in search_result["structuredContent"]["tools"][:5]:  # Just grabbing top 5 tools (out of max 10 returned)

            tool_name = t["name"]

            if tool_name not in self.agent.tool_names:

                mcp_tool = MCPTool(
                    name=tool_name,
                    description=t["description"],
                    inputSchema=t["inputSchema"],
                )

                mcp_agent_tool = MCPAgentTool(mcp_tool, self.mcp_client)

                self.agent.tool_registry.register_tool(mcp_agent_tool)
                found_tool_names.append(t["name"])

        if found_tool_names:

            return_message = (
                f"The following additional tools have been made available to you: {', '.join(found_tool_names)}"
            )

        else:
            return_message = "No additional tools were found, based on your search criteria."

        print(return_message)
        return return_message

    def chat(self, prompt: str):
        """Send a message to the agent and stream the response."""
        return self.agent(prompt)

    def __enter__(self):
        """Open the MCP gateway connection."""
        self.mcp_client.__enter__()
        return self

    def __exit__(self, *args):
        """Close the MCP gateway connection."""
        self.mcp_client.__exit__(*args)
