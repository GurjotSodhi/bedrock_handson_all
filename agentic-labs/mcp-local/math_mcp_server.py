"""Math MCP server implemented with mcp library"""

import math
from pydantic import Field

from mcp.server import FastMCP  # mcp.server.FastMCP becomes MCPServer in mcp V2, Q1 2026 target date

# Create a server instance
mcp = FastMCP(name="MathServer")


@mcp.tool(description="Calculates the cosine of x.")
def cosine(x: float = Field(description="The value of x in radians")) -> float:
    """Cosine tool"""
    return math.cos(x)


@mcp.tool(description="Calculates the sine of x")
def sine(x: float = Field(description="The value of x in radians")) -> float:
    """Sine tool"""
    return math.sin(x)


@mcp.tool(description="Divides x by y")
def divide(x: float = Field(description="The numerator"), y: float = Field(description="The denominator")) -> float:
    """Divide tool"""
    return x / y


@mcp.tool(description="Raise x to the power y")
def raise_to_power(x: float = Field(description="The base"), y: float = Field(description="The exponent")) -> float:
    """Raise to power tool"""
    return math.pow(x, y)


if __name__ == "__main__":
    mcp.run()
