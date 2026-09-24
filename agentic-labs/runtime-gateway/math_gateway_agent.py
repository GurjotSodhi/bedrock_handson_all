"""A basic math agent"""

import os

from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client

from strands import Agent
from strands.tools.mcp import MCPClient


GATEWAY_URL = os.getenv("DEMO_GATEWAY_URL")
if not GATEWAY_URL:
    raise ValueError("DEMO_GATEWAY_URL environment variable is not set. Set it to your MCP Gateway endpoint URL.")


def create_mcp_client():
    """Creates an MCP client that connects to the gateway using AWS IAM auth."""
    mcp_client = MCPClient(
        lambda: aws_iam_streamablehttp_client(
            endpoint=GATEWAY_URL, aws_region="us-west-2", aws_service="bedrock-agentcore"
        )
    )

    return mcp_client


def create_agent(mcp_client: MCPClient, session_id: str):
    """Creates and returns an agent with some basic math tools"""

    # Setting callback_handler=None will override the default PrintingCallbackHandler
    # So we don't have to see all LLM responses in our CloudWatch logs
    agent = Agent(
        agent_id=session_id,
        tools=[mcp_client],
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        callback_handler=None,
    )
    return agent
