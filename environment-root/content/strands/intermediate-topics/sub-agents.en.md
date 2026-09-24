---
title: "Sub-agents"
weight: 300
---



::::alert
This lab is based on the following article: [Orchestration and sub-agents using Strands Agents](https://builder.aws.com/content/38oNsaQfOSbawDMpHdZIUdWRy99/orchestration-and-sub-agents-using-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/sub-agents**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/sub-agents

```

## Introduction to sub-agents

**Sub-agents** (AKA [agents-as-tools](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agents-as-tools/)) allow one agent to delegate work to other agents.

Delegating work to another agent has several advantages:

1. The sub-agent can be passed a smaller subset of relevant information from the orchestrator agent, to help keep its context window smaller. (We previously discussed the **context window** in the [Context engineering basics](https://builder.aws.com/content/38oLzpDYZJKUwbbKw3XyKD4Qjdd/introduction-to-context-engineering) section)
2. The sub-agent can have its own distinct set of tools, reducing the need for the orchestrator agent to fill its context window with many tool definitions.
3. The sub-agent can specialize in specific areas through [Agent standard operating procedures (SOPs)](https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/) or [skills](https://support.claude.com/en/articles/12512176-what-are-skills).
4. The sub-agent can do its work over multiple iterations and return a finished result, saving the orchestrator agent from having to fill its context window with intermediate steps.
5. The sub-agent could use another LLM better suited to a specific task. This could be due to better price/performance characteristics, or support for specific features like multimodal understanding or advanced reasoning.

 

## Code examples

The examples below require that the [strands-agents](https://pypi.org/project/strands-agents/) package is installed, and AWS access.

## A basic sub-agent example

For our purposes, sub-agents are [agents that are invoked from tools](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agents-as-tools/). You can refer to the Strands Agents documentation for [additional multi-agent patterns](https://strandsagents.com/docs/user-guide/concepts/multi-agent/multi-agent-patterns/).

Let's create a simple example in **simple\_sub\_agent.py**.

There will be two agents, `orchestrator_agent` and `arithmetic_agent`. The orchestrator agent will reference a tool that creates and runs the arithmetic agent.

To help understand the output, we'll print `ORCHESTRATOR_PREFIX` and `SUB_AGENT_PREFIX` to highlight which agent is printing to stdout.

```python
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

```

Run it:

```bash
python simple_sub_agent.py
```

The output will look something like this:

```bash
🤖Orchestrator:
I'll calculate 3.1321 * 412.73 for you.
Tool #1: do_arithmetic

🧮Sub-Agent:

Tool #1: multiply
1292.7116330000001

🤖Orchestrator:
The result of 3.1321 * 412.73 is 1292.71 (rounded to two decimal places).

```

Important things to note:

1. Only the sub-agent was told not to round, so it's OK that the orchestrator agent rounded its own result.
2. Since each agent executes independently, they both considered their first tool call to be "Tool #1".

 

## A more advanced example

Let's create an orchestrator agent that uses three sub-agents:

1. An arithmetic agent to do basic addition, subtraction, multiplication, and division operations.
2. A trigonometry agent to do basic trig operations.
3. A conversion agent to convert radians to degrees and back.

This will allow us to demonstrate orchestration across the different sub-agents with a single prompt. Each sub-agent module also includes a `get_tools()` function that we'll use to help the orchestrator agent better understand what each sub-agent can do.

 

### The arithmetic agent

Code for **arithmetic\_agent.py**:

```python
"""The arithmetic agent"""

import math
from typing import Annotated
from strands import Agent, tool

@tool(description="Adds x and y")
def add(x: Annotated[float, "The augend"], y: Annotated[float, "The addend"]) -> float:
    """Addition tool"""
    return x + y

@tool(description="Subtracts y from x")
def subtract(x: Annotated[float, "The minuend"], y: Annotated[float, "The subtrahend"]) -> float:
    """Subtraction tool"""
    return x - y

@tool(description="Multiplies x by y")
def multiply(x: Annotated[float, "The multiplier"], y: Annotated[float, "The multiplicand"]) -> float:
    """Multiply tool"""
    return x * y

@tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y

@tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)

def get_tools():
    return [add, subtract, multiply, divide, raise_to_power]

def create_arithmetic_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(tools=get_tools(), model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent

```

 

### The trigonometry agent

Code for **trigonometry\_agent.py**:

```python
# trigonometry_agent.py
"""The trigonometry agent"""

import math
from typing import Annotated
from strands import Agent, tool

@tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)

@tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)

@tool(description="Calculates the tangent of x")
def tangent(x: Annotated[float, "The value of x in radians"]) -> float:
    """Tangent tool"""
    return math.tan(x)

def get_tools():
    return [cosine, sine, tangent]

