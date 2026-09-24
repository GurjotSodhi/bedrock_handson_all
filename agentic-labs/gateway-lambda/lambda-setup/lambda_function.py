"""Lambda function for AgentCore Gateway target

When AgentCore Gateway receives a tool call from an agent, it forwards the
request to this Lambda function. The Gateway passes the tool name via the
client context, and the tool arguments as the event payload.

This handler looks up the matching function in math_tool_functions and
calls it with the provided arguments.
"""

from typing import Any

import math_tool_functions


def lambda_handler(event, context) -> dict[str, Any]:
    """Route an incoming Gateway tool request to the correct math function."""

    # The Gateway sends the tool name in the client context using the format
    # "targetName___toolName". We split on "___" and take the tool name part.
    gateway_tool_name = context.client_context.custom.get("bedrockAgentCoreToolName", "unknown___unknown")
    tool_name = gateway_tool_name.split("___", 1)[-1]

    # Look up the function by name in math_tool_functions.
    # getattr returns None if no matching function exists.
    func = getattr(math_tool_functions, tool_name, None)

    if func is None:
        result = f"Unknown tool: {tool_name}"
    else:
        # The event dict contains the tool's input arguments,
        # so we unpack them as keyword arguments to the function.
        result = func(**event)

    return {"statusCode": 200, "body": result}
