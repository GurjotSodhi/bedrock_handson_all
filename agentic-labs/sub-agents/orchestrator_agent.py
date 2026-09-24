"""A basic reusable agent"""

from typing import Annotated
from strands import Agent, tool

import conversion_agent
import trigonometry_agent
import arithmetic_agent

conversion_tools = [t.tool_name for t in conversion_agent.get_tools()]


@tool(description=f"Handles conversion requests including: {','.join(conversion_tools)}")
def do_conversion(request: Annotated[str, "The conversion request"]) -> str:
    """Conversion tool"""
    agent = conversion_agent.create_conversion_agent()
    result = agent(request)
    return result


trigonometry_tools = [t.tool_name for t in trigonometry_agent.get_tools()]


@tool(
    description=f"Handles trigonometry requests including: {','.join(trigonometry_tools)}. These functions all take values in radians."
)
def do_trigonometry(request: Annotated[str, "The trigonometry request"]) -> str:
    """Trigonometry tool"""
    agent = trigonometry_agent.create_trigonometry_agent()
    result = agent(request)
    return result


arithmetic_tools = [t.tool_name for t in arithmetic_agent.get_tools()]


@tool(description=f"Handles arithmetic requests including: {','.join(arithmetic_tools)}")
def do_arithmetic(request: Annotated[str, "The arithmetic request"]) -> str:
    """Arithmetic tool"""
    agent = arithmetic_agent.create_arithmetic_agent()
    result = agent(request)
    return result


def create_orchestrator_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(
        tools=[do_conversion, do_trigonometry, do_arithmetic], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    )
    return agent
