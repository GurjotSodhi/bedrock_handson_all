"""The conversion agent"""

import math
from typing import Annotated
from strands import Agent, tool


@tool(description="Converts degrees to radians")
def degrees_to_radians(x: Annotated[float, "The value of x in degrees"]) -> float:
    """degrees_to_radians tool"""
    return math.radians(x)


@tool(description="Converts radians to degrees")
def radians_to_degrees(x: Annotated[float, "The value of x in radian"]) -> float:
    """radians_to_degrees tool"""
    return math.degrees(x)


def get_tools():
    return [radians_to_degrees, degrees_to_radians]


def create_conversion_agent():
    """Creates and returns an agent with conversion tools"""
    agent = Agent(tools=get_tools(), model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent
