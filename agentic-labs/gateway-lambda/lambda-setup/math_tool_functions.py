"""Math tool functions"""

import math
from typing import Annotated


def degrees_to_radians(x: Annotated[float, "The value of x in degrees"]) -> float:
    """degrees_to_radians tool"""
    return math.radians(x)


def radians_to_degrees(x: Annotated[float, "The value of x in radians"]) -> float:
    """radians_to_degrees tool"""
    return math.degrees(x)


def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)


def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)


def tangent(x: Annotated[float, "The value of x in radians"]) -> float:
    """Tangent tool"""
    return math.tan(x)


def add(x: Annotated[float, "The augend"], y: Annotated[float, "The addend"]) -> float:
    """Addition tool"""
    return x + y


def subtract(x: Annotated[float, "The minuend"], y: Annotated[float, "The subtrahend"]) -> float:
    """Subtraction tool"""
    return x - y


def multiply(x: Annotated[float, "The multiplier"], y: Annotated[float, "The multiplicand"]) -> float:
    """Multiply tool"""
    return x * y


def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y


def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)


def cube_root(x: Annotated[float, "The value of x"]) -> float:
    """Cube root tool"""
    return math.cbrt(x)


def exponential(x: Annotated[float, "The exponent"]) -> float:
    """Exponential tool"""
    return math.exp(x)


def exponential_base_2(x: Annotated[float, "The exponent"]) -> float:
    """Exponential base 2 tool"""
    return math.exp2(x)


def exponential_minus_1(x: Annotated[float, "The exponent"]) -> float:
    """Exponential minus 1 tool"""
    return math.expm1(x)


def logarithm(x: Annotated[float, "The value"], base: Annotated[float, "The base (e by default)"] = math.e) -> float:
    """Logarithm tool"""
    return math.log(x, base)


def natural_log_plus_1(x: Annotated[float, "The value of x"]) -> float:
    """Natural logarithm of 1+x tool"""
    return math.log1p(x)


def logarithm_base_2(x: Annotated[float, "The value of x"]) -> float:
    """Base-2 logarithm tool"""
    return math.log2(x)


def logarithm_base_10(x: Annotated[float, "The value of x"]) -> float:
    """Base-10 logarithm tool"""
    return math.log10(x)


def square_root(x: Annotated[float, "The value of x"]) -> float:
    """Square root tool"""
    return math.sqrt(x)
