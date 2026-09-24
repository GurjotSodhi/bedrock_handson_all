"""A basic gateway-using agent"""

import os

from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client

from strands import Agent
from strands.tools.mcp import MCPClient

GATEWAY_URL = os.environ.get("DEMO_GATEWAY_URL")


def create_mcp_client():
    """Creates an MCP client to be used with the Strands Agent"""
    mcp_client = MCPClient(
        lambda: aws_iam_streamablehttp_client(
            endpoint=GATEWAY_URL, aws_region="us-west-2", aws_service="bedrock-agentcore"
        )
    )

    return mcp_client


def create_agent(mcp_client: MCPClient):
    """Creates and returns an agent with some basic math tools"""

    tools = mcp_client.list_tools_sync()

    agent = Agent(
        tools=tools,
        system_prompt="Respond using space raps.",
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )
    return agent
