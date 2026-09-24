---
title : "Lab I-6: Extracting JSON data from text"
weight : 30600
---


::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Text to JSON app showing a two-column layout: the left column contains a large text area with a customer complaint email and a Run button, and the right column displays the extracted JSON result with fields including summary, escalate_complaint set to true, overall_sentiment as Negative, supporting_business_unit as Customer Service, and sentiment_towards_employees listing Roger Longbottom as Negative](/static/labs/bedrock-json/app-in-use.png)

In this lab, we will build a JSON generator using Amazon Bedrock and Streamlit.

Text to JSON allows us to extract hierarchical data from unstructured content. For example, we can extract information from a customer's email, including any referenced products, employees mentioned, sentiment, account numbers, and anything else the model can detect based on our prompt.

We generate JSON through Amazon Bedrock's built-in tool use capabilities, which generate JSON responses based on a predefined JSON schema. You can learn more about generating JSON through tool use here: https://community.aws/content/2hWA16FSt2bIzKs0Z1fgJBwu589/generating-json-with-the-amazon-bedrock-converse-api

You can build the application code by copying the code snippets below and pasting into the indicated Python file.





::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The text to JSON pattern is good for the following use cases:

* Email data extraction
* Call transcript data extraction
* Document data extraction

---


This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/json** folder, and open the file **json_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)



&nbsp;

2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3


::::



&nbsp;



3. Add a function to create the tool definitions we will use to define the format for the generated JSON.

    * Please see this article to learn more about the JSON Schema format below: https://community.aws/content/2hWA16FSt2bIzKs0Z1fgJBwu589/generating-json-with-the-amazon-bedrock-converse-api

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_tools():
    tools = [
        {
            "toolSpec": {
                "name": "summarize_email",
                "description": "Summarize email content.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "A brief one-line or two-line summary of the email."
                            },
                            "escalate_complaint": {
                                "type": "boolean",
                                "description": "Indicates if this email is serious enough to be immediately escalated for further review."
                            },
                            "level_of_concern": {
                                "type": "integer",
                                "description": "Rate the level of concern for the above content on a scale from 1-10",
                                "minimum": 1,
                                "maximum": 10
                            },
                            "overall_sentiment": {
                                "type": "string",
                                "description": "The sender's overall sentiment.",
                                "enum": ["Positive", "Neutral", "Negative"]
                            },
                            "supporting_business_unit": {
                                "type": "string",
                                "description": "The internal business unit that this email should be routed to.",
                                "enum": ["Sales", "Operations", "Customer Service", "Fund Management"]
                            },
                            "customer_names": {
                                "type": "array",
                                "description": "An array of customer names mentioned in the email.",
                                "items": { "type": "string" }
                            },
                            "sentiment_towards_employees": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "employee_name": {
                                            "type": "string",
                                            "description": "The employee's name."
                                        },
                                        "sentiment": {
                                            "type": "string",
                                            "description": "The sender's sentiment towards the employee.",
                                            "enum": ["Positive", "Neutral", "Negative"]
                                        }
                                    }
                                }
                            }
                        },
                        "required": [
                            "summary",
                            "escalate_complaint",
                            "overall_sentiment",
                            "supporting_business_unit",
                            "level_of_concern",
                            "customer_names",
                            "sentiment_towards_employees"
                        ]
                    }
                }
            }
        }
    ]

    return tools


::::


&nbsp;






4. Add this function to call Amazon Bedrock.

    * This code calls Amazon Bedrock and extracts the JSON from the tool use response.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_json_response(input_content): #text-to-text client function

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    tool_list = get_tools()
    
    message = {
        "role": "user",
        "content": [
            { "text": f"<content>{input_content}</content>" },
            { "text": "Please use the summarize_email tool to generate the email summary JSON based on the content within the <content> tags." }
        ],
    }
    
    response = bedrock.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
        },
        toolConfig={
            "tools": tool_list,
            "toolChoice": {
                "tool": {
                    "name": "summarize_email"
                }
            }
        }
    )
    
    
    response_message = response['output']['message']
    
    response_content_blocks = response_message['content']
    
    content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)
    
    tool_use_block = content_block['toolUse']
    
    tool_result_dict = tool_use_block['input']
    
    return tool_result_dict


::::



&nbsp;

5. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **json_app.py**


&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias
import json_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title, configuration, and two-column layout.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Text to JSON", layout="wide")  #set the page width wider to accommodate columns
st.title("Text to JSON")  #page title

col1, col2 = st.columns(2)  #create 2 columns


::::



&nbsp;





4. Add the input elements.

    * We are creating a multiline text box and button to get the user's prompt and send it to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
with col1: #everything in this with block will be placed in column 1
    st.subheader("Content") #subhead for this column
    
    input_text = st.text_area("Input text", height=500, label_visibility="collapsed")

    process_button = st.button("Run", type="primary") #display a primary button


::::



&nbsp;


5. Add the output elements.

    * We use the `if` block below to handle the button click. We display a spinner while the backing function is called, then write the output to the web page. We display the formatted JSON.


::::code{showCopyAction=true language="python" showLineNumbers=false}
with col2: #everything in this with block will be placed in column 2
    st.subheader("Result") #subhead for this column
    
    if process_button: #code in this if block will be run when the button is clicked
        with st.spinner("Running..."): #show a spinner while the code in this with block runs
            response_content = glib.get_json_response(input_content=input_text) #call the model through the supporting library
            
            st.json(response_content) #render JSON if there was no error


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
cd /environment/workshop/labs/json

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/json

:::

You can now proceed with step 2 below.

::::

:::::




&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run json_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![Text to JSON app at launch showing a two-column dark-themed layout with a Content column on the left containing an empty text area and a red Run button, and an empty Result column on the right](/static/labs/bedrock-json/app.png)



&nbsp;

4. Try out some content and see the results.

    * ::::code{showCopyAction=true language="text" showLineNumbers=false}
Dear Acme Investments,
I am writing to bring to your attention a situation that I believe to be unethical on the part of one of your account managers, Roger Longbottom.
I recently met with Roger to discuss my investment portfolio and was deeply concerned to hear that he suggested I invest in a certain stock. When I asked him why he thought this was a good investment, he stated that the stock was currently undervalued and was likely to increase in value in the near future.
However, upon further research, I have discovered that the stock in question has a questionable reputation. It has been the subject of multiple lawsuits and has been found to have engaged in questionable business practices.
I believe Roger was aware of these facts, but failed to disclose them to me. As a result, I feel I was misled into making an unwise investment decision.
I therefore urge you to investigate whether Roger has acted unethically and take appropriate action if necessary.
Yours sincerely,
Carson Bradford
::::

    

![Text to JSON app showing a two-column layout: the left column contains a large text area with a customer complaint email and a Run button, and the right column displays the extracted JSON result with fields including summary, escalate_complaint set to true, overall_sentiment as Negative, supporting_business_unit as Customer Service, and sentiment_towards_employees listing Roger Longbottom as Negative](/static/labs/bedrock-json/app-in-use.png)



&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a JSON generator app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
