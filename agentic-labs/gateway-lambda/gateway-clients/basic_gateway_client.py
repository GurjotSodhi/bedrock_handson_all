"""Basic AgentCore Gateway client"""

import os

from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client

from strands import Agent
from strands.tools.mcp import MCPClient


GATEWAY_URL = os.environ.get("DEMO_GATEWAY_URL")

mcp_client = MCPClient(
    lambda: aws_iam_streamablehttp_client(endpoint=GATEWAY_URL, aws_region="us-west-2", aws_service="bedrock-agentcore")
)

with mcp_client:
    tools = mcp_client.list_tools_sync()

    agent = Agent(
        tools=tools,
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    result = agent("What is the secant squared of 1.8237?")
