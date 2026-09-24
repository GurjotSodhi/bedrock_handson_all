"""A basic reusable agent"""

import os
import math
from typing import Annotated

from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from strands import Agent, tool


MEM_ID = os.getenv("DEMO_MEMORY_ID")


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


def get_session_manager(session_id: str, actor_id: str) -> AgentCoreMemorySessionManager:
    """Gets a session manager to be used by the Agent for memory management"""
    config = AgentCoreMemoryConfig(
        memory_id=MEM_ID,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            "/preferences/{actorId}/": RetrievalConfig(top_k=5, relevance_score=0.7),
            "/facts/{actorId}/": RetrievalConfig(top_k=10, relevance_score=0.3),
            "/summaries/{actorId}/{sessionId}/": RetrievalConfig(top_k=5, relevance_score=0.5),
        },
    )

    session_manager = AgentCoreMemorySessionManager(config)

    return session_manager


def create_agent(session_manager: AgentCoreMemorySessionManager):
    """Creates and returns an agent"""

    agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        session_manager=session_manager,
        tools=[cosine, sine, divide],
    )

    return agent
