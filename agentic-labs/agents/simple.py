"""A simple agent demo"""

import math
from strands import Agent, tool


@tool
def cosine(x: float) -> float:
    return math.cos(x)


@tool
def sine(x: float) -> float:
    return math.sin(x)


@tool(description="Divide x by y")
def divide(x: float, y: float) -> float:
    return x / y


agent = Agent(tools=[cosine, sine, divide], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("What is the tangent of 8.12515? Provide accuracy to 5 places.")
