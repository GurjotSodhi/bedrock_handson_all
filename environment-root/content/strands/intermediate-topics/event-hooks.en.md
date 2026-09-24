---
title: "Event hooks"
weight: 400
---


::::alert
This lab is based on the following article: [Event hooks with Strands Agents](https://builder.aws.com/content/38oNuNrc3NaC0EIRulQtTH9055Z/event-hooks-with-strands-agents)
::::



In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/event-hooks**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/event-hooks

```





## Event handling in Strands Agents

Strands Agents offers two different ways to handle events during the agent lifecycle, **callback handlers** and **hooks**.

 

## Callback handlers

**Callback handlers** can act as a catch-all for events during the agent lifecycle. You can [learn more about callback handlers in the Strands Agents user guide](https://strandsagents.com/docs/user-guide/concepts/streaming/callback-handlers/).

 

## Hooks

**Hooks** support subscribing to specific events during the agent lifecycle. You can [learn more about hooks in the Strands Agents user guide](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/).

In this series, we will be focusing on the ability to extend Strands tool use capabilities using its tool-related event hooks. We will use `BeforeToolCallEvent` and `AfterToolCallEvent` in several scenarios.

**BeforeToolCallEvent** is triggered before a tool is called. You can use this event to cancel a tool, limit the number of tool calls made by an agent, transform tool call parameters, and record tool call parameters. [Learn more about BeforeToolCallEvent specifics in the API reference documentation](https://strandsagents.com/docs/api/python/strands.hooks.events/#strands.hooks.events.BeforeToolCallEvent).

**AfterToolCallEvent** is triggered after a tool returns its result. You can use this event to transform the result and record tool call results. [Learn more about AfterToolCallEvent specifics in the API reference documentation](https://strandsagents.com/docs/api/python/strands.hooks.events/#strands.hooks.events.AfterToolCallEvent).

 

## Code examples

The examples below require that the [strands-agents](https://pypi.org/project/strands-agents/) package is installed, and AWS access.

 

## Tool call recorder

One common scenario is the need to collect the tool call parameters and/or results from an agent invocation. This can help us update a user interface after an invocation, capture a structured record of work performed, or support structured output-like scenarios but with more than one possible output format.

This hook provider can optionally capture each tool request in a "tool\_requests" list, and each tool result in a "tool\_results" list. These are then accessible from the invocation result's `state` property.

Hook provider definition, in **tool\_call\_recorder.py**:

```python
from threading import Lock
from typing import Any

from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent, HookProvider, HookRegistry

class ToolCallRecorderHookProvider(HookProvider):
    """Conditionally records tool use requests and results and makes them available in AgentResult.state"""

    def __init__(self, record_requests: bool = False, record_results: bool = False):
        self.record_requests = record_requests
        self.record_results = record_results
        self._lock = Lock()

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        if self.record_requests:
            registry.add_callback(BeforeToolCallEvent, self.before_tool_hook)
        if self.record_results:
            registry.add_callback(AfterToolCallEvent, self.after_tool_hook)

    def before_tool_hook(self, event: BeforeToolCallEvent) -> None:
        """Records all tool use requests in "tool_requests" in the AgentResult's "state" property"""
        with self._lock:
            req_state = event.invocation_state.setdefault("request_state", {})  # this should already exist
            tool_requests = req_state.setdefault("tool_requests", [])
            tool_requests.append(event.tool_use)

    def after_tool_hook(self, event: AfterToolCallEvent) -> None:
        """Records all tool results in "tool_results" in the AgentResult's "state" property"""
        with self._lock:
            req_state = event.invocation_state.setdefault("request_state", {})  # this should already exist
            tool_results = req_state.setdefault("tool_results", [])
            tool_results.append(event.result)

```

Example usage in **recorder\_test.py:**

```python
"""Tool tracking demo"""

import json
import math
from typing import Annotated

from strands import Agent, tool

from tool_call_recorder import ToolCallRecorderHookProvider

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

agent = Agent(
    tools=[cosine, sine, divide],
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    hooks=[ToolCallRecorderHookProvider(record_requests=True, record_results=True)],
)

print("-" * 40)
print("Round 1")
r1 = agent("What is the tangent of 1.11122? Provide accuracy to 5 places.")
print("-" * 40)
print(json.dumps(r1.state.get("tool_requests", []), indent=4))  # only shows tool requests from the first invocation
print("-" * 40)
print(json.dumps(r1.state.get("tool_results", []), indent=4))  # only shows tool results from the first invocation

print("-" * 40)
print("Round 2")
print("-" * 40)
r2 = agent("What is the cotangent?")
print("-" * 40)
print(json.dumps(r2.state.get("tool_requests", []), indent=4))  # only shows tool requests from the second invocation
print("-" * 40)
print(json.dumps(r2.state.get("tool_results", []), indent=4))  # only shows tool results from the second invocation

```

Running **recorder\_test.py** will allow you to see the tool requests and results after each agent invocation.

### Round 1 tool requests

In round 1, we ask the agent to solve "What is the tangent of 1.11122? Provide accuracy to 5 places."

These are the two parallel calls to `sine` and `cosine`, followed by the call to `divide` using their results:

```json
[
    {
        "toolUseId": "tooluse_Rp-o6ZAESkasoTpn-ozpHQ",
        "name": "sine",
        "input": {
            "x": 1.11122
        }
    },
    {
        "toolUseId": "tooluse_xVsmoYtTTDyfsogO4I8v0w",
        "name": "cosine",
        "input": {
            "x": 1.11122
        }
    },
    {
        "toolUseId": "tooluse_0BtH0uAXRZOOZiqC94zQOw",
        "name": "divide",
        "input": {
            "x": 0.8962405060170204,
            "y": 0.4435684336991928
        }
    }
]
```

### Round 1 tool results

These are results from `sine` , `cosine`, and `divide` :

```json
[
    {
        "toolUseId": "tooluse_Rp-o6ZAESkasoTpn-ozpHQ",
        "status": "success",
        "content": [
            {
                "text": "0.8962405060170204"
            }
        ]
    },
    {
        "toolUseId": "tooluse_xVsmoYtTTDyfsogO4I8v0w",
        "status": "success",
        "content": [
            {
                "text": "0.4435684336991928"
            }
        ]
    },
    {
        "toolUseId": "tooluse_0BtH0uAXRZOOZiqC94zQOw",
        "status": "success",
        "content": [
            {
                "text": "2.0205236394815427"
            }
        ]
    }
]
```

### Round 2 tool requests

In round 2, we ask the agent to solve "What is the cotangent?". Note that the agent is able to use the output from the previous messages, but the round 2 invocation result's state property just includes the new tool calls.

```json
[
    {
        "toolUseId": "tooluse_NDgOptrLQ2aPim9wCuZffQ",
        "name": "divide",
        "input": {
            "x": 1,
            "y": 2.0205236394815427
        }
    }
]
```

### Round 2 tool results

Here is the tool result for the divide operation used to invert the tangent into the cotangent:

```json
[
    {
        "toolUseId": "tooluse_NDgOptrLQ2aPim9wCuZffQ",
        "status": "success",
        "content": [
            {
                "text": "0.4949212077798781"
            }
        ]
    }
]
```

This is just one possible use of hooks with Strands Agents. They are a great way to extend and customize agent behavior to meet the needs of your application.

## Additional examples

You can find some [more hook examples in the Strands Agents user guide](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/).



Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)