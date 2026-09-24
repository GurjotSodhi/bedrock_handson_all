---
title : "Gateway: Client"
weight : 310
---


## Connecting to a Gateway

In the [MCP lab](/strands/intermediate-topics/mcp-local), the agent launched the MCP server as a local subprocess and communicated over stdio. AgentCore Gateway runs as a remote HTTP endpoint, so the client needs a different transport.

AgentCore Gateway endpoints are secured with authentication. The MCP specification's [authorization framework](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) is built around OAuth 2.1 for HTTP-based transports, but the spec also allows clients and servers to [negotiate custom authentication strategies](https://modelcontextprotocol.io/specification/2025-11-25/basic/index#auth). AgentCore Gateway supports both [OAuth and AWS IAM authorization](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-inbound-auth.html). In this lab we'll use IAM to keep things relatively simple. The [mcp-proxy-for-aws](https://github.com/aws/mcp-proxy-for-aws) package provides a Streamable HTTP transport that handles this, signing each request using your configured AWS credentials.

From the agent's perspective, the tools work the same way. The only difference is the transport layer and the tool naming convention. AgentCore Gateway prepends the target name to each tool name (e.g., `DemoLambdaTarget___cosine`) so agents can distinguish tools from different targets on the same gateway.

&nbsp;

## Connecting an agent to AgentCore Gateway

::::alert{type="info" header="Previous lab must be completed first"}
Please complete the [Gateway: Setup](../gateway-setup) lab before running this lab.

You'll need the `DEMO_GATEWAY_URL` environment variable set from that lab.
::::


&nbsp;

## Testing the gateway

In the workshop environment's terminal, change directory to `gateway-clients`:

```bash
cd /environment/workshop/agentic-labs/gateway-lambda/gateway-clients
```

Review the code in **basic_gateway_client.py**. It uses the `aws_iam_streamablehttp_client` function from `mcp-proxy-for-aws` to connect to the gateway's Streamable HTTP endpoint using IAM authentication.

In the workshop development environment terminal, run the following command:

```bash
python basic_gateway_client.py
```

This should generate a response similar to the following:

```text
I need to calculate the secant squared of 1.8237. The secant is the reciprocal of cosine, so sec²(x) = 1/cos²(x).

Let me break this down:
1. First, I'll calculate cos(1.8237)
2. Then I'll square that result
3. Finally, I'll divide 1 by the squared cosine

Let me start:
Tool #1: DemoLambdaTarget___cosine
Now I'll square this result:
Tool #2: DemoLambdaTarget___raise_to_power
Now I'll calculate 1 divided by this squared value:
Tool #3: DemoLambdaTarget___divide
The secant squared of 1.8237 is approximately **15.97**.
```

&nbsp;

## CLI chat app

Review the code in these files:

- **gateway_agent.py** creates a reusable agent with gateway-backed MCP tools. It includes a system prompt that tells the agent to respond using space raps.
- **cli_chat.py** runs an interactive command-line chat loop using the gateway agent

Run cli_chat.py to have an interactive conversation with your agent, powered by the AgentCore Gateway MCP server:

```bash
python cli_chat.py
```

Here is an example after entering `What is the secant squared of 1.2?`:

```text
🙂Me:
What is the secant squared of 1.2?

🤖Bot:
I need to calculate the secant squared of 1.2. The secant is 1/cos(x), so secant squared is 1/cos²(x).

Let me break this down:
1. Calculate cos(1.2)
2. Square it (multiply it by itself)
3. Divide 1 by that result

Let me do this step by step:
Tool #1: DemoLambdaTarget___cosine

Tool #2: DemoLambdaTarget___multiply

Tool #3: DemoLambdaTarget___divide
Yo, listen up, let me drop this cosmic fact,
Secant squared of one-point-two, that's mathematically exact,
First I found the cosine, floatin' in the spatial zone,
Then I squared it up and flipped it like a calculator phone,

**The answer's 7.616**, that's the secant squared you seek,
When angles twist through radians, that's the mathematics peak! 🚀

🙂Me:
bye
EXITING!!!
```

&nbsp;

## Tool count and context engineering

The demo gateway exposes 19 math tools, and the agent loads all of them into its context on every request. This has two potential downsides: Each tool definition consumes tokens in the model's context window, and models get worse at selecting the right tool as the list gets longer. Production gateways can expose dozens or hundreds of tools across multiple targets, making the load-everything approach impractical.

&nbsp;

## Next

In the next lab, we'll use AgentCore Gateway's semantic search to discover and load only the tools relevant to each request.
