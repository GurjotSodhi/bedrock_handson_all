"""The arithmetic agent"""

import math
from typing import Annotated
from strands import Agent, tool


@tool(description="Adds x and y")
def add(x: Annotated[float, "The augend"], y: Annotated[float, "The addend"]) -> float:
    """Addition tool"""
    return x + y


@tool(description="Subtracts y from x")
def subtract(x: Annotated[float, "The minuend"], y: Annotated[float, "The subtrahend"]) -> float:
    """Subtraction tool"""
    return x - y


@tool(description="Multiplies x by y")
def multiply(x: Annotated[float, "The multiplier"], y: Annotated[float, "The multiplicand"]) -> float:
    """Multiply tool"""
    return x * y


@tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y


@tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)


def get_tools():
    return [add, subtract, multiply, divide, raise_to_power]


def create_arithmetic_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(tools=get_tools(), model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent
