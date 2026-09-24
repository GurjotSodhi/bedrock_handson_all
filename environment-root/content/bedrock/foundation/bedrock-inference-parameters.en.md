---
title : "Lab F-4: Inference parameters"
weight : 10400
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Terminal output showing the params.py script being run with the ai21.j2-ultra-v1 model and a haiku prompt, with the model's response displayed: "Whispering spring breeze / Blooms dance in radiant hues / Nature's poetry"](/static/labs/params/app-in-use.png)

**[Inference parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html)** are used to configure the response behavior of the foundation model. Inference parameters vary from model to model:

* At a minimum, they can be used to influence the variability (**Temperature**, **Top P**) and **token length** of the response.
    * You can think of **tokens** as either a word or part of a word. The overall ratio of tokens per word varies from model to model. Many common words could be represented as a single token, while less common words might contain multiple tokens.
* **Stop Sequences** are another common parameter, useful for splitting few-shot prompt examples or stopping the model from having a conversation with itself. 

You can see the various inference parameters for each model in the Amazon Bedrock console, along with definitions for those parameters.

In this lab, we will use the Converse API to pass a standard set of parameters to Amazon Bedrock models.

The Converse API standard inference parameters are documented here: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html 


The Converse API also supports an `additionalModelRequestFields` parameter, if you need to set additional inference parameters for a specific model that aren't handled by the standard Converse API inferenceConfig parameter. You can learn more about model-specific inference parameters here: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html


You can build the application code by copying the code snippets below and pasting into the indicated Python file.



---

&nbsp;


# Create the Python script
---

&nbsp;

1. Navigate to the **workshop/labs/params** folder, and open the file **params.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements.

    * These statements allow us to call Amazon Bedrock and access command line arguments.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import sys
import boto3


::::




&nbsp;


3. Build the function to call Amazon Bedrock with the appropriate inference parameters for the model.

    * Here we are instantiating the Amazon Bedrock client, setting the model, and getting the inference parameters for the model.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_text_response(model, input_content):

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        "role": "user",
        "content": [ { "text": input_content } ]
    }
    
    response = bedrock.converse(
        modelId=model,
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "stopSequences": []
        },
    )
    
    return response['output']['message']['content'][0]['text']
    

::::




&nbsp;



4. Pass the command line parameters to the `get_text_response` function.

    * We're passing in the first argument (Bedrock Model ID) and second argument (prompt) from the command line.

::::code{showCopyAction=true language="python" showLineNumbers=false}
response = get_text_response(sys.argv[1], sys.argv[2])

::::


&nbsp;


5. Display the response.

    * This prints the text returned by the model.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print(response)


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
cd /environment/workshop/labs/params

::::



&nbsp;

2. Run the script from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 params.py "us.amazon.nova-pro-v1:0" "Please write a haiku:"

::::

The results should be displayed in the terminal:

![Terminal showing the params.py script executed with the ai21.j2-ultra-v1 model, returning a three-line haiku: "Whispering spring breeze / Blooms dance in radiant hues / Nature's poetry"](/static/labs/params/app-in-use.png)



&nbsp;

3. Try using the Mistral model.



::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 params.py "mistral.mixtral-8x7b-instruct-v0:1" "Write a haiku:" 

::::


&nbsp;

4. Try using the Cohere Command model.



::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 params.py "cohere.command-r-plus-v1:0" "Write a haiku:"

::::


&nbsp;



---

&nbsp;

You can learn more about inference parameters in the [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html).


::alert[You have successfully called the Amazon Bedrock API with inference parameters!]{header="Congratulations!" type="success"}
