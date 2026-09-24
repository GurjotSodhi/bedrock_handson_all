"""A basic math agent"""

from strands import Agent
from math_tools import cosine, sine, divide


def create_agent(session_id: str):
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(
        agent_id=session_id, tools=[cosine, sine, divide], model="us.anthropic.claude-haiku-4-5-20251001-v1:0"
    )
    return agent
