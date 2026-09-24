"""A basic reusable agent"""

import math
from typing import Annotated
from strands import Agent, tool

from proactive_conversation_manager import ProactiveSummarizingConversationManager


@tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)


@tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)


@tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y


@tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)


def create_agent_and_proactive_manager():
    """Creates and returns an agent"""

    summarizing_agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

    proactive_manager = ProactiveSummarizingConversationManager(
        preserve_recent_messages=4,  # set too low, for demo purposes only!
        maximum_message_count_before_summarizing=8,  # set too low, for demo purposes only!
        summarization_agent=summarizing_agent,
        summary_ratio=0.8,
    )

    main_agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        conversation_manager=proactive_manager,
        tools=[cosine, sine, divide, raise_to_power],
    )

    return main_agent, proactive_manager
