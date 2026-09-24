"""Testing utils for understanding Strands agents"""

import json
import textwrap

from strands import Agent
from strands.tools.decorator import DecoratedFunctionTool


def print_messages(messages):
    """Prints the formatted messages and content blocks from the agent"""
    for message in messages:
        message_role = message["role"]

        if message_role == "assistant":
            message_prefix = "\033[1;36m\n🤖"  # bold cyan
        else:
            message_prefix = "\033[1;33m\n🙂"  # bold yellow

        print(f"{message_prefix}{message_role}:\n")

        for content in message["content"]:
            for key, value in content.items():
                if isinstance(value, dict):
                    value = json.dumps(value, default=lambda n: "**UNSERIALIZABLE**")

                wrapped_line = textwrap.fill(text=f"    {key}: {value}", subsequent_indent="    ", width=79)
                print(wrapped_line)


def display_decorated_function_tool_spec(decorated_function: DecoratedFunctionTool):
    """Displays the generated tool spec based on the decorated function"""

    print("DECORATED FUNCTION'S TOOL SPEC:")
    print(json.dumps(decorated_function.tool_spec, indent=4))
    print("-" * 40)


def test_decorated_function_result(
    decorated_function: DecoratedFunctionTool, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Runs and displays the generated result for the decorated function"""

    agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0", system_prompt=system_prompt, tools=[decorated_function]
    )
    agent(prompt)

    print_messages(agent.messages)


def display_and_test_decorated_function(
    decorated_function: DecoratedFunctionTool, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Displays and tests the tool spec and results for a decorated tool function"""
    display_decorated_function_tool_spec(decorated_function=decorated_function)

    test_decorated_function_result(decorated_function=decorated_function, prompt=prompt, system_prompt=system_prompt)
