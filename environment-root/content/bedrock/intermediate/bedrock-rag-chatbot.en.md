---
title : "Lab I-1: Chatbot with RAG"
weight : 30100
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![RAG Chatbot Streamlit UI showing a two-turn conversation where the user asks "what can you do with it?" and "what else?", with the assistant responding with bulleted lists of Amazon Bedrock capabilities, and a chat input box at the bottom](/static/labs/bedrock-rag-chatbot/app-in-use.png)



In this lab, we will build a chatbot supported by Retrieval-Augmented Generation (RAG). We'll use Anthropic Claude, Amazon Titan Embeddings, and Streamlit. We will use Amazon Bedrock's built-in tool use capabilities to allow Anthropic Claude to decide when to use the retrieval-augmented generation pattern.

We will use a local [Chroma](https://docs.trychroma.com/) database to demonstrate the RAG pattern. In a real-world scenario, you will most likely want to use a persistent data store through [Knowledge Bases for Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/).


You can build the application code by copying the code snippets below and pasting into the indicated Python file.

::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The chatbot with RAG pattern is good for the following use cases:

* Simple interactive user conversation, supported by specialized knowledge or data

---

## Architecture



![Architecture diagram showing Amazon Bedrock at the center connected to a chat history database, a vector DB knowledge base, a user input panel, and an AI response panel, with six numbered arrows illustrating the RAG chatbot data flow from user question through retrieval and response](/static/labs/bedrock-rag-chatbot/architecture.png)

1. Past interactions are tracked in the chat memory object.
2. The user enters a new message.
3. The chat history is retrieved from the memory object and added before the new message.
4. The question is converted to a vector using Amazon Titan Embeddings, then matched to the closest vectors in the vector database.
5. The combined history, knowledge, and new message are sent to the model.
6. The model's response is displayed to the user.



This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/rag_chatbot** folder, and open the file **rag_chatbot_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements and the ChatMessage class definition.

    * These statements allow us to use Python to call Amazon Bedrock and our local Chroma vector database.

    * MAX_MESSAGES sets the upper limit for previous chat messages kept in memory.

    * The ChatMessage class is used to store text messages.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import itertools
import boto3
import chromadb
from chromadb.utils.embedding_functions import AmazonBedrockEmbeddingFunction

MAX_MESSAGES = 20

class ChatMessage(): #create a class that can store image and text messages
    def __init__(self, role, text):
        self.role = role
        self.text = text


::::

&nbsp;

3. Add a function to connect to the ChromaDB collection.

    * This will allow us to access the previously created Chroma vector database.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_collection(path, collection_name):
    session = boto3.Session()
    embedding_function = AmazonBedrockEmbeddingFunction(session=session, model_name="amazon.titan-embed-text-v2:0")
    
    client = chromadb.PersistentClient(path=path)
    collection = client.get_collection(collection_name, embedding_function=embedding_function)
    
    return collection


::::

&nbsp;



4. Add the function to retrieve results from the vector store.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_vector_search_results(collection, question):
    
    results = collection.query(
        query_texts=[question],
        n_results=4
    )
    
    return results


::::

&nbsp;




5. Add a function to create the tool definitions we will use to define the format for the generated JSON.

    * Please see this article to learn more about the JSON Schema format below: https://community.aws/content/2hWA16FSt2bIzKs0Z1fgJBwu589/generating-json-with-the-amazon-bedrock-converse-api

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_tools():
    tools = [
        {
            "toolSpec": {
                "name": "get_amazon_bedrock_information",
                "description": "Retrieve information about Amazon Bedrock, a managed service for hosting generative AI models.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The retrieval-augmented generation query used to look up information in a repository of FAQs about Amazon Bedrock."
                            }
                        },
                        "required": [
                            "query"
                        ]
                    }
                }
            }
        }
    ]

    return tools


::::



6. Add a function to convert ChatMessages to the Converse API format.

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


