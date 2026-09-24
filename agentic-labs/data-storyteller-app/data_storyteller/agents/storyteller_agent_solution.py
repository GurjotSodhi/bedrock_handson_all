"""
The storyteller agent.
"""

from strands import Agent

from data_storyteller.tools import content_creation_tools, data_retrieval_tools
from .hooks import ToolCallRecorderHookProvider


# BEGIN CHALLENGE CONTENT: Define the system prompt -----------------------------------------------

STORYTELLER_SYSTEM_PROMPT = """You are a data storyteller.
Use a mix of commentary, charts, and tables to explain the data.
Be sure to alternate between text commentary and visualizations.
Always start with an executive summary.
"""

# END CHALLENGE CONTENT ---------------------------------------------------------------------------


def _extract_result_json(event_result):
    """Extract the relevant content to return as part of the results"""

    if event_result["status"] == "error":
        try:
            error_content = event_result["content"][0]["text"]
            return {"content_type": "error", "error_message": error_content}
        except Exception:
            return event_result
    else:
        try:
            json_content = event_result["content"][0]["json"]
            return json_content
        except Exception as e:
            return {"content_type": "error", "error_message": str(e)}


def create_storyteller_agent():
    """Creates and returns the storyteller agent"""
    agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        system_prompt=STORYTELLER_SYSTEM_PROMPT,
        tools=[
            data_retrieval_tools.retrieve_data,
            content_creation_tools.create_bar_chart,
            content_creation_tools.create_line_chart,
            content_creation_tools.create_pie_chart,
            content_creation_tools.create_table,
            content_creation_tools.create_commentary,
        ],
        hooks=[ToolCallRecorderHookProvider(record_results=True)],
    )

    return agent


def run_storyteller_agent_workflow(prompt: str):
    """Run the storyteller agent workflow and return transformed results."""

    agent = create_storyteller_agent()

    result = agent(prompt)

    tool_results = result.state["tool_results"]

    transformed_results = [_extract_result_json(result) for result in tool_results]

    return transformed_results
