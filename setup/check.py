"""Installation check"""

from strands import Agent, tool


@tool
def configuration_check() -> str:
    return "Configuration complete!"


agent = Agent(tools=[configuration_check], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("Please confirm if the configuration is complete")

print()
