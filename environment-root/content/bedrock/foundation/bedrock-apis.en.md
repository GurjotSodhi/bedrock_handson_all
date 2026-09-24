---
title: "Lab F-2: InvokeModel API"
weight: 10200
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Terminal window showing the bedrock_api.py script being run and the output "The largest city in New Hampshire is Manchester."](/static/labs/bedrock-apis/app-in-use.png)


In this lab, we will show how to make a basic API call directly to Amazon Bedrock. 


You can build the application code by copying the code snippets below and pasting into the indicated Python file.

---

&nbsp;


# Create the Python script
---

&nbsp;

1. Navigate to the **workshop/labs/api** folder, and open the file **bedrock_api.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements.

    * These statements allow us to use the AWS Boto3 library to call Amazon Bedrock.
    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import json
import boto3


::::




&nbsp;

3. Initialize the Amazon Bedrock client library.

    * This creates a Bedrock client.

::::code{showCopyAction=true language="python" showLineNumbers=false}
session = boto3.Session()

bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client


::::




&nbsp;


4. Build the payload for the API call.

    * Here we are identifying the model to use, the prompt, and the inference parameters for the specified model.

::::code{showCopyAction=true language="python" showLineNumbers=false}
bedrock_model_id = "us.amazon.nova-2-lite-v1:0" #set the foundation model

prompt = "What is the largest city in New Hampshire?" #the prompt to send to the model

messages = [
    {
        "role": "user",
        "content": [
            {"text": prompt}
        ]
    }
]

body = json.dumps({
    "schemaVersion": "messages-v1",
    "messages": messages,
    "inferenceConfig": {
        "maxTokens": 1024,
        "topP": 0.5,
        "topK": 20,
        "temperature": 0.0
    }
}) #build the request payload


::::


&nbsp;



5. Call the Amazon Bedrock API.

    * We use Bedrock's `invoke_model` function to make the call.

::::code{showCopyAction=true language="python" showLineNumbers=false}
response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') #send the payload to Amazon Bedrock


::::



&nbsp;


6. Display the response.

    * This extracts & prints the returned text from the model's response JSON.

::::code{showCopyAction=true language="python" showLineNumbers=false}
response_body = json.loads(response.get('body').read()) # read the response

response_text = response_body["output"]["message"]["content"][0]["text"] #extract the text from the JSON response

print(response_text)


::::






&nbsp;

7. Save the file.

Great! Now you are ready to run the script!



&nbsp;

# Run the script

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/api

::::



&nbsp;

2. Run the script from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 bedrock_api.py

::::



&nbsp;

3. The results should be displayed in the terminal.

![Terminal window showing the bedrock_api.py script being run and the output "The largest city in New Hampshire is Manchester."](/static/labs/bedrock-apis/app-in-use.png)

---

&nbsp;


::alert[You have successfully called the Amazon Bedrock API!]{header="Congratulations!" type="success"}
