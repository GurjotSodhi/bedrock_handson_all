"""The main agentcore app"""

from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.runtime.context import RequestContext

import math_memory_agent

app = BedrockAgentCoreApp()

_agent = None  # We can't instantiate this Runtime session's agent until the calling app gives us our session ID


def get_or_initialize_agent(session_id: str, actor_id: str):
    """Initializes the agent on first use for a session,
    or retrieves the agent for subsequent sessions."""
    global _agent
    if not _agent:
        _agent = math_memory_agent.create_agent(session_id=session_id, actor_id=actor_id)

    return _agent


@app.entrypoint
def invoke(payload, context: RequestContext):
    """Entrypoint for the agentcore app"""
    prompt = payload.get("prompt", "Tell the user they forgot to pass a JSON dict with a prompt attribute.")

    # This is a bit of a hack since we're not using oauth here.
    # we are trusting the caller to identify the actor.
    # If sensitive user data is accessed, we should be using proper oauth
    # or other appropriate controls.
    # See commentary under "Important Notes on Actor ID and Session Management" here:
    # https://github.com/awslabs/agentcore-samples/blob/main/06-workshops/04-AgentCore-memory/03-advanced-patterns/02-memory-runtime-integration/runtime_memory_integration.ipynb
    actor_id = payload.get("actor_id")

    if actor_id is None:
        raise KeyError("Please provide a value for actor_id")

    agent = get_or_initialize_agent(session_id=context.session_id, actor_id=actor_id)

    result = agent(prompt)

    return {"result": str(result), "session_id": context.session_id}


if __name__ == "__main__":
    app.run()
