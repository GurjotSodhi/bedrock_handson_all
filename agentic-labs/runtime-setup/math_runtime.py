"""The main agentcore app"""

import argparse

from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.runtime.context import RequestContext

import math_agent

app = BedrockAgentCoreApp()

_agent = None  # We can't instantiate this until the calling app gives us our session ID


def get_or_initialize_agent(session_id: str):
    """Initializes the agent on first use for a new AgentCore Runtime session,
    or retrieves the agent for subsequent AgentCore Runtime sessions."""
    global _agent
    if not _agent:
        _agent = math_agent.create_agent(session_id=session_id)

    return _agent


@app.entrypoint
def invoke(payload, context: RequestContext):
    """Entrypoint for the agentcore app"""
    prompt = payload.get("prompt", "Tell the user they forgot to pass a JSON dict with a prompt attribute.")

    agent = get_or_initialize_agent(context.session_id)

    result = agent(prompt)

    return {"result": str(result), "session_id": context.session_id}


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo-port", type=int, help="The port to use for demoing directly.", required=False)
    return parser.parse_args()


if __name__ == "__main__":
    # app.run() defaults to running on port 8080.
    # In the workshop environment, we need to run it on another port by default,
    # since the development environment takes port 8080
    args = parse_args()
    if args.demo_port:
        app.run(port=args.demo_port)
    else:
        app.run()
