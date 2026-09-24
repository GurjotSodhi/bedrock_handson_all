"Basic ToolContext example"

from strands import ToolContext, tool

import agent_testing_utils


@tool(
    context=True,
    description="Creates a new string by repeating a string a certain number of times",
    inputSchema={
        "json": {
            "properties": {
                "string_to_repeat": {
                    "type": "string",
                    "description": "The string to be repeated",
                    "minLength": 1,
                },
                "times_to_repeat": {
                    "type": "integer",
                    "description": "The number of times to repeat the string.",
                    "minimum": 0,
                },
            },
            "required": ["string_to_repeat", "times_to_repeat"],
        }
    },
)
def repeat_string(tool_context: ToolContext) -> str:

    print(tool_context.tool_use)

    string_to_repeat = tool_context.tool_use["input"]["string_to_repeat"]

    times_to_repeat = tool_context.tool_use["input"]["times_to_repeat"]

    resulting_string = string_to_repeat * times_to_repeat

    return {
        "status": "success",
        "content": [{"text": resulting_string}],
    }


agent_testing_utils.display_and_test_decorated_function(repeat_string, prompt="Repeat '-' 40 times.")
