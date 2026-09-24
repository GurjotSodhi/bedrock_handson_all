---
title : "Runtime: Client"
weight : 120
---


## Invoking AgentCore Runtime programmatically

::::alert{type="info" header="Previous lab must be completed first"}
Please complete the [Runtime: Deploy](../runtime-deploy) lab before running this lab.
::::

&nbsp;

## Get the agent ARN

First, we need to retrieve the [previously created Runtime ARN](../runtime-deploy), so we can invoke it programmatically.

In the workshop environment's terminal, change directory to `runtime-setup`:

```bash
cd /environment/workshop/agentic-labs/runtime-setup
```

This command retrieves the local agentcore runtime configuration, extracts the agent ARN, and saves it to the `RUNTIME_AGENT_ARN` environmental variable:

```bash
export RUNTIME_AGENT_ARN=$(python get_agent_arn.py)
echo $RUNTIME_AGENT_ARN
```

&nbsp;

## Creating a basic CLI runtime client application

In the workshop environment's terminal, change directory to `runtime-client`:

```bash
cd /environment/workshop/agentic-labs/runtime-client
```

In the **runtime-client** directory, review the following files:

- **math_client.py** is a client library that invokes the deployed AgentCore Runtime using the boto3 `bedrock-agentcore` SDK
- **cli.py** is a command-line wrapper that takes a prompt and optional session ID, calls math_client, and prints the response

Note the timeout and retry settings in **math_client.py**. Agent executions can run longer than the default boto3 timeouts, so the code sets `connect_timeout=120`, `read_timeout=3600`, and `total_max_attempts=1`. You'll want to configure these settings based on the expected duration of your agent execution and runtime startup time.

## Running the CLI client app

First, we'll try using our CLI client app without setting a session ID. Each call to our AgentCore Runtime application will create its own session and separate running instance.

### Running without setting a session ID

In the workshop development environment terminal, run the following command:

```bash
python cli.py --prompt "What is 11321 / 341?"
```

This should return output similar to this:

```bash
{
    "result": "11321 / 341 = **33.199413489736074** (or approximately **33.20**)\n",
    "session_id": "8b473ed3-d085-4b43-b352-7807e48a075e"
}
```

### Running again, creating an additional session

Running this will start a new session:

```bash
python cli.py --prompt "What did we just discuss?"
```

The agent in the new session won't know what we just discussed, since it is running from another container:

```bash
{
    "result": "We haven't discussed anything yet - this is the start of our conversation! I'm ready to help you with various tasks, including:\n\n- Calculating trigonometric functions (sine and cosine)\n- Division operations\n- Any other questions or tasks you'd like assistance with\n\nWhat would you like to discuss or work on?\n",
    "session_id": "f8b1166b-1f9a-4fe2-b8dc-bf1c48a01de7"
}
```


&nbsp;

### Passing the session ID

If we set the session ID, we can pass it to the CLI script to continue the conversation while the Runtime application is running. 

In the workshop development environment terminal, run the following commands:

```bash
DEMO_RUNTIME_SESSION_ID=$(uuidgen)
echo $DEMO_RUNTIME_SESSION_ID

python cli.py --prompt "Why is the sky blue? Answer in one sentence." --session-id $DEMO_RUNTIME_SESSION_ID
python cli.py --prompt "What did we just discuss?" --session-id $DEMO_RUNTIME_SESSION_ID
```

In this case, we can see that the conversation continues since it is invoking the same Runtime instance:

```bash
{
    "result": "The sky is blue because molecules in the atmosphere scatter shorter blue wavelengths of sunlight more efficiently than longer red wavelengths in a process called Rayleigh scattering.\n",
    "session_id": "990e5581-f73e-4be8-b04f-eb9078a50be6"
}
{
    "result": "We just discussed why the sky is blue - specifically, that it's due to Rayleigh scattering, where atmospheric molecules scatter shorter blue wavelengths of sunlight more efficiently than longer red wavelengths.\n",
    "session_id": "990e5581-f73e-4be8-b04f-eb9078a50be6"
}
```

The AgentCore Runtime session should live until its idle timeout is hit (default is 900 seconds / 15 minutes). We'll add memory in a later section to allow resumption of sessions after the idle timeout expires.

&nbsp;



## Streamlit client

The CLI application is nice for quick testing, but a web UI makes it easier to interact with the agent across multiple sessions. We'll use [Streamlit](https://docs.streamlit.io/develop/api-reference) to create a simple chatbot web application with Python.

&nbsp;

### Review the Streamlit app code

In the **runtime-client** directory, review the following files:

- **ui_demo_app.py** is the Streamlit UI that manages chat rendering and user input
- **ui_demo_logic.py** handles session and message logic, calling the same math_client we used in the CLI app

&nbsp;

### Running the Streamlit app

In the workshop development environment terminal, run the following command:

```bash
streamlit run ui_demo_app.py
```

In your workshop development environment, a popup should appear. In the popup, select **Open in Browser**.

![Screenshot of workshop dev environment, showing the application preview popup](/static/labs/code-preview.png)

&nbsp;

This should then launch the Streamlit app, which will look something like this:

![Screenshot of a chatbot web application titled 'Chatbot using AgentCore' with a session ID displayed. A user message reads 'Tell me about the ALF show' and the assistant responds with a detailed answer about the ALF TV show, including sections for 'Plot & Premise' and 'Main Characters', describing it as an American sitcom that aired from 1986 to 1990.](/static/images/agentcore/client/client-app.png)

The app is designed to create a unique AgentCore Runtime session per browser tab. Each session will have its own agent and local conversation history. For example, you can discuss _ALF_ in one tab, and _Mr. Belvedere_ in another. Each AgentCore Runtime session will end after 15 minutes of inactivity.

In the terminal, press Ctrl-C to exit the Streamlit app.

&nbsp;

## Next

In the next lab, we'll explore AgentCore Memory for persisting conversations across sessions.

&nbsp;
