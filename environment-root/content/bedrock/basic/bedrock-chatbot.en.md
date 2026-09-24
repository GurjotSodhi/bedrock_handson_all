---
title : "Lab B-3: Chatbot"
weight : 20401
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![The Chatbot Streamlit app showing a multi-turn conversation in which the user asks about rainbow colors and guitar strings, with alternating user and assistant chat bubbles and a text input field at the bottom](/static/labs/bedrock-chatbot/app-in-use.png)

In this lab, we will build a simple chatbot with Amazon Bedrock and Streamlit.

LLMs don't have any concept of state or memory. Any chat history has to be tracked externally and then passed into the model with each new message. We are using a list of custom objects to track chat history. Since there is a limit on the amount of content that can be processed by the model, we need to prune the chat history so there is enough space left to handle the user's message and the model's responses. Our code will delete older messages.


An important difference between this lab and the [retrieval-augmented generation lab](/bedrock/basic/bedrock-rag): the responses from this chatbot are based purely on the underlying foundation model, without any supporting data source. So the chatbot's messages can potentially include made-up responses (hallucination). In a [later lab](/bedrock/intermediate/bedrock-rag-chatbot), we will create a more powerful chatbot that incorporates the retrieval-augmented generation pattern to return more accurate responses.

You can build the application code by copying the code snippets below and pasting into the indicated Python file.

::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The chatbot pattern is good for the following use cases:

* Simple interactive user conversation, without the use of any specialized knowledge or data

---

## Architecture



![Architecture diagram showing a 5-step chatbot flow: past interactions stored in a Chat History box (step 1 and 3), a user question sent to Amazon Bedrock (step 2), the combined question and chat history used as the prompt (step 4), and the AI response returned to the user interface (step 5)](/static/labs/bedrock-chatbot/architecture.png)

1. Past interactions are tracked in the chat memory object.
2. The user enters a new message.
3. The chat history is retrieved from the memory object and added before the new message.
4. The combined history & new message are sent to the model.
5. The model's response is displayed to the user.



This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/chatbot** folder, and open the file **chatbot_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;



2. Add the import statements and the ChatMessage class definition.

    * These statements allow us to use the Boto3 library to call Amazon Bedrock.

    * MAX_MESSAGES sets the upper limit for previous chat messages kept in memory.

    * The ChatMessage class is used to store text messages.

    * You can use the copy button in the box below to automatically copy its code:





::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3

MAX_MESSAGES = 20

class ChatMessage(): #create a class that can store image and text messages
    def __init__(self, role, text):
        self.role = role
        self.text = text


::::




&nbsp;


3. Add a function to convert ChatMessages to the Converse API format.

    * This format allows us to send a list of current and past messages to Amazon Bedrock for processing.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def convert_chat_messages_to_converse_api(chat_messages):
    messages = []
    
    for chat_msg in chat_messages:
        messages.append({
            "role": chat_msg.role,
            "content": [
                {
                    "text": chat_msg.text
                }
            ]
        })
            
    return messages


::::




&nbsp;





4. Add this function to call Amazon Bedrock.

    * We're creating a function we can call from the Streamlit front end application. This function creates an Amazon Bedrock client with Boto3, then passes the input content to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def chat_with_model(message_history, new_text=None):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    
    new_text_message = ChatMessage('user', text=new_text)
    message_history.append(new_text_message)
    
    number_of_messages = len(message_history)
    
    if number_of_messages > MAX_MESSAGES:
        del message_history[0 : (number_of_messages - MAX_MESSAGES) * 2] #make sure we remove both the user and assistant responses
    
    messages = convert_chat_messages_to_converse_api(message_history)
    
    response = bedrock.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=messages,
        inferenceConfig={
            "maxTokens": 2000,
            "stopSequences": []
        },
    )
    
    output = response['output']['message']['content'][0]['text']
    
    response_message = ChatMessage('assistant', output)
    
    message_history.append(response_message)
    
    return


::::




&nbsp;

5. Save the file.

Nice! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **chatbot_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}

import streamlit as st #all streamlit commands will be available through the "st" alias
import chatbot_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}

st.set_page_config(page_title="Chatbot") #HTML title
st.title("Chatbot") #page title


::::



&nbsp;


4. Add the UI chat history to the session cache.

    * This allows us to re-render the chat history to the UI as the Streamlit app is re-run with each user interaction. Otherwise, the old messages will disappear from the user interface with each new chat message.


::::code{showCopyAction=true language="python" showLineNumbers=false}

if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history


::::



&nbsp;



5. Add the chat input controls

    * These controls allow us to send text to the Claude model for processing.

    * We use the `if` block below to handle the user input.

::::code{showCopyAction=true language="python" showLineNumbers=false}

chat_container = st.container()

input_text = st.chat_input("Chat with your bot here") #display a chat input box

if input_text:
    glib.chat_with_model(message_history=st.session_state.chat_history, new_text=input_text)


::::



&nbsp;




6. Add the for loop to render previous chat messages.

    * Re-render previous messages based on the chat_history session state object.

::::code{showCopyAction=true language="python" showLineNumbers=false}

#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with chat_container.chat_message(message.role): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message.text) #display the chat content


::::



&nbsp;



7. Save the file.

Magnificent! Now you are ready to run the application!



&nbsp;

# Run the Streamlit app

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/chatbot

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/chatbot

:::

You can now proceed with step 2 below.

::::

:::::







&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run chatbot_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![The Chatbot Streamlit app at initial launch showing the page title "Chatbot" and an empty chat area with a "Chat with your bot here" input field at the bottom](/static/labs/bedrock-chatbot/app.png)



&nbsp;

4. Try out some prompts and see the results.

    * :code[What is the first color of the rainbow?]{showCopyAction=true}
    * :code[What is the next one?]{showCopyAction=true}
    * :code[What is the first planet from the sun?]{showCopyAction=true}
    * :code[What is the next one?]{showCopyAction=true}



![The Chatbot Streamlit app showing a multi-turn conversation in which the user asks about rainbow colors and guitar strings, with alternating user and assistant chat bubbles and a text input field at the bottom](/static/labs/bedrock-chatbot/app-in-use.png)






&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;




::alert[You have successfully built a chatbot with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