7. Add a function to handle any tool use requests.

    * This format lets us check the model's response to see if the `get_amazon_bedrock_information` tool was requested. If it was, we will retrieve relevant content from the vector database and submit an additional request to Anthropic Claude to generate a final response based on the retrieved content.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def process_tool(response_message, messages, bedrock, tool_list):
    
    messages.append(response_message)
    
    response_content_blocks = response_message['content']

    follow_up_content_blocks = []
    
    for content_block in response_content_blocks:
        if 'toolUse' in content_block:
            tool_use_block = content_block['toolUse']
            
            if tool_use_block['name'] == 'get_amazon_bedrock_information':
                
                collection = get_collection("../../data/chroma", "bedrock_faqs_collection")
                
                query = tool_use_block['input']['query']
                
                print("----QUERY:----")
                print(query)
                
                search_results = get_vector_search_results(collection, query)
    
                flattened_results_list = list(itertools.chain(*search_results['documents'])) #flatten the list of lists returned by chromadb
                
                rag_content = "\n\n".join(flattened_results_list)
                
                print("----RAG CONTENT----")
                print(rag_content)
                
                follow_up_content_blocks.append({
                    "toolResult": {
                        "toolUseId": tool_use_block['toolUseId'],
                        "content": [
                            { "text": rag_content }
                        ]
                    }
                })
                
                
    if len(follow_up_content_blocks) > 0:
        
        follow_up_message = {
            "role": "user",
            "content": follow_up_content_blocks,
        }
    
        messages.append(follow_up_message)
        
        response = bedrock.converse(
            modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            messages=messages,
            inferenceConfig={
                "maxTokens": 2000,
                "stopSequences": []
            },
            toolConfig={
                "tools": tool_list
            }
        )
        
    
        return True, response['output']['message']['content'][0]['text'] #tool used, response
        
    else:
        return False, None #tool not used, no response


::::


&nbsp;

8. Add this function to handle the request from the Streamlit front end application.

    * We're creating a function we can call from the Streamlit front end application.
    * This function creates an Amazon Bedrock client with Boto3, then passes the input content to Amazon Bedrock.
    * It can then optionally handle a tool use request if necessary.

::::code{showCopyAction=true language="python" showLineNumbers=false}

def chat_with_model(message_history, new_text=None):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    
    tool_list = get_tools()
    
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
        toolConfig={
            "tools": tool_list
        }
    )
    
    response_message = response['output']['message']
    
    tool_used, output = process_tool(response_message, messages, bedrock, tool_list)
    
    if not tool_used: #just use the original non-RAG result if no tool was needed
        output = response['output']['message']['content'][0]['text']
    
    
    print("----FINAL RESPONSE----")
    print(output)
    
    response_chat_message = ChatMessage('assistant', output)
    
    message_history.append(response_chat_message)
    
    return


::::

&nbsp;





9. Save the file.

Nice! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **rag_chatbot_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias
import rag_chatbot_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}

st.set_page_config(page_title="RAG Chatbot") #HTML title
st.title("RAG Chatbot") #page title


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

    * These controls allow us to send text to the Claude 3 model for processing.

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

1. Select the **Terminal** in your development environment and run the script to initialize the vector database.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/data
python3 populate_collection.py

::::

&nbsp;



2. Change directory to the application.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/rag_chatbot

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/rag_chatbot

:::

You can now proceed with step 2 below.

::::

:::::







&nbsp;

3. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run rag_chatbot_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


4. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![RAG Chatbot Streamlit app at initial launch showing the "RAG Chatbot" page title and an empty chat input box labeled "Chat with your bot here" with no messages yet](/static/labs/bedrock-rag-chatbot/app.png)



&nbsp;

5. Try out some prompts and see the results.

    * :code[what can you do with it?]{showCopyAction=true}
    * :code[what else?]{showCopyAction=true}
    * :code[what models?]{showCopyAction=true}



![RAG Chatbot Streamlit UI showing a two-turn conversation where the user asks "what can you do with it?" and "what else?", with the assistant responding with bulleted lists of Amazon Bedrock capabilities, and a chat input box at the bottom](/static/labs/bedrock-rag-chatbot/app-in-use.png)


::::alert{header="Check the terminal!" type="info"}
You can see the rewritten prompt, retrieved content, and final response each time the RAG tool is used.

Note how the original vague user request of "what else?" gets rewritten to something clearer, like "What other capabilities does Amazon Bedrock provide?"
::::



&nbsp;

6. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;




::alert[You have successfully built a RAG chatbot with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}
