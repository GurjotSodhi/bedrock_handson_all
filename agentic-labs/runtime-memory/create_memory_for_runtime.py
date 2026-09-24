"""Creates AgentCore Memory"""

from bedrock_agentcore.memory import MemoryClient

client = MemoryClient(region_name="us-west-2")

print("Creating AgentCore Memory and waiting (will take a few minutes)")

# create AgentCore Memory for your application
# this will create short term memory (by default) + 3 long term memory strategies
memory = client.create_memory_and_wait(
    name="DemoAgentRuntimeMemory",
    description="Agent memory with summarization, preferences, facts, and episodes.",
    strategies=[
        {
            "summaryMemoryStrategy": {
                "name": "SessionSummaries",
                "description": "Extracts summaries about a session.",
                "namespaces": ["/summaries/{actorId}/{sessionId}/"],
            }
        },
        {
            "userPreferenceMemoryStrategy": {
                "name": "ActorPreferences",
                "description": "Extracts preferences for an actor.",
                "namespaces": ["/preferences/{actorId}/"],
            }
        },
        {
            "semanticMemoryStrategy": {
                "name": "ActorSemanticFacts",
                "description": "Extracts facts about an actor.",
                "namespaces": ["/facts/{actorId}/"],
            }
        },
    ],
)

# Get the AgentCore memory ID
memory_id = memory.get("id")

print(f"Created memory with ID: {memory_id}")
