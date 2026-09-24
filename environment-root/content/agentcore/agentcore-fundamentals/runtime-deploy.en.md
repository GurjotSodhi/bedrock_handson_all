---
title : "Runtime: Deploy"
weight : 110
---


## Deploying and testing an AgentCore Runtime application

In the previous lab, we ran our math agent locally using both Python and the `agentcore` CLI. Now we'll deploy it to AWS and interact with it as a hosted service.

In the workshop environment's terminal, change directory to `runtime-setup`:

```bash
cd /environment/workshop/agentic-labs/runtime-setup
```

## Configure your Runtime application

If you didn't complete the previous lab, run the following command to configure AgentCore Runtime. This is safe to run again if you've already done it.

Accept the defaults for each item in the configuration:

```bash
agentcore configure --entrypoint math_runtime.py --disable-memory
```

The `--disable-memory` flag skips memory configuration. We'll add AgentCore Memory in a later lab.

&nbsp;

## Deploy the Runtime

Deploy the agent to AgentCore Runtime:

```bash
agentcore deploy
```

This packages your agent code, uploads it, and provisions the runtime infrastructure. After about a minute, you'll see the details of your deployed application, including its ARN and endpoint information.

&nbsp;

## Review the Runtime application in the AWS Console

In the AWS Console, search for `AgentCore`. You'll find the **math_runtime** application listed in the **Runtime** section. From here you can view the application's configuration, endpoints, and status.

&nbsp;

## Check Runtime status

Use `agentcore status` to confirm the deployment and review your application's settings from the command line:

```bash
agentcore status
```

&nbsp;

## Invoke the Runtime

With the agent deployed, we can send it requests using `agentcore invoke`.

### Create a session ID

First, create a session ID. We'll reuse this across multiple invocations to maintain a conversation.

```bash
export DEMO_SESSION_ID=$(uuidgen)
echo DEMO_SESSION_ID: $DEMO_SESSION_ID
```

Send a request to the deployed agent:

```bash
agentcore invoke '{"prompt":"what is the sine of 1.1"}' --session-id $DEMO_SESSION_ID
```


### Conversation continuity

Because the Strands `agent` object stays in memory on the runtime instance, we can carry on the conversation over multiple turns. The session lives until its idle timeout is reached (default: 900 seconds / 15 minutes).

Send a few more requests using the same session ID:

```bash
agentcore invoke '{"prompt":"what is the cos of 1.1?"}' --session-id $DEMO_SESSION_ID
```

```bash
agentcore invoke '{"prompt":"what is tangent of 1.1?"}' --session-id $DEMO_SESSION_ID
```

Now ask the agent what it remembers:

```bash
agentcore invoke '{"prompt":"what have we discussed so far?"}' --session-id $DEMO_SESSION_ID
```

Because the session is still active, the agent remembers the full conversation:

```json
{
  "result": "So far, we've discussed the trigonometric functions of the angle 1.1 radians:\n\n1. **Sine of 1.1**: approximately 0.8912\n2. **Cosine of 1.1**: approximately 0.4536\n3. **Tangent of 1.1**: approximately 1.9648\n\nFor the tangent, I calculated it by dividing the sine by the cosine (since tan(x) = sin(x) / cos(x)).\n",
  "session_id": "56585205-cd47-469b-af78-672b30885bb1"
}
```

This works because the runtime keeps the agent process and its message history alive between invocations within the same session.

&nbsp;

## What happens when a session ends

After 15 minutes of inactivity, the runtime shuts down the agent process and the in-memory conversation history is lost. We can also end a session explicitly using the `stop-session` command:

```bash
agentcore stop-session --session-id $DEMO_SESSION_ID
```

Now invoke the agent again with the same session ID:

```bash
agentcore invoke '{"prompt":"What have we discussed so far?"}' --session-id $DEMO_SESSION_ID
```

The agent has no memory of the previous conversation:

```json
{
  "result": "We haven't discussed anything yet - this is the start of our conversation! This is the first message you've sent me.\n\nI'm here to help you with various tasks. I have access to several mathematical functions:\n- **Sine** - calculates the sine of a value (in radians)\n- **Cosine** - calculates the cosine of a value (in radians)\n- **Divide** - divides one number by another\n\nFeel free to ask me questions, request calculations, or let me know what you'd like help with!\n",
  "session_id": "56585205-cd47-469b-af78-672b30885bb1"
}
```

This is the key limitation of in-memory sessions: once the process stops, the conversation starts over from scratch. In a later lab, we'll add AgentCore Memory to persist conversation history. This will allow continuity of a session, even if the Runtime is stopped or crashes.

&nbsp;

## Observability

[AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) provides observability capabilities for Amazon Bedrock AgentCore through Amazon Cloudwatch. During development, here are two ways you can use AgentCore Observability:

### From the command line

The `agentcore invoke` response includes log-related commands in its output. Copy and run the command ending with `--since 1h` to review logs for your recent invocations.

### From the AWS Console

Navigate to **AWS Console → AgentCore → Runtime → math_runtime → Endpoints**. Under the **CloudWatch** column, click **Logs** to view invocation logs.

&nbsp;

## Next

In the next lab, we'll invoke the runtime programmatically from a Python client.
