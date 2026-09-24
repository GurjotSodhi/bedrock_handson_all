---
title : "Lab I-4: Embeddings search"
weight : 30400
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![The Embeddings Search Streamlit app showing a question about Guardrails for Amazon Bedrock entered in the input field, with a table of matching FAQ text results displayed below](/static/labs/bedrock-embeddings-search/app-in-use.png)

In this lab, we will build a simple embeddings search application with Titan Embeddings and Streamlit.

This example is similar to the [Retrieval-Augmented Generation](/bedrock/basic/bedrock-rag) lab. In this lab, we also match a query to the closest entries in a vector database. But in this case, we do not pass those matches to a large language model. Instead, we will just display those matches directly in the user interface. This can be useful if you want to troubleshoot a RAG application, or directly evaluate an embeddings model.

In this lab, we will use a local [Chroma](https://docs.trychroma.com/) database to store and search for embeddings vectors. In a real-world scenario, you will most likely want to use a persistent data store through [Knowledge Bases for Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/).

You can build the application code by copying the code snippets below and pasting into the indicated Python file.

::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The embeddings search pattern is good for the following use cases:

* Identifying related items based on text descriptions
* Application portfolio rationalization - particularly in cases where data between the companies or divisions is inconsistent, matching applications based on their descriptions can accelerate the process of finding potential overlap.

---

## Architecture


![Architecture diagram showing four numbered steps: new data flows into a Document Store, then through Amazon Titan Embeddings into a Vector DB knowledge base (step 1); a user submits a question (step 2) which is matched against the Vector DB (step 3) via the Titan Embeddings relevancy model, and matching results are returned to the user (step 4)](/static/labs/bedrock-embeddings-search/architecture.png)

1. A document is broken up into chunks of text. The chunks are passed to Titan Embeddings to be converted to vectors. The vectors are then saved to the vector database.
2. The user submits a question.
3. The question is converted to a vector using Amazon Titan Embeddings, then matched to the closest vectors in the vector database.
4. The combined content from the matching vectors are then returned to the user



This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/embeddings_search** folder, and open the file **embeddings_search_lib.py**

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

    * This code searches the previously created index based on the user's input.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_vector_search_results(collection, question):
    
    results = collection.query(
        query_texts=[question],
        n_results=4
    )
    
    return results


::::


5. Add this function to handle search requests from the Streamlit app.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_similarity_search_results(question):

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    collection = get_collection("../../data/chroma", "bedrock_faqs_collection")
    
    search_results = get_vector_search_results(collection, question)
    
    flattened_results_list = list(itertools.chain(*search_results['documents'])) #flatten the list of lists returned by chromadb
    
    return flattened_results_list


::::




&nbsp;

6. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **embeddings_search_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias
import embeddings_search_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Embeddings Search", layout="wide") #HTML title
st.title("Embeddings Search") #page title


::::



&nbsp;







5. Add the input elements.

    * We are creating a multiline text box and button to get the user's prompt and send it to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
input_text = st.text_input("Question about Amazon Bedrock:")
go_button = st.button("Go", type="primary") #display a primary button


::::



&nbsp;


6. Add the output elements.

    * We use the `if` block below to handle the button click. We display a spinner while the backing functions are called.
    * Streamlit's `table` function displays the search results.


::::code{showCopyAction=true language="python" showLineNumbers=false}
if go_button: #code in this if block will be run when the button is clicked
    
    with st.spinner("Working..."): #show a spinner while the code in this with block runs
        response_content = glib.get_similarity_search_results(question=input_text)
        
        st.table(response_content) #using table so text will wrap
        

::::



&nbsp;

7. Save the file.

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
cd /environment/workshop/labs/embeddings_search

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/embeddings_search

:::

You can now proceed with step 2 below.

::::

:::::







&nbsp;

3. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run embeddings_search_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


4. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![The Embeddings Search Streamlit app at launch, showing the page title, a text input field labeled "Ask a question about Amazon SageMaker:", and a red Go button, with no results yet displayed](/static/labs/bedrock-embeddings-search/app.png)



&nbsp;

5. Try out some prompts and see the results. The lower the **score** value, the closer the match.

    * :code[What can you do with Amazon Bedrock?]{showCopyAction=true}
    * :code[What are the key features of Guardrails for Amazon Bedrock?]{showCopyAction=true}

![The Embeddings Search Streamlit app showing a question about Guardrails for Amazon Bedrock entered in the input field, with a table of matching FAQ text results displayed below](/static/labs/bedrock-embeddings-search/app-in-use.png)



&nbsp;

6. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built an embeddings search app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}

