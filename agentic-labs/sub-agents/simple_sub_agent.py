"""A basic sub-agent"""

from typing import Annotated
from strands import Agent, tool


ORCHESTRATOR_PREFIX = "\033[1;36m\n\n🤖Orchestrator:"
SUB_AGENT_PREFIX = "\033[0;34m\n🧮Sub-Agent:"


@tool(description="Multiplies x by y")
def multiply(x: Annotated[float, "The multiplier"], y: Annotated[float, "The multiplicand"]) -> float:
    """Multiply tool"""
    return x * y


@tool(description="Handles arithmetic requests including multiplication")
def do_arithmetic(request: Annotated[str, "The arithmetic request"]) -> str:
    """Arithmetic tool"""
    arithmetic_agent = Agent(
        tools=[multiply],
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        system_prompt="Respond only with the answer to the question. Do not round your results.",
    )
    print(SUB_AGENT_PREFIX)
    arithmetic_result = arithmetic_agent(request)
    print(ORCHESTRATOR_PREFIX)
    return arithmetic_result


orchestrator_agent = Agent(tools=[do_arithmetic], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

print(ORCHESTRATOR_PREFIX)
result = orchestrator_agent("What is 3.1321 * 412.73?")
