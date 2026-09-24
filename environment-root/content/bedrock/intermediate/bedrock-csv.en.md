---
title : "Lab I-7: Extracting CSV data from text"
weight : 30700
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Text to CSV app showing a sample customer email in the Content text area, with a Result table displaying extracted fields (escalate_complaint, level_of_concern, overall_sentiment, supporting_business_unit, summary) and the corresponding raw CSV output below](/static/labs/bedrock-csv/app-in-use.png)

In this lab, we will build a CSV generator using Amazon Bedrock and Streamlit.

Text to CSV allows us to extract tabular data from unstructured content. For example, we can extract information from a customer's email, including any referenced products, employees mentioned, sentiment, account numbers, and anything else the model can detect based on our prompt.


To generate CSV, we first generate JSON through Amazon Bedrock's built-in tool use capabilities, which generate JSON responses based on a predefined JSON schema. We can then convert the JSON to CSV. You can learn more about generating JSON through tool use here: https://community.aws/content/2hWA16FSt2bIzKs0Z1fgJBwu589/generating-json-with-the-amazon-bedrock-converse-api




You can build the application code by copying the code snippets below and pasting into the indicated Python file.




::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The text to CSV pattern is good for the following use cases:

* Email data extraction
* Call transcript data extraction
* Document data extraction
* Sample dataset generation


---

This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/csv** folder, and open the file **csv_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock, and safely attempt to convert the output to a CSV.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3
import pandas as pd


::::




&nbsp;



3. Add a function to create the tool definitions we will use to define the format for the generated JSON (and ultimately the CSV file).

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
                            }
                        },
                        "summary": {
                            "type": "string",
                            "description": "A brief one-line or two-line summary of the email."
                        },
                        "required": [
                            "escalate_complaint",
                            "level_of_concern",
                            "overall_sentiment",
                            "supporting_business_unit",
                            "summary"
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

    * This code calls Amazon Bedrock and passes the response to the CSV converter.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_csv_response(input_content): #text-to-text client function

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
    
    data_frame = pd.DataFrame.from_dict([tool_result_dict])
    csv = data_frame.to_csv(index = False)
    
    return data_frame, csv


::::



&nbsp;

5. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.


&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **csv_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias
import csv_lib as glib #reference to local lib script


::::


&nbsp;



3. Add the page title, configuration, and two-column layout.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Text to CSV", layout="wide")  #set the page width wider to accommodate columns

st.title("Text to CSV")  #page title


::::



&nbsp;





4. Add the input elements.

    * We are creating a multiline text box and button to get the user's prompt and send it to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}

st.subheader("Content") #subhead for this column

input_text = st.text_area("Input text", height=200, label_visibility="collapsed")

process_button = st.button("Run", type="primary") #display a primary button


::::



&nbsp;


5. Add the output elements.

    * We use the `if` block below to handle the button click. We display a spinner while the backing function is called, then write the output to the web page. We display the dataframe as a table, along with the raw CSV content.


::::code{showCopyAction=true language="python" showLineNumbers=false}
st.subheader("Result") #subhead for this column

if process_button: #code in this if block will be run when the button is clicked
    with st.spinner("Running..."): #show a spinner while the code in this with block runs
        response_data_frame, response_csv = glib.get_csv_response(input_content=input_text) #call the model through the supporting library
        
        st.table(response_data_frame)
        
        st.markdown("#### Raw CSV")
        st.text(response_csv)
        

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
cd /environment/workshop/labs/csv

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/csv

:::

You can now proceed with step 2 below.

::::

:::::





&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run csv_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![Text to CSV app at launch showing an empty Content text area, a red Run button, and an empty Result section below](/static/labs/bedrock-csv/app.png)



&nbsp;

4. Try out some prompts and see the results.

    * ::::code{showCopyAction=true language="text" showLineNumbers=false}
Dear Acme Investments,
I am writing to compliment one of your customer service representatives, Shirley Scarry. I recently had the pleasure of speaking with Shirley regarding my loan. Shirley was extremely helpful and knowledgeable, and went above and beyond to ensure that all of my questions were answered. Shirley also had Robert Herbford join the call, who wasn't quite as helpful. My wife, Clara Bradford, didn't like him at all.
Shirley's professionalism and expertise were greatly appreciated, and I would be happy to recommend Acme Investments to others based on my experience.
Sincerely,

Carson Bradford
::::

![Text to CSV app showing a sample customer email in the Content text area, with a Result table displaying extracted fields (escalate_complaint, level_of_concern, overall_sentiment, supporting_business_unit, summary) and the corresponding raw CSV output below](/static/labs/bedrock-csv/app-in-use.png)





&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;

::alert[You have successfully built a CSV generator app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
