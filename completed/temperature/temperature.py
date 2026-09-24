import sys
import boto3

def get_text_response(input_content, temperature): #text-to-text client function
    
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        "role": "user",
        "content": [ { "text": input_content } ]
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


for i in range(3):
    response = get_text_response(sys.argv[1], float(sys.argv[2]))
    print(response, end='\n\n')

