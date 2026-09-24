"""Tool tracking demo"""

import json
import math
from typing import Annotated

from strands import Agent, tool

from tool_call_recorder import ToolCallRecorderHookProvider


@tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)


@tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)


@tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y


agent = Agent(
    tools=[cosine, sine, divide],
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    hooks=[ToolCallRecorderHookProvider(record_requests=True, record_results=True)],
)


print("-" * 40)
print("Round 1")
r1 = agent("What is the tangent of 1.11122? Provide accuracy to 5 places.")
print("-" * 40)
print(json.dumps(r1.state.get("tool_requests", []), indent=4))  # only shows tool requests from the first invocation
print("-" * 40)
print(json.dumps(r1.state.get("tool_results", []), indent=4))  # only shows tool results from the first invocation


print("-" * 40)
print("Round 2")
print("-" * 40)
r2 = agent("What is the cotangent?")
print("-" * 40)
print(json.dumps(r2.state.get("tool_requests", []), indent=4))  # only shows tool requests from the second invocation
print("-" * 40)
print(json.dumps(r2.state.get("tool_results", []), indent=4))  # only shows tool results from the second invocation
