import boto3
import json
import test_helper as glib

def invoke_nova_lite_with_guardrails(prompt, guardrail_id, guardrail_version, region='us-west-2'):
    bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
    model_id = 'us.amazon.nova-2-lite-v1:0'

    # Construct the request body
    request_body = {
        "schemaVersion": "messages-v1",
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 500,
            "temperature": 0.7,
            "topK": 20
        }
    }

    try:
        body = json.dumps(request_body)

        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=body,
            guardrailIdentifier=guardrail_id,
            guardrailVersion=guardrail_version,
            trace='ENABLED'  # Optional: enables tracing for debugging
        )

        response_body = json.loads(response['body'].read())
        model_response = response_body['output']['message']['content'][0]['text']

        if 'amazon-bedrock-trace' in response_body:
            trace = response_body['amazon-bedrock-trace']   
            print("Amazon Bedrock Trace:")
            print(json.dumps(trace, indent=4))

        return model_response

    except Exception as e:
        print(str(e))
        return None

prompt = glib.get_prompt_from_command_line()
guardrail_id = glib.get_guardrail_id('content_blocking_guardrail_id')
guardrail_version="DRAFT"

answer = invoke_nova_lite_with_guardrails(prompt, guardrail_id, guardrail_version)
print(answer)

