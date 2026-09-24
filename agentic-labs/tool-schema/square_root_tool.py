"""Square root tool schema example"""

import math

from strands import tool

import agent_testing_utils


@tool(
    description="Calculates the square root of x",
    inputSchema={
        "json": {
            "type": "object",
            "properties": {"x": {"description": "The value of x", "type": "number"}},
            "required": ["x"],
        }
    },
)
def square_root(x: float) -> float:
    return math.sqrt(x)


agent_testing_utils.display_and_test_decorated_function(square_root)
