---
title : "Gateway: Search"
weight : 320
---


## Semantic tool search with AgentCore Gateway


When a gateway has many targets with many tools, loading them all into an agent's context has costs. Each tool definition consumes tokens in the model's context window, and models can struggle to select the right tool when presented with too many options. For a gateway with a handful of math tools this isn't a problem, but production gateways can have dozens or hundreds of tools across multiple targets.

AgentCore Gateway's semantic search addresses this. When you enable semantic search during gateway creation (as we did in the setup lab with `"searchType": "SEMANTIC"`), AgentCore Gateway adds a built-in tool called `x_amz_bedrock_agentcore_search`. An agent can call this tool with a natural language query, and the gateway returns the tools most relevant to that query. The agent then registers only those tools and uses them to handle the request.

::::alert{type="info" header="Previous lab must be completed first"}
Please complete the [Gateway: Setup](../gateway-setup) lab before running this lab.

You'll need the `DEMO_GATEWAY_URL` environment variable set from that lab.
::::

In the example below, the agent starts with a single tool, `find_and_add_tools`, and uses it to search the gateway for relevant tools on demand.


&nbsp;

## Review the code for the lab

In the workshop environment's terminal, change directory to `gateway-search`:

```bash
cd /environment/workshop/agentic-labs/gateway-lambda/gateway-search
```

Review the code in these files:

- **gateway_search_agent.py** wraps a Strands agent with a `find_and_add_tools` tool that performs semantic search against the gateway and registers matching tools at runtime. The agent starts with no math tools and discovers them as needed.
- **cli_search_chat.py** is an interactive chat loop using the search agent

&nbsp;

## Run the chat

In the workshop development environment terminal, run the following command:

```bash
python cli_search_chat.py
```

Try submitting a multi-step math problem. Below is a response to the question `What is the secant squared of 82 degrees?`:

```text
🙂Me:
What is the secant squared of 82 degrees?

🤖Bot:
I need to find the secant squared of 82 degrees. Let me start by finding the appropriate tools for this calculation.
Tool #1: find_and_add_tools
tool_to_find: trigonometric functions secant cosine sine
The following additional tools have been made available to you: DemoLambdaTarget___cosine, DemoLambdaTarget___sine, DemoLambdaTarget___tangent, DemoLambdaTarget___cube_root, DemoLambdaTarget___degrees_to_radians
Good! Now I need to:
1. Convert 82 degrees to radians
2. Find the cosine of that value
3. Square the cosine result
4. Take the reciprocal (since secant = 1/cosine, so secant² = 1/cosine²)

Let me find tools for division and squaring:
Tool #2: find_and_add_tools
tool_to_find: division divide reciprocal
The following additional tools have been made available to you: DemoLambdaTarget___divide, DemoLambdaTarget___square_root, DemoLambdaTarget___subtract, DemoLambdaTarget___multiply
Perfect! Now let me start the calculation:
Tool #3: DemoLambdaTarget___degrees_to_radians
Now I'll find the cosine of 82 degrees (1.4311699866353502 radians):
Tool #4: DemoLambdaTarget___cosine
Now I need to square this cosine value (multiply it by itself):
Tool #5: DemoLambdaTarget___multiply
Finally, I'll calculate secant² = 1/cos²:
Tool #6: DemoLambdaTarget___divide
The secant squared of 82 degrees is approximately **51.63**.
```

For simple math tools, the search-then-use pattern adds overhead. Each search is an extra round trip to the model and an extra call to the gateway's search API, and the agent may need to search more than once if the first results don't cover everything it needs. But for agents working across large tool catalogs where the full set of needed tools isn't known at development time, dynamic discovery keeps the context focused and the agent flexible.

&nbsp;

## Next

In the next lab, we'll deploy an agent that uses AgentCore Gateway to AgentCore Runtime.
