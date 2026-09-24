---
title : "Gateway: Setup"
weight : 300
---


## AgentCore Gateway

AgentCore Gateway exposes backend services as MCP-compatible tools that agents can discover and invoke through a single endpoint. You register backend services as gateway targets with tool schemas. Agents connect to the gateway and use those tools through MCP.

In the [MCP lab](/strands/intermediate-topics/mcp-local), agents connected to a local MCP server over stdio. That works for development, but production agents need tools hosted as managed services with authentication, scaling, and centralized access. This is where AgentCore Gateway comes in.

Three concepts to understand before setting up a gateway:

**Targets** are the backend services behind a gateway. Each target maps to a set of tools. AgentCore Gateway [supports several target types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-supported-targets.html) including Lambda functions, OpenAPI specs, Smithy models, and existing MCP servers. It handles protocol translation between the agent's MCP requests and the target's native interface. An agent calls a tool through MCP, and AgentCore Gateway routes that call to the appropriate Lambda function or API endpoint.

**Authentication** works in two directions. [Inbound authentication](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-inbound-auth.html) verifies the agent's identity using IAM or OAuth. [Outbound authentication](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-outbound-auth.html) handles credentials for each target, so agents don't need to manage API keys or tokens for the services behind the gateway.

**Semantic search** is an optional feature that helps agents find relevant tools without loading all of them into context. When enabled, AgentCore Gateway adds a [search tool](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-using-mcp-semantic-search.html) that agents can query with natural language. This matters when a gateway has dozens or hundreds of tools across multiple targets, since loading all tool definitions into the model's [context window](https://builder.aws.com/content/38oLzpDYZJKUwbbKw3XyKD4Qjdd/introduction-to-context-engineering) wastes tokens and can degrade tool selection accuracy.

&nbsp;

## AgentCore Gateway with Lambda

In this lab, we'll take some local MCP tools and ultimately deploy them to an AgentCore Gateway backed by a Lambda function.

&nbsp;

## MCP Prototype

This is the same math MCP server from the previous lab, expanded from four tools to nineteen. The larger tool set gives us something more realistic to work with when we test semantic search on the gateway.

In the workshop environment's terminal, change directory to `mcp-prototype`:

```bash
cd /environment/workshop/agentic-labs/gateway-lambda/mcp-prototype
```

Review the code in **mcp_client.py**, then run it:

```bash
python mcp_client.py
```

This should generate a response similar to the following:

```text
I need to calculate the secant squared of 1.4. The secant is the reciprocal of cosine, so sec²(x) = 1/cos²(x).

Let me first calculate the cosine of 1.4 (assuming this is in radians):
Tool #1: cosine
Now I'll square this cosine value:
Tool #2: raise_to_power
Finally, I'll calculate the reciprocal (1 divided by cos²(1.4)) to get sec²(1.4):
Tool #3: divide
The secant squared of 1.4 (radians) is approximately **34.62**.
```

&nbsp;

## Preparing local tools for AgentCore Gateway

To move from a local MCP server to an AgentCore Gateway, we need to generate tool specs, set up a Lambda function, and create the gateway.

&nbsp;

### Generating tool specs

Review the code for **generate_mcp_tool_schema.py**. This script extracts tool definitions from the FastMCP-decorated functions and writes them as JSON. It filters out non-standard keys like `x-fastmcp-wrap-result` that FastMCP adds to its output schemas.

In the workshop development environment terminal, run the following command:

```bash
python generate_mcp_tool_schema.py
```

This saves a **tool_specs.json** file to the **mcp-prototype** directory. We'll use this later to configure the AgentCore Gateway Lambda target.

&nbsp;

### Configuring the Lambda function

Now we create a Lambda function based on the local MCP prototype. The code is in the **lambda-setup** directory.

```bash
cd /environment/workshop/agentic-labs/gateway-lambda/lambda-setup
```

- **math_tool_functions.py** has the same tool functions as the MCP prototype, but without `@mcp.tool` decorators. AgentCore Gateway sits in front of the Lambda and handles MCP on its behalf, so the Lambda is just plain Python.
- **lambda_function.py** is the Lambda handler. AgentCore Gateway passes the tool name in the Lambda client context using the format `targetName___toolName`. The handler splits on `___`, looks up the matching function in `math_tool_functions`, and calls it with the event payload as keyword arguments.
- **create_lambda_function.py** creates the Lambda function in your AWS account. It creates a function named **DemoToolLambda** using the **DemoToolLambdaRole** IAM role that was created during workshop setup.

In the workshop development environment terminal, run the following command:

```bash
python create_lambda_function.py
```

&nbsp;

### Creating the gateway

Now we'll create an AgentCore Gateway with a target pointing to the Lambda function.

In the workshop environment's terminal, change directory to `gateway-setup`:

```bash
cd /environment/workshop/agentic-labs/gateway-lambda/gateway-setup
```

Review the code in **create_gateway.py**. The script does two things:

1. Creates a gateway named **DemoGateway** using the `create_gateway` API with `AWS_IAM` as the authorizer type and `SEMANTIC` search enabled. The gateway uses the **DemoGatewayRole** IAM role created during workshop setup. It polls until the gateway status is `READY`.
2. Creates a Lambda target named **DemoLambdaTarget** on the gateway. The target points to the **DemoToolLambda** function and includes the tool schemas from **tool_specs.json** (generated in the previous step). AgentCore Gateway uses these schemas to expose the Lambda function's operations as MCP tools. The target uses `GATEWAY_IAM_ROLE` as its credential provider, meaning the gateway's own execution role is what invokes the Lambda.

Run the following command to create the AgentCore Gateway with a Lambda target:

```bash
python create_gateway.py
```

This will output the gateway ID and an `export` command to copy and run.

Example output:

```text
Creating gateway
Gateway Ready!
Gateway ID: demogateway-aaaaa
Gateway URL: https://demogateway-aaaaa.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp
Please copy and run this command to configure your Gateway clients:
export DEMO_GATEWAY_URL=...
```

Copy the export command from your terminal output and run it, so the gateway URL is available for the next lab.

&nbsp;

## Next

In the next lab, we'll connect a Strands agent to this gateway and invoke the Lambda-backed tools.
