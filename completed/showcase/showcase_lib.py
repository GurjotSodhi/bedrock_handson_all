import boto3


def get_prompt(user_input, template):
    
    prompt = template.format(user_input=user_input)
    
    return prompt


def get_text_response(user_input, template):

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    prompt = get_prompt(user_input, template)
    
    message = {
        "role": "user",
        "content": [ { "text": prompt } ]
    }
    
    response = bedrock.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "stopSequences": []
        },
    )
    
    return response['output']['message']['content'][0]['text']
