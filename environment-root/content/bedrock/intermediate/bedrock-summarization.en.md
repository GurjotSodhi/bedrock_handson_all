---
title : "Lab I-2: Document summarization"
weight : 30200
---



::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Document Summarization Streamlit app showing a submitted prompt asking to highlight the three most important elements for an intern or new hire, with a Summary section below displaying a multi-paragraph response about Amazon's Leadership Principles](/static/labs/bedrock-summarization/app-in-use.png)

In this lab, we will build a simple document summarizer with Amazon Bedrock and Streamlit.

The Amazon Bedrock Converse API includes a document chat capability that allows you to pass the text of a document along with a prompt.

You can find which models support document chat in the table here: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html

Learn more about document chat here: https://community.aws/content/2i4v2vZRb9YgL2RxkawPiF8f0lZ/using-document-chat-with-the-amazon-bedrock-converse-api 


You can build the application code by copying the code snippets below and pasting into the indicated Python file.


::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The document summarization pattern is good for the following use cases:

* Summarizing long documents
* Summarizing call transcripts
* Summarizing customer activity history

---


This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.


---

&nbsp;



# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/summarization** folder, and open the file **summarization_lib.py**

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

    * This code passes the document bytes and a prompt to Amazon Bedrock, then returns the response text. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_summary(input_text):
    
    with open("amazon-leadership-principles-070621-us.pdf", "rb") as doc_file:
        doc_bytes = doc_file.read()

    doc_message = {
        "role": "user",
        "content": [
            {
                "document": {
                    "name": "Document 1",
                    "format": "pdf",
                    "source": {
                        "bytes": doc_bytes #Look Ma, no base64 encoding!
                    }
                }
            },
            { "text": input_text }
        ]
    }
    
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    response = bedrock.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=[doc_message],
        inferenceConfig={
            "maxTokens": 2000,
        },
    )
    
    return response['output']['message']['content'][0]['text']


::::


&nbsp;

4. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.


&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **summarization_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st
import summarization_lib as glib


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Document Summarization")
st.title("Document Summarization")


::::



&nbsp;



4. Add the interactive elements.

    * We have a document that will be automatically loaded behind the scenes.
    * The text box will allow the user to guide what the summary will focus on.
    * We use the `if` block below to handle the button click. We display a spinner while the backing function is called, then write the output to the web page.


::::code{showCopyAction=true language="python" showLineNumbers=false}
input_text = st.text_area("How would you like the document summarized?")

summarize_button = st.button("Summarize", type="primary")

if summarize_button:
    st.subheader("Summary")

    with st.spinner("Running..."):
        response_content = glib.get_summary(input_text)
        st.write(response_content)


::::



&nbsp;

5. Save the file.

Superb! Now you are ready to run the application!



&nbsp;

# Run the Streamlit app

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/summarization

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/summarization

:::

You can now proceed with step 2 below.

::::

:::::



&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run summarization_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![Document Summarization Streamlit app at launch showing the page title, a text area labeled "How would you like the document summarized?", and a red Summarize button with no output yet](/static/labs/bedrock-summarization/app.png)



&nbsp;

4. Try out some prompts and see the results.

    * :code[Please summarize the document, highlighting the three most important elements that an intern or new hire should focus on.]{showCopyAction=true}
    * :code[What are the top three principles for a newly promoted manager to consider?]{showCopyAction=true}


![Document Summarization Streamlit app showing a submitted prompt asking to highlight the three most important elements for an intern or new hire, with a Summary section below displaying a multi-paragraph response about Amazon's Leadership Principles](/static/labs/bedrock-summarization/app-in-use.png)




&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a document summarizer with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
