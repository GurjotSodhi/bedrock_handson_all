from strands import tool


@tool(  # converts the function into a tool that can be used by an agent
    description="Brief description of what your tool does",
    inputSchema={  # defines the expected structure of a tool use request made by an LLM
        "json": {  # the root of the tool definition schema
            "type": "object",  # always use the object type for the root schema
            "properties": {  # these properties map to the function's arguments
                "parameter_1": {  # Maps to the parameter_1: str argument in the function
                    "type": "string",  # Maps to the str type
                    "description": "Tells the LLM what this parameter is for",
                    # Add default and/or constraints here
                }
            },
            "required": ["parameter_1"],  # indicate the required fields here
        }
    },
)
def your_function(  # the function name becomes the name of the tool
    parameter_1: str,  # the function parameter names should map to the keys under "properties" in the tool definition
) -> str:  # return type will normally be either a simple type like a string or a number, or a dictionary
    result = parameter_1.upper()  # advanced custom tool logic in the function
    return f"Result: {result}"  # this is returned to the LLM to interpret the tool result


import agent_testing_utils

agent_testing_utils.display_and_test_decorated_function(your_function)
