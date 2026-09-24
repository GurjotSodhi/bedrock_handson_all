"""The main agentcore app"""

from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.runtime.context import RequestContext

import math_gateway_agent


mcp_client = math_gateway_agent.create_mcp_client()

app = BedrockAgentCoreApp()

_agent = None  # We can't instantiate this until the calling app gives us our session ID


def get_or_initialize_agent(session_id: str):
    """Initializes the agent on first use for a session,
    or retrieves the agent for subsequent sessions."""
    global _agent
    if not _agent:
        _agent = math_gateway_agent.create_agent(mcp_client=mcp_client, session_id=session_id)

    return _agent


@app.entrypoint
def invoke(payload, context: RequestContext):
    """Entrypoint for the agentcore app"""
    prompt = payload.get("prompt", "Tell the user they forgot to pass a JSON dict with a prompt attribute.")

    agent = get_or_initialize_agent(session_id=context.session_id)

    result = agent(prompt)

    return {"result": str(result), "session_id": context.session_id}


if __name__ == "__main__":
    app.run()
