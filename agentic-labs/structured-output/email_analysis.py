"""A basic structured output example"""

import pprint
from pydantic import BaseModel, Field
from strands import Agent

import agent_testing_utils


class EmailAnalysis(BaseModel):
    """The analysis of an email message"""
    one_line_summary: str = Field(description="One-line summary of the email", min_length=1)
    requires_urgent_response: bool = Field(
        description="Indicates if the email requires an immediate response", default=False
    )


# agent_testing_utils.display_and_test_structured_output(pydantic_class=EmailAnalysis)

agent_testing_utils.display_structured_output_tool_spec(EmailAnalysis)

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

result = agent("Generate a sample output using the tool.", structured_output_model=EmailAnalysis)

pprint.pp(result.structured_output)

print(result.structured_output.model_dump_json(indent=4))
