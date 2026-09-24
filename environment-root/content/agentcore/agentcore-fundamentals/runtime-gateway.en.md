---
title : "Gateway + Runtime"
weight : 350
---


## Deploying a gateway agent to AgentCore Runtime

In this lab, we'll connect AgentCore Runtime and AgentCore Gateway. We'll deploy an agent that connects via MCP to the gateway to access Lambda-backed tools.


::::alert{type="info" header="Previous lab must be completed first"}
Please complete the [Gateway: Setup](../gateway-setup) lab before running this lab.

You'll need the `DEMO_GATEWAY_URL` environment variable set from that lab.
::::


&nbsp;

## Review the code for the lab

In the workshop environment's terminal, change directory to `runtime-gateway`:

```bash
cd /environment/workshop/agentic-labs/runtime-gateway
```

Review the code in these files:

- **math_gateway_agent.py** creates an MCP client connected to the gateway using IAM authentication and builds an agent using the gateway-backed tools
- **math_gateway_runtime.py** is the runtime entrypoint that initializes the MCP client at startup and routes requests to the gateway agent
- **requirements.txt** lists dependencies including `mcp-proxy-for-aws` for gateway connectivity

&nbsp;

## Configure and deploy the runtime

The `--execution-role` flag uses the **DemoRuntimeRole** IAM role that was created during workshop setup. The `AWS_ACCOUNTID` environment variable is workshop-specific. The `--disable-memory` flag skips memory configuration.

Accept the defaults for the wizard:

```bash
agentcore configure --entrypoint math_gateway_runtime.py --execution-role arn:aws:iam::${AWS_ACCOUNTID}:role/DemoRuntimeRole --disable-memory
```

Deploy the runtime. The `--env` flag passes the gateway URL as an environment variable to the deployed runtime, so the agent code can connect to the gateway endpoint:

```bash
agentcore deploy --env DEMO_GATEWAY_URL=$DEMO_GATEWAY_URL
```

&nbsp;

## Check runtime status

Use `agentcore status` to confirm the deployment and review settings:

```bash
agentcore status
```

&nbsp;

## Invoke the runtime

Create a session ID:

```bash
export DEMO_SESSION_ID=$(uuidgen)
echo DEMO_SESSION_ID: $DEMO_SESSION_ID
```

Send a request to the deployed agent:

```bash
agentcore invoke '{"prompt":"what is the secant squared of 32 degrees? Then tell me how you solved the problem, including tools used."}' --session-id $DEMO_SESSION_ID
```

This should generate a response similar to the following:

```json
{
  "result": "**Answer: The secant squared of 32 degrees is approximately 1.3905**\n\n## How I solved the problem:\n\n**Tools used:**\n1. **degrees_to_radians**: Converted 32° to 0.5585 radians (since trigonometric functions work with radians)\n2. **cosine**: Calculated cos(0.5585) = 0.8480\n3. **raise_to_power**: Squared the cosine value: (0.8480)² = 0.7192\n4. **divide**: Calculated secant squared using the identity sec²(x) = 1/cos²(x): 1 ÷ 0.7192 = 1.3905\n\n**Mathematical relationship:**\n- Secant is the reciprocal of cosine: sec(x) = 1/cos(x)\n- Therefore: sec²(x) = 1/cos²(x)\n",
  "session_id": "f323da04-816b-4518-9886-906df5063fa1"
}
```

The agent used four tools (`degrees_to_radians`, `cosine`, `raise_to_power`, `divide`) exposed through the gateway's Lambda target.

&nbsp;

## Learn more

See the [AgentCore Gateway documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) for more on configuring targets, authentication, and tool schemas.
