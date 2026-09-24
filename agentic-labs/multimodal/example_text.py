"""Text message examples"""

from strands import Agent

print("PROMPT AS STRING")
agent1 = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
agent1("What are the first three colors of the rainbow?")

print("PROMPT AS LIST OF CONTENT BLOCKS")
agent2 = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
agent2(
    [
        {"text": "What are the first three colors of the rainbow?"}
    ]
)
