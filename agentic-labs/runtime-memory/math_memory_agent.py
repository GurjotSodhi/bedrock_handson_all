"""A basic math agent"""

import os

from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

from strands import Agent
from math_tools import cosine, sine, divide


def get_session_manager(session_id: str, actor_id: str) -> AgentCoreMemorySessionManager:
    """Creates and returns an AgentCore Memory session manager to use with a Strands SDK agent."""

    memory_id = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")

    config = AgentCoreMemoryConfig(
        memory_id=memory_id,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            "/preferences/{actorId}/": RetrievalConfig(top_k=5, relevance_score=0.7),
            "/facts/{actorId}/": RetrievalConfig(top_k=10, relevance_score=0.3),
            "/summaries/{actorId}/{sessionId}/": RetrievalConfig(top_k=5, relevance_score=0.5),
        },
    )

    session_manager = AgentCoreMemorySessionManager(agentcore_memory_config=config, region_name="us-west-2")

    return session_manager


def create_agent(session_id: str, actor_id: str):
    """Creates and returns an agent with some basic math tools"""

    session_manager = get_session_manager(session_id=session_id, actor_id=actor_id)

    agent = Agent(
        agent_id=session_id,
        tools=[cosine, sine, divide],
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        session_manager=session_manager,
    )
    return agent
