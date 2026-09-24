---
title: "Lab F-6: Streaming API"
weight: 10700
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Terminal window showing the command "python intro_streaming.py" being run in the ~/environment/workshop/labs/intro_streaming directory, with the script's streamed output appearing in the bash shell](/static/labs/streaming-intro/streaming-cli.gif)


In this lab, we will show how to make a streaming API call directly to Amazon Bedrock.

Streaming responses are useful when you want to start returning content immediately to the end user. You can display the output a few words at a time, instead of waiting for the entire response to be created.

We'll use the Boto3 library directly for this lab.

You can build the application code by copying the code snippets below and pasting into the indicated Python file.

---

&nbsp;


# Create the Python script
---

&nbsp;

1. Navigate to the **workshop/labs/intro_streaming** folder, and open the file **intro_streaming.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements.

    * These statements allow us to use the AWS Boto3 library to call Amazon Bedrock.
    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3


::::


&nbsp;


3. Define the callback handler for streaming results.

    * This function allows us to print response chunks as they are returned from the streaming api.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def chunk_handler(chunk):
    print(chunk, end='')


::::




&nbsp;



4. Define the function to call the Amazon Bedrock streaming API.

    * We use Amazon Bedrock's `converse_stream` function to make the call to the streaming API endpoint.
    * As response chunks are returned, this code extracts the chunk's text from the returned JSON and passes it to the provided callback function.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_streaming_response(prompt, streaming_callback):
    
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        "role": "user",
        "content": [ { "text": prompt } ]
    }
    
    response = bedrock.converse_stream(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
        }
    )
    
    stream = response.get('stream')
    for event in stream:
        if "contentBlockDelta" in event:
            streaming_callback(event['contentBlockDelta']['delta']['text'])


::::


&nbsp;


5. Display the response.

    * This defines the prompt and passes it to the `get_streaming_response` function along with the callback handler.

::::code{showCopyAction=true language="python" showLineNumbers=false}
prompt = "Tell me a story about two puppies and two kittens who became best friends:"
                
get_streaming_response(prompt, chunk_handler)
print("\n")


::::

&nbsp;


6. Save the file.

Great! Now you are ready to run the script!



&nbsp;

# Run the script

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/intro_streaming

::::



&nbsp;

2. Run the script from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 intro_streaming.py

::::



&nbsp;

3. The results should be displayed in the terminal.

![Terminal window showing the command "python intro_streaming.py" being run in the ~/environment/workshop/labs/intro_streaming directory, with the script's streamed output appearing in the bash shell](/static/labs/streaming-intro/streaming-cli.gif)

---

&nbsp;


::alert[You have successfully called the Amazon Bedrock streaming API!]{header="Congratulations!" type="success"}
