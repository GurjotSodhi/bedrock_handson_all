"""Math MCP server implemented with fastmcp library"""

import math
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP(name="MathServer")


@mcp.tool(description="Converts degrees to radians")
def degrees_to_radians(x: Annotated[float, "The value of x in degrees"]) -> float:
    """degrees_to_radians tool"""
    return math.radians(x)


@mcp.tool(description="Converts radians to degrees")
def radians_to_degrees(x: Annotated[float, "The value of x in radians"]) -> float:
    """radians_to_degrees tool"""
    return math.degrees(x)


@mcp.tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)


@mcp.tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)


@mcp.tool(description="Calculates the tangent of x")
def tangent(x: Annotated[float, "The value of x in radians"]) -> float:
    """Tangent tool"""
    return math.tan(x)


@mcp.tool(description="Adds x and y")
def add(x: Annotated[float, "The augend"], y: Annotated[float, "The addend"]) -> float:
    """Addition tool"""
    return x + y


@mcp.tool(description="Subtracts y from x")
def subtract(x: Annotated[float, "The minuend"], y: Annotated[float, "The subtrahend"]) -> float:
    """Subtraction tool"""
    return x - y


@mcp.tool(description="Multiplies x by y")
def multiply(x: Annotated[float, "The multiplier"], y: Annotated[float, "The multiplicand"]) -> float:
    """Multiply tool"""
    return x * y


@mcp.tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y


@mcp.tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)


@mcp.tool(description="Calculates the cube root of x")
def cube_root(x: Annotated[float, "The value of x"]) -> float:
    """Cube root tool"""
    return math.cbrt(x)


@mcp.tool(description="Calculates e raised to the power x")
def exponential(x: Annotated[float, "The exponent"]) -> float:
    """Exponential tool"""
    return math.exp(x)


@mcp.tool(description="Calculates 2 raised to the power x")
def exponential_base_2(x: Annotated[float, "The exponent"]) -> float:
    """Exponential base 2 tool"""
    return math.exp2(x)


@mcp.tool(description="Calculates e raised to the power x, minus 1")
def exponential_minus_1(x: Annotated[float, "The exponent"]) -> float:
    """Exponential minus 1 tool"""
    return math.expm1(x)


@mcp.tool(description="Calculates the logarithm of x to the given base")
def logarithm(x: Annotated[float, "The value"], base: Annotated[float, "The base (e by default)"] = math.e) -> float:
    """Logarithm tool"""
    return math.log(x, base)


@mcp.tool(description="Calculates the natural logarithm of 1+x")
def natural_log_plus_1(x: Annotated[float, "The value of x"]) -> float:
    """Natural logarithm of 1+x tool"""
    return math.log1p(x)


@mcp.tool(description="Calculates the base-2 logarithm of x")
def logarithm_base_2(x: Annotated[float, "The value of x"]) -> float:
    """Base-2 logarithm tool"""
    return math.log2(x)


@mcp.tool(description="Calculates the base-10 logarithm of x")
def logarithm_base_10(x: Annotated[float, "The value of x"]) -> float:
    """Base-10 logarithm tool"""
    return math.log10(x)


@mcp.tool(description="Calculates the square root of x")
def square_root(x: Annotated[float, "The value of x"]) -> float:
    """Square root tool"""
    return math.sqrt(x)


if __name__ == "__main__":
    mcp.run()
