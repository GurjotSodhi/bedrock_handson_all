---
title : "Runtime: Setup"
weight : 100
---


## Setting up AgentCore Runtime and running locally

AgentCore Runtime lets you run agents locally during development before deploying to AWS. The runtime server can be started directly from Python or through the `agentcore` CLI, which provides a deployment-like experience on your machine.

&nbsp;

## Review the code for the lab

The code below has the following dependencies. These have been automatically installed for you in your workshop development environment:

* [bedrock-agentcore-starter-toolkit](https://pypi.org/project/bedrock-agentcore-starter-toolkit/)
* [strands-agents](https://pypi.org/project/strands-agents/)

In the workshop environment's terminal, change directory to `runtime-setup`:

```bash
cd /environment/workshop/agentic-labs/runtime-setup
```

In the **runtime-setup** directory, you can review the following files. The code follows a layered pattern: tools are defined separately, the agent wires them together, and the runtime exposes the agent as a service.

- **math_tools.py** contains tool definitions for the agent, including sine, cosine, and division
- **math_agent.py** configures the agent with access to the math tools
- **math_runtime.py** is the runtime entrypoint that receives requests and routes them to the agent
- **requirements.txt** lists dependencies for the deployed AgentCore Runtime application

&nbsp;

## Running an AgentCore Runtime application from Python

We can run the AgentCore Runtime application locally as a Python script.

### Start the Python application

Run the following command to start the runtime server on port 8081. We need to use port 8081 because the workshop development environment claims port 8080.

```bash
python math_runtime.py --demo-port 8081
```

&nbsp;

### Invoke the Python application

In a separate terminal in your workshop development environment, send a request to the agent:

```bash
curl -X POST http://localhost:8081/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the tangent of 3.1?"}'
```

The curl response will show the agent's final answer. The `session_id` is null because we didn't pass one in the request. The direct Python approach doesn't manage sessions automatically.

```json
{"result": "The tangent of 3.1 radians is approximately **-0.0416**.\n", "session_id": null}
```

In the terminal running the Python script, you'll see the agent's reasoning and tool calls:

```bash
I'll calculate the tangent of 3.1 radians by computing sine(3.1) / cosine(3.1).
Tool #1: sine

Tool #2: cosine
Now I'll divide the sine by the cosine:
Tool #3: divide
{"timestamp": "2026-02-22T14:12:16.728Z", "level": "INFO", "message": "Invocation completed successfully (4.849s)", "logger": "bedrock_agentcore.app", "requestId": "31c53f9e-47f8-4da5-9e58-afbfe3a876da"}
```

Press Control-C in the original terminal window to exit the running **math_runtime.py** script.

&nbsp;

## Configuring and testing your Runtime application with the AgentCore Starter Toolkit CLI

The `agentcore` CLI provides a deployment-like experience locally. First, configure your agent using the [AgentCore Starter Toolkit CLI](https://aws.github.io/bedrock-agentcore-starter-toolkit/api-reference/cli.html).

### Configure your AgentCore Runtime application

Accept the defaults for each step in the configuration wizard:

```bash
agentcore configure --entrypoint math_runtime.py --disable-memory
```

This creates a local `.bedrock_agentcore` directory and a `.bedrock_agentcore.yaml` configuration file.

&nbsp;

### Start the development server

This will also run on port 8081, since port 8080 is claimed by the development environment:

```bash
agentcore dev
```

&nbsp;

### Invoke the development server

In a separate terminal in your workshop development environment, invoke the agent on port 8081:

```bash
agentcore invoke --dev '{"prompt": "What is the tangent of 1.13?"}' --port 8081
```

The response will appear in your terminal:

```bash
✓ Response from dev server:
{'response': '{"result": "The tangent of 1.13 radians is approximately **2.1198**.\\n", "session_id": "c1fa4c3a-a03a-4113-b4cc-4feb73091fa0"}'}
```

In the terminal where the dev server is running, you'll see the agent's execution trace:

```bash
I need to calculate the tangent of 1.13 radians. The tangent function is defined as tan(x) = sin(x) / cos(x), so I'll calculate both the sine and cosine of 1.13, then divide them.
Tool #1: sine

Tool #2: cosine
Now I'll divide the sine by the cosine to get the tangent:
Tool #3: divide
{"timestamp": "2026-02-22T14:21:07.859Z", "level": "INFO", "message": "Invocation completed successfully (3.771s)", "logger": "bedrock_agentcore.app", "requestId": "8ccdd185-9004-41a2-9a55-2942e81b48e8", "sessionId": "c1fa4c3a-a03a-4113-b4cc-4feb73091fa0"}
The tangent of 1.13 radians is approximately **2.1198**.
```

For more configuration options, see the [CLI reference](https://aws.github.io/bedrock-agentcore-starter-toolkit/api-reference/cli.html).

&nbsp;

## Next

In the next lab, we'll deploy the runtime agent to AWS.

