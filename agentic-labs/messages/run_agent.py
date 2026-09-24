"""A simple agent demo"""

from strands import Agent

from agent_testing_utils import print_messages
from simple_tools import cosine, sine, divide


agent = Agent(
    tools=[cosine, sine, divide],
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    system_prompt="Talk like a cartoonish villain, in single sentences.",
)

# Start the conversation:
agent("What is the tangent of 1.12315? Provide accuracy to 5 places.")

# Continue the conversation:
agent("What is the cotangent?")

# Cause an error:
agent("What is 3 / 0?")

# Call a tool directly:
division_result = agent.tool.divide(x=2, y=3.5)

print("-" * 30)

# Format and display the complete conversation:
print_messages(agent.messages)
