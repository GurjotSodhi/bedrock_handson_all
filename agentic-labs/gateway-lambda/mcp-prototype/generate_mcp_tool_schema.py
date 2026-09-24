import asyncio
import json

from fastmcp.tools import FunctionTool

import math_fastmcp_server


def deep_filter_schema(obj, allowed_keys):
    """Recursively filter all nested schema dictionaries to only include allowed keys."""
    if not isinstance(obj, dict):
        return obj

    filtered = {}
    for key, value in obj.items():
        if key not in allowed_keys:
            continue

        if key == "properties" and isinstance(value, dict):
            # Filter each property's schema
            filtered[key] = {
                prop_name: deep_filter_schema(prop_schema, allowed_keys) for prop_name, prop_schema in value.items()
            }
        elif key == "items" and isinstance(value, dict):
            # Filter array item schema
            filtered[key] = deep_filter_schema(value, allowed_keys)
        else:
            filtered[key] = value

    return filtered


def get_standardized_tool_spec_from_fastmcp_decorated_function(tool: FunctionTool):
    # filter out any extra keys like "x-fastmcp-wrap-result"
    schema_keys = ["type", "properties", "required", "items", "description"]

    return {
        "name": tool.name,
        "description": tool.description,
        "inputSchema": deep_filter_schema(tool.parameters, schema_keys),
        "outputSchema": deep_filter_schema(tool.output_schema, schema_keys),
    }


def main():
    """Generate tool specs from FastMCP-decorated functions and save to JSON."""

    tools = asyncio.run(math_fastmcp_server.mcp.list_tools())

    tool_specs = [get_standardized_tool_spec_from_fastmcp_decorated_function(tool) for tool in tools]

    with open("tool_specs.json", "w") as f:
        json.dump(tool_specs, f, indent=4)


if __name__ == "__main__":
    main()
