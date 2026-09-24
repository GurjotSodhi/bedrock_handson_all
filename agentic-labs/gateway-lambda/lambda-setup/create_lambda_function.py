"""Create a custom Lambda function and add it as a Gateway target

This is based on the AgentCore Gateway Quickstart:
https://aws.github.io/bedrock-agentcore-starter-toolkit/user-guide/gateway/quickstart.html#custom-lambda-tools
"""

import io
import zipfile
import boto3


def create_custom_lambda(region, account_id):

    lambda_client = boto3.client("lambda", region_name=region)

    # Create zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write("lambda_function.py")
        zip_file.write("math_tool_functions.py")

    zip_buffer.seek(0)

    # Create Lambda function. This function uses the "DemoToolLambdaRole" that is automatically set up for the workshop
    function_name = "DemoToolLambda"
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.13",
            Role=f"arn:aws:iam::{account_id}:role/DemoToolLambdaRole",
            Handler="lambda_function.lambda_handler",
            Code={"ZipFile": zip_buffer.read()},
            Description="Demo Lambda function for AgentCore Gateway target",
        )
        lambda_arn = response["FunctionArn"]
        print(f"Created Lambda: {lambda_arn}")

    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.get_function(FunctionName=function_name)
        lambda_arn = response["Configuration"]["FunctionArn"]
        print(f"Lambda already exists: {lambda_arn}")

    return lambda_arn


if __name__ == "__main__":
    sts = boto3.client("sts")
    aws_account_id = sts.get_caller_identity()["Account"]

    aws_region = "us-west-2"

    create_custom_lambda(region=aws_region, account_id=aws_account_id)
