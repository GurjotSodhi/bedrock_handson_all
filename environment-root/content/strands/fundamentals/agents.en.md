---
title: "Agents and agentic applications"
weight: 100
---

::::alert
This lab is based on the following article: [Understanding agents and agentic applications](https://builder.aws.com/content/38oL9fya9bzlvJYSVlgRqIWdGqn/understanding-agents-and-agentic-applications)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/agents**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/agents

```

## What is an agent?

Let's start with a [definition from AWS:](https://aws.amazon.com/what-is/ai-agents/)

> An artificial intelligence (AI) agent is a software program that can interact with its environment, collect data, and use that data to perform self-directed tasks that meet predetermined goals.

Simon Willison also offers this [concise definition:](https://simonwillison.net/2025/Sep/18/agents/)

> An LLM agent runs tools in a loop to achieve a goal.

What is the [meaning of "tool"](https://builder.aws.com/content/2hW5367isgQOkkXLYjp4JB3Pe16/intro-to-tool-use-with-the-amazon-bedrock-converse-api) in this case? A **tool** allows a large language model to tell the calling application to invoke a function with parameters supplied by the model.

Bringing the two definitions together, **tools** are the primary mechanism for an agent to **interact with its environment** and **collect data**. The **agent loop** is where the self-directed tasks are chosen that align with the goals.

 

## The agent loop

The **agent loop** is the iterative process through which an agent achieves a goal. This process is illustrated in the diagram below:


![Agentic workflow diagram showing how a large language model processes user prompts and context, requests tool execution from the application, receives tool results, and generates a final response in an iterative loop.](/static/images/agentic-fundamentals/agents/agent-loop.png)

The agent loop process is as follows:

1. A prompt and context are sent to an LLM. The context includes tools, a system prompt, and past messages.
2. Based on the input, the LLM determines if it should:
   * Request tool use to achieve the goal
   * Request more information (ends the agent loop for now)
   * Return a final result (ends the agent loop for now)
3. The application executes the requested tools, and sends the tool results to the LLM along with the context.
4. `GOTO 2`

This process can iterate multiple times as the agent progresses towards its goal. It may need to exit the loop to get user input or clarification, or exit due to an error.

[See the Strands Agents documentation for more on the agent loop](https://strandsagents.com/docs/user-guide/concepts/agents/agent-loop/)

 

## A simple example agent

Let's create a simple agent that demonstrates running tools in a loop. We'll use the [Strands Agents SDK](https://strandsagents.com/) with Python.

This example creates an agent with three math tools (sine, cosine, and divide) and a hard-coded prompt. No best practices, but good enough to get started:

Here is the code for **simple.py**. It requires the [strands-agents](https://pypi.org/project/strands-agents/) package to be installed, and AWS access:

```python
"""A simple agent demo"""

import math
from strands import Agent, tool

@tool
def cosine(x: float) -> float:
    return math.cos(x)

@tool
def sine(x: float) -> float:
    return math.sin(x)

@tool(description="Divide x by y")
def divide(x: float, y: float) -> float:
    return x / y

agent = Agent(tools=[cosine, sine, divide], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("What is the tangent of 8.12515? Provide accuracy to 5 places.")

```

Then we can run it from the command line:

```bash
python simple.py
```

With output that looks something like this:

```plaintext
I can calculate the tangent of 8.12515 using the relationship tan(x) = sin(x) / cos(x).
Let me compute both the sine and cosine of this value first.
Tool #1: sine

Tool #2: cosine
Now I'll divide sine by cosine to get the tangent:
Tool #3: divide
The tangent of 8.12515 is **-3.59691** (accurate to 5 decimal places).
```

### What just happened?

We asked the agent to calculate a tangent, but didn't give it a `tangent` tool. So it had to figure out another way to achieve its task (the trigonometric identity tan(x) = sin(x) / cos(x)). In this case, it did the work in two steps:

1. Calculate the sine and cosine values for `x`. These were invoked at the same time, since they have no dependency on each other.
2. Divide the sine value by the cosine value. This was invoked once the previous values were calculated.

 

### Mapping this example to the definitions of agent

Recall the first definition from earlier:

> An artificial intelligence (AI) agent is a software program that can interact with its environment, collect data, and use that data to perform self-directed tasks that meet predetermined goals.

* **a software program**: the `Agent` object instance
* **that can interact with its environment**: the `cosine`, `sine`, and `divide` tools
* **collect data**: the results from the `sine`, `cosine`, and `divide` tool calls
* **and use that data to perform self-directed tasks**: calculating the trigonometric identity for tangent
* **that meet predetermined goals**: calculating the tangent of 8.12515

Or the second definition:

> An LLM agent runs tools in a loop to achieve a goal.

* **An LLM agent**: the `Agent` object instance
* **runs tools**: the array of tools passed to the Agent() constructor
* **in a loop**: kicked off by invoking `agent()`
* **to achieve a goal**: calculating the tangent of 8.12515

Throughout this series, we'll expand on the use of tools and agent loops to achieve a wide variety of goals.

 

## What are agentic applications?

For the purpose of this series, we will be focusing on the building of "agentic applications".

**Agentic applications** combine deterministic (code-powered) and non-deterministic (AI-powered) components to solve problems that could not be solved by deterministic processes alone.

There is a spectrum of agentic applications, from almost entirely deterministic (workflows and applications with generative AI functions in isolation), to almost entirely non-deterministic (AI agents solving advanced problems as they see fit).

Much value will be found somewhere in between, with a combination of fast & cheap deterministic processes mixed with comparatively slow & expensive AI-powered processes. By "fast/slow" and "cheap/expensive", we are referring to run-time compute. In emerging use cases, solutions that tilt towards the AI-powered side may end up being less expensive overall due to the reduced development time and code complexity needed to solve more open-ended problems.

You will likely have experience building deterministic systems. The good news is that with the advent of LLMs and agentic frameworks like Strands Agents, we can interact with AI using the same API-based approaches that we have been using for years. Most of us know how to speak "API". So the real learning curve will be in how to speak "LLM". For our purposes that means:

* **Context engineering** - effectively curating the combined inputs to an LLM to efficiently get the desired outcome
* **Prompt engineering** - (really a sub-discipline of context engineering) - communicating intent and objectives effectively to an LLM (the "wordsmithing" aspects)
* **Tool definitions** - (really a sub-discipline of prompt engineering) - defining API signatures to help bridge the gap between non-deterministic and deterministic processes

Additionally, we will also discuss systems-related topics like session management, Model Context Protocol (MCP), and observability. These are critical for scaling agentic applications effectively.

 



## Learn more

* [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)
