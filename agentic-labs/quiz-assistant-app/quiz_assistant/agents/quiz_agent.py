"""Agent logic for language quiz generation."""

from strands import Agent

from quiz_assistant.tools import quiz_tools
from quiz_assistant.agents.hooks import ToolCallRecorderHookProvider, ToolCallLimiterHookProvider


QUIZ_SYSTEM_PROMPT = """You are a quiz assistant.
Work with the user to brainstorm, create and edit a quiz.
You can only work on one quiz at a time.
"""


def create_quiz_agent():
    """Creates an agent for creating quizzes."""

    agent = Agent(
        # model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        system_prompt=QUIZ_SYSTEM_PROMPT,
        tools=[quiz_tools.create_quiz],
        hooks=[
            ToolCallRecorderHookProvider(record_results=True),
            ToolCallLimiterHookProvider(max_tool_calls_per_invocation=1),
        ],
    )

    return agent
