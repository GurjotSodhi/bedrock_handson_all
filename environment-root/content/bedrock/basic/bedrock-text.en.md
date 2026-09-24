---
title : "Lab B-1: Text generation"
weight : 20100
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::




# Lab introduction

---

*Final product:*

![The Text to Text Streamlit app showing a prompt asking for a product name for large language models, with the Go button and a generated response displayed below](/static/labs/bedrock-text/app-in-use.png)

In this lab, we will build a simple text generator with [Amazon Bedrock](https://aws.amazon.com/bedrock/) and Streamlit. We will collect user input, pass it to Amazon Bedrock, and return the foundation model’s response. While this is a fairly trivial example, it allows us to understand how to build a basic generative AI prototype with very little code.





You can build the application code by copying the code snippets below and pasting into the indicated Python file.

::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::


---

## Use cases

The basic text generation pattern is good for the following use cases:

* General content creation, where factuality isn't critical
* Basic question & answer for well-known facts that are repeated frequently on the internet

---

## Architecture


![Architecture diagram showing a three-step flow: a Prompt Input Request (chat bubble icon) passes via arrow to an Amazon Bedrock Foundation Model (brain icon), which then produces a Generated Output (document icon)](/static/labs/bedrock-text/architecture.png)

This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the workshop/labs/text folder, and open the file **text_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)

&nbsp;



2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock. 

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3


::::




&nbsp;


3. Add this function to call Amazon Bedrock.

    * We're creating a function we can call from the Streamlit front end application. This function creates an Amazon Bedrock client with Boto3, then passes the input content to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_text_response(input_content):

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
    

::::




&nbsp;

4. Save the file.

Great! You are done with the backing library. Now we will create the front-end application.



&nbsp;

# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **text_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias
import text_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Text to Text") #HTML title
st.title("Text to Text") #page title


::::



&nbsp;


4. Add the input elements.

    * We are creating a multiline text box and button to get the user's prompt and send it to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
input_text = st.text_area("Input text", label_visibility="collapsed") #display a multiline text box with no label
go_button = st.button("Go", type="primary") #display a primary button


::::



&nbsp;


5. Add the output elements.

    * We use the `if` block below to handle the button click. We display a spinner while the backing function is called, then write the output to the web page. 


::::code{showCopyAction=true language="python" showLineNumbers=false}
if go_button: #code in this if block will be run when the button is clicked
    
    with st.spinner("Working..."): #show a spinner while the code in this with block runs
        response_content = glib.get_text_response(input_content=input_text) #call the model through the supporting library
        
        st.write(response_content) #display the response content


::::



&nbsp;

6. Save the file.

Outstanding! Now you are ready to run the application!



&nbsp;

# Run the Streamlit app

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/text

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/text

:::

You can now proceed with step 2 below.

::::

:::::





&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run text_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![The Text to Text Streamlit app at launch, showing an empty multiline text input area and a red Go button, with no response yet displayed](/static/labs/bedrock-text/app.png)



&nbsp;

4. Try out some prompts and see the results.

    * :code[What is a good name for a product that provides large language models?]{showCopyAction=true}
    * :code[Why is the sky blue?]{showCopyAction=true}
    * :code[What is the capital of New Hampshire?]{showCopyAction=true}
    * :code[I am pleased to meet you. What is the sentiment of the previous statement?]{showCopyAction=true}

![The Text to Text Streamlit app with the prompt "What is a good name for a product that provides large language models?" entered, and a response suggesting "Gigaton AI" displayed below the Go button](/static/labs/bedrock-text/app-in-use.png)



&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a text-to-text app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
