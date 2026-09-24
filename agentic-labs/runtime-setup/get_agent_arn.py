"""Get the Bedrock AgentCore Runtime ARN from the local configuration file."""

import yaml

# Load the YAML file
with open(".bedrock_agentcore.yaml", "r") as file:
    data = yaml.safe_load(file)

# Access nested values using dictionary keys
agent_arn = data["agents"]["math_runtime"]["bedrock_agentcore"]["agent_arn"]

print(agent_arn)
