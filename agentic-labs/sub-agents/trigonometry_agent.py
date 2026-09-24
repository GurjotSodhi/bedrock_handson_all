"""The trigonometry agent"""

import math
from typing import Annotated
from strands import Agent, tool


@tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)


@tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)


@tool(description="Calculates the tangent of x")
def tangent(x: Annotated[float, "The value of x in radians"]) -> float:
    """Tangent tool"""
    return math.tan(x)


def get_tools():
    return [cosine, sine, tangent]


def create_trigonometry_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(tools=get_tools(), model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent
