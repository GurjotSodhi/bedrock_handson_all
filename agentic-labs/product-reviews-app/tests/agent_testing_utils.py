"""Utilities for structured output and Pydantic models"""

import json
import pprint

from pydantic import BaseModel
from strands import Agent
from strands.tools.structured_output.structured_output_utils import convert_pydantic_to_tool_spec

# from strands.types.exceptions import StructuredOutputException


def display_structured_output_tool_spec(pydantic_class: BaseModel):
    """Displays the generated tool spec based on the Pydantic class"""
    tool_spec = convert_pydantic_to_tool_spec(pydantic_class)

    print("STRUCTURED OUTPUT CLASS' TOOL SPEC:")
    print(json.dumps(tool_spec, indent=4))
    print("-" * 40)


def test_structured_output_result(
    pydantic_class: BaseModel, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Runs and displays the generated structured output for the Pydantic class"""
    agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0", system_prompt=system_prompt)
    result = agent(prompt, structured_output_model=pydantic_class)
    generated_output: pydantic_class = result.structured_output

    print(agent.system_prompt)

    print("STRUCTURED OUTPUT RESULT:")
    pprint.pp(generated_output)
    print("-" * 40)

    print("STRUCTURED OUTPUT RESULT AS JSON:")
    print(generated_output.model_dump_json(indent=4))
    print("-" * 40)


def display_and_test_structured_output(
    pydantic_class: BaseModel, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Displays and tests the tool spec and results for a Pydantic class"""
    display_structured_output_tool_spec(pydantic_class=pydantic_class)

    test_structured_output_result(pydantic_class=pydantic_class, prompt=prompt, system_prompt=system_prompt)
