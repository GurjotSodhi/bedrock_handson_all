"""Math MCP server implemented with fastmcp library"""

import math
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP(name="MathServer")


@mcp.tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)


@mcp.tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)


@mcp.tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y


@mcp.tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)


if __name__ == "__main__":
    mcp.run()
