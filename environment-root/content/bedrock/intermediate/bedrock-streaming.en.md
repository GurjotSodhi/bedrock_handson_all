---
title : "Lab I-3: Response streaming"
weight : 30300
---


::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![The Response Streaming app with the prompt "Write a story about two cats that go on an adventure:" entered in the text area, the Go button visible, and a spinning "Working..." indicator showing the streamed response being generated](/static/labs/bedrock-streaming/streaming-ui.gif)

In this lab, we will build a response streaming application using Amazon Bedrock and Streamlit.

Streaming responses are useful when you want to start returning content immediately to the end user. You can display the output a few words at a time, instead of waiting for the entire response to be created.

You can build the application code by copying the code snippets below and pasting into the indicated Python file.



::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The response streaming pattern is good for the following use cases:

* Situations where longer text will be generated, but you want to keep the user engaged by beginning to return a response immediately.

---

## Architecture



![Architecture diagram showing a Prompt Input Request arrow flowing into an Amazon Bedrock Foundation Model, which fans out into three labeled response chunks (Chunk 1, Chunk 2, Chunk 3) representing streamed output](/static/labs/bedrock-streaming/architecture.png)

From an architectural perspective, response streaming is similar to text-to-text. We just need to add a special handler to immediately process the streaming output as it is created.

The streamed response is returned in chunks of JSON. You can then extract the returned text from each chunk to be displayed to the end user.


This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/streaming** folder, and open the file **streaming_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)



&nbsp;

2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock and process the streaming output.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3


::::



&nbsp;







3. Add this function to call Amazon Bedrock and handle the streaming response.

    * This function calls Amazon Bedrock with the streaming invocation method. As response chunks are returned, it passes the chunk's text to the provided callback method.

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

4. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **streaming_app.py**


&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streaming_lib as glib  # reference to local lib script
import streamlit as st


::::



&nbsp;


3. Add the page title, configuration, and two-column layout.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Response Streaming")  # HTML title
st.title("Response Streaming")  # page title


::::



&nbsp;





4. Add the input elements.

    * We are creating a multiline text box and button to get the user's prompt and send it to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")  # display a primary button


::::



&nbsp;


5. Add the output elements.

    * We use the `if` block below to handle the button click.
    * We create an empty streamlit container and pass it to the StreamlitCallbackHandler object so it can display output as it is generated.
    * We pass the StreamlitCallbackHandler to the backing function so it can handle responses as streaming chunks are returened.


::::code{showCopyAction=true language="python" showLineNumbers=false}
if go_button:  # code in this if block will be run when the button is clicked

    with st.empty():
        combined_response = ""
        
        def streaming_callback(chunk):
            global combined_response
            
            combined_response += chunk
            st.write(combined_response)
        
        glib.get_streaming_response(prompt=input_text, streaming_callback=streaming_callback)


::::



&nbsp;

6. Save the file.

Superb! Now you are ready to run the application!



&nbsp;

# Run the Streamlit app

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/streaming

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/streaming

:::

You can now proceed with step 2 below.

::::

:::::




&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run streaming_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![The Response Streaming Streamlit app at launch, showing an empty text area input field and a red Go button, with no output displayed yet](/static/labs/bedrock-streaming/app.png)



&nbsp;

4. Try out some prompts and see the results.

    * :code[Write a story about two cats that go on an adventure:]{showCopyAction=true}

![The Response Streaming app with the prompt "Write a story about two cats that go on an adventure:" entered in the text area, the Go button visible, and a spinning "Working..." indicator showing the streamed response being generated](/static/labs/bedrock-streaming/streaming-ui.gif)



&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a response streaming app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
