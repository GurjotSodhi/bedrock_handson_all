"""Client library for accessing the math runtime agent"""

import os
import json

import boto3

from botocore.config import Config


def invoke_agentcore_runtime(prompt: str, session_id: str):
    """Invoke the agentcore runtime with the given prompt and session ID."""

    # Always set a Config object for your AgentCore Runtime connections.
    # Since the normal read timeout is 60 seconds, it's really common to see confusion
    # when agents get restarted in the middle of a minutes-long process.
    # So get in the habit of setting your retry and timeout settings now.
    # The below settings are fine for this example. Base your settings on the expected
    # duration of your agent execution, runtime startup time, and retry requirements.
    # https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
    agentcore_boto_config = Config(
        retries={
            "total_max_attempts": 1,  # Only attempt the call once
        },
        connect_timeout=120,  # Allow 120 seconds for initial connection
        read_timeout=3600,  # Give agent 60 minutes to run
    )

    client = boto3.client("bedrock-agentcore", region_name="us-west-2", config=agentcore_boto_config)
    payload = json.dumps({"prompt": prompt})

    agent_runtime_arn = os.getenv("RUNTIME_AGENT_ARN")

    if not agent_runtime_arn:
        raise ValueError("Please set the environment variable RUNTIME_AGENT_ARN.")

    response = client.invoke_agent_runtime(
        agentRuntimeArn=agent_runtime_arn, runtimeSessionId=session_id, payload=payload
    )
    response_body = response["response"].read()
    response_data = json.loads(response_body)

    return response_data