def create_trigonometry_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(tools=get_tools(), model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent

```

 

### The conversion agent

Code for **conversion\_agent.py**:

```python
"""The conversion agent"""

import math
from typing import Annotated
from strands import Agent, tool

@tool(description="Converts degrees to radians")
def degrees_to_radians(x: Annotated[float, "The value of x in degrees"]) -> float:
    """degrees_to_radians tool"""
    return math.radians(x)

@tool(description="Converts radians to degrees")
def radians_to_degrees(x: Annotated[float, "The value of x in radian"]) -> float:
    """radians_to_degrees tool"""
    return math.degrees(x)

def get_tools():
    return [radians_to_degrees, degrees_to_radians]

def create_conversion_agent():
    """Creates and returns an agent with conversion tools"""
    agent = Agent(tools=get_tools(), model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent

```

 

### The orchestrator agent

We can now reference the other agents as tools of the orchestrator agent. We keep the tools basic, just accepting a `request` string. We include a brief list of each sub-agent's tool names in the orchestrator's tool descriptions to help the orchestrator agent understand the specific capabilities of each sub-agent. We also mention that the trigonometry sub-agent's functions take values in radians, so the orchestrator can determine if conversion is required before delegating work to the trigonometry agent.

Code for **orchestrator\_agent.py**:

```python
"""A basic reusable agent"""

from typing import Annotated
from strands import Agent, tool

import conversion_agent
import trigonometry_agent
import arithmetic_agent

conversion_tools = [t.tool_name for t in conversion_agent.get_tools()]

@tool(description=f"Handles conversion requests including: {','.join(conversion_tools)}")
def do_conversion(request: Annotated[str, "The conversion request"]) -> str:
    """Conversion tool"""
    agent = conversion_agent.create_conversion_agent()
    result = agent(request)
    return result

trigonometry_tools = [t.tool_name for t in trigonometry_agent.get_tools()]

@tool(
    description=f"Handles trigonometry requests including: {','.join(trigonometry_tools)}. These functions all take values in radians."
)
def do_trigonometry(request: Annotated[str, "The trigonometry request"]) -> str:
    """Trigonometry tool"""
    agent = trigonometry_agent.create_trigonometry_agent()
    result = agent(request)
    return result

arithmetic_tools = [t.tool_name for t in arithmetic_agent.get_tools()]

@tool(description=f"Handles arithmetic requests including: {','.join(arithmetic_tools)}")
def do_arithmetic(request: Annotated[str, "The arithmetic request"]) -> str:
    """Arithmetic tool"""
    agent = arithmetic_agent.create_arithmetic_agent()
    result = agent(request)
    return result

def create_orchestrator_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(
        tools=[do_conversion, do_trigonometry, do_arithmetic], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    )
    return agent

```

 

### The CLI app

Finally we create **cli.py** to run the agent. We can pass it a `--prompt` parameter:

```python
"""Command line interface for the agent."""

import argparse
import orchestrator_agent

def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", help="The prompt to send to the agent.", required=True)
    return parser.parse_args()

def main(prompt: str):
    """Main logic for command line interface"""
    agent = orchestrator_agent.create_orchestrator_agent()

    agent(prompt)

if __name__ == "__main__":
    args = parse_args()
    main(args.prompt)

```

 

## Run the CLI app

We can now trigger a multi-step, multi-agent process with a single prompt:

```bash
python cli.py --prompt "What is the secant squared of 42 degrees?"
```

Will generate output similar to this:

```bash
I need to calculate the secant squared of 42 degrees. Since secant is 1/cosine, secant squared is 1/cosine squared.

First, let me convert 42 degrees to radians, then find the cosine, and finally calculate the secant squared.

Tool #1: do_conversion
Tool #1: degrees_to_radians
42 degrees is equal to approximately **0.733 radians** (or more precisely, 0.7330382858376184 radians).

Tool #2: do_trigonometry
Tool #1: cosine
The cosine of 0.7330382858376184 radians is approximately **0.7431448254773942**.

Tool #3: do_arithmetic
Tool #1: raise_to_power
The result of raising 0.7431448254773942 to the power of 2 is **0.5522642316338268**.

Tool #4: do_arithmetic
Tool #1: divide
The result of dividing 1 by 0.5522642316338268 is approximately **1.8107** (or more precisely, 1.8107274429879063).

The secant squared of 42 degrees is approximately **1.8107** (or more precisely, 1.8107274429879063).

```

In the above example, the orchestrator agent was able to correctly coordinate with the three sub-agents to solve the problem.

Note that we see different tool counters in effect. The "do\_..." tool calls increment from #1-#4, while each sub-agent runs independently and considers its own tool call to be #1.

Also note in the above code that we used Anthropic Claude Sonnet for the orchestrator, and Anthropic Claude Haiku for the sub-agents. This is just an example and not meant to be a specific recommendation. The LLM version didn't really matter in this case. In your use case you may find that a smaller model works fine for your orchestrator, but you might need more advanced models for your sub-agents if they are fairly sophisticated. Or you may find that an Amazon Nova or other LLM provider has better price/performance characteristics for a specific subset of tasks.





Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)
