"""Script for creating an AgentCore Gateway"""

import json
import time
import boto3


def create_gateway(
    region: str,
    account_id: str,
) -> str:
    """Creates an AgentCore Gateway"""

    agentcore_client = boto3.client("bedrock-agentcore-control", region_name=region, aws_account_id=account_id)

    # This role is automatically created during Workshop environment setup
    gateway_role_arn = f"arn:aws:iam::{account_id}:role/DemoGatewayRole"

    print("Creating gateway")

    gateway = agentcore_client.create_gateway(
        name="DemoGateway",
        roleArn=gateway_role_arn,
        protocolType="MCP",
        authorizerType="AWS_IAM",
        protocolConfiguration={"mcp": {"searchType": "SEMANTIC"}},  # enables semantic tool search
    )

    gateway_id = gateway["gatewayId"]
    gateway_url = gateway["gatewayUrl"]

    while True:
        time.sleep(2)
        gateway_check = agentcore_client.get_gateway(gatewayIdentifier=gateway_id)
        gateway_status = gateway_check.get("status")

        if gateway_status in ("CREATING", "UPDATING"):
            print(".", end="")
            continue
        elif gateway_status == "READY":
            print("Gateway Ready!")
            break
        else:
            raise Exception(f"Gateway failed with status {gateway_status}")

    print(f"Gateway ID: {gateway_id}")
    print(f"Gateway URL: {gateway_url}")
    print("Please copy and run this command to configure your Gateway clients:")
    print(f"export DEMO_GATEWAY_URL={gateway_url}")

    return gateway_id


def create_gateway_target(region: str, account_id: str, gateway_id: str):
    """Creates an AgentCore Gateway Lambda target"""

    agentcore_client = boto3.client("bedrock-agentcore-control", region_name=region, aws_account_id=account_id)

    # Use the Lambda function created by create_lambda_function.py
    lambda_arn = f"arn:aws:lambda:{region}:{account_id}:function:DemoToolLambda"

    # Load tool specs from JSON file
    with open("../mcp-prototype/tool_specs.json", "r") as f:
        tool_specs = json.load(f)

    agentcore_client.create_gateway_target(
        gatewayIdentifier=gateway_id,
        name="DemoLambdaTarget",
        targetConfiguration={"mcp": {"lambda": {"lambdaArn": lambda_arn, "toolSchema": {"inlinePayload": tool_specs}}}},
        credentialProviderConfigurations=[{"credentialProviderType": "GATEWAY_IAM_ROLE"}],
    )


def main():
    sts = boto3.client("sts")
    account_id = sts.get_caller_identity()["Account"]

    region = "us-west-2"

    gateway_id = create_gateway(region=region, account_id=account_id)

    create_gateway_target(region=region, account_id=account_id, gateway_id=gateway_id)


if __name__ == "__main__":
    main()
