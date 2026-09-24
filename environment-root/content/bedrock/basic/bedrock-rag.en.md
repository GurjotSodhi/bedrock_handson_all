---
title : "Lab B-2: Retrieval-Augmented Generation"
weight : 20301
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![The Retrieval-Augmented Generation Streamlit app showing a question about Guardrails for Amazon Bedrock entered in the text area, with a detailed multi-point answer displayed below the Go button](/static/labs/bedrock-rag/app-in-use.png)

In this lab, we will build a simple question & answer application with Amazon Nova Lite, Titan Embeddings, and Streamlit.

Large language models are prone to **hallucination**, which is just a fancy word for making up a response. To correctly and consistently answer questions, we need to ensure that the model has real information available to support its responses. We use the **Retrieval-Augmented Generation** (RAG) pattern to make this happen.

With Retrieval-Augmented Generation, we first pass a user's prompt to a data store. This might be in the form of a query to [Amazon Kendra](https://aws.amazon.com/kendra/). We could also create a numerical representation of the prompt using Amazon Titan Embeddings to pass to a vector database. We then retrieve the most relevant content from the data store to support the large language model's response.

In this lab, we will use a local [Chroma](https://docs.trychroma.com/) database to demonstrate the RAG pattern. In a real-world scenario, you will most likely want to use a persistent data store through Amazon Kendra or [Knowledge Bases for Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/).


You can build the application code by copying the code snippets below and pasting into the indicated Python file.

::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The Retrieval-Augmented Generation pattern is good for the following use cases:

* Question & answer, supported by specialized knowledge or data
* Intelligent search

---

## Architecture


![Four-step RAG architecture diagram showing: new data flowing into Amazon Titan Embeddings and a vector DB knowledge base (step 1), a user submitting a question (step 2), the vector DB returning relevant context via a relevancy model (step 3), and the question plus context being sent to an Amazon Bedrock Foundation Model to produce an answer (step 4)](/static/labs/bedrock-rag/architecture.png)

1. A document is broken up into chunks of text. The chunks are passed to Titan Embeddings to be converted to vectors. The vectors are then saved to the vector database.
2. The user submits a question.
3. The question is converted to a vector using Amazon Titan Embeddings, then matched to the closest vectors in the vector database.
4. The combined content from the matching vectors + the original question are then passed to the large language model to get the best answer.



This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/rag** folder, and open the file **rag_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock and our local Chroma vector database.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import itertools
import boto3
import chromadb
from chromadb.utils.embedding_functions import AmazonBedrockEmbeddingFunction


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



5. Add this function to call Amazon Bedrock.

    * This code searches the previously created index based on the user's input, adds the best matches to a prompt along with the user's text, and then sends the combined prompt to the model.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_rag_response(question):

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    collection = get_collection("../../data/chroma", "bedrock_faqs_collection")
    
    search_results = get_vector_search_results(collection, question)
    
    flattened_results_list = list(itertools.chain(*search_results['documents'])) #flatten the list of lists returned by chromadb
    
    rag_content = "\n\n".join(flattened_results_list)
    print(rag_content)
    
    message = {
        "role": "user",
        "content": [
            { "text": rag_content },
            { "text": "Based on the content above, please answer the following question:" },
            { "text": question }
        ]
    }
    
    response = bedrock.converse(
        modelId="us.amazon.nova-2-lite-v1:0",
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "stopSequences": []
        },
    )
    
    return response['output']['message']['content'][0]['text'], flattened_results_list


::::




&nbsp;

6. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **rag_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}

import streamlit as st #all streamlit commands will be available through the "st" alias
import rag_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Retrieval-Augmented Generation") #HTML title
st.title("Retrieval-Augmented Generation") #page title


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
        response_content, search_results = glib.get_rag_response(question=input_text) #call the model through the supporting library
        
        st.write(response_content) #display the response content
        
        with st.expander("See search results"):
            st.table(search_results)


::::



&nbsp;

6. Save the file.

Superb! Now you are ready to run the application!



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
cd /environment/workshop/labs/rag

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/rag

:::

You can now proceed with step 2 below.

::::

:::::







&nbsp;

3. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run rag_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


4. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![The Retrieval-Augmented Generation Streamlit app at initial load, showing the page title, an empty multiline text input area, and a red Go button with no output yet displayed](/static/labs/bedrock-rag/app.png)



&nbsp;

5. Try out some prompts and see the results:

    * :code[What are some of the key features of Amazon Bedrock?]{showCopyAction=true}
    * :code[What can you do with Guardrails for Amazon Bedrock?]{showCopyAction=true}



![The Retrieval-Augmented Generation Streamlit app showing a question about Guardrails for Amazon Bedrock entered in the text area, with a detailed multi-point answer displayed below the Go button](/static/labs/bedrock-rag/app-in-use.png)



&nbsp;

6. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a question & answer app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}

