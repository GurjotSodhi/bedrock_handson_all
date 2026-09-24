---
title : "Lab I-5: Personalized recommendations"
weight : 30500
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---


*Final product:*

![The Personalized Recommendations Streamlit app showing a query for "A cloud NoSQL database service for massive amounts of data" with a result for Amazon DynamoDB and a bulleted personalized recommendation summary](/static/labs/bedrock-personalized-recommendations/app-in-use.png)

In this lab, we will build a personalized recommendations application with Amazon Bedrock and Streamlit.

This example is similar to the [Retrieval-Augmented Generation](/bedrock/basic/bedrock-rag) lab. In this lab, we also match a query to the closest entries in a vector database. But in this case, we will pass each matched result to the large language model to create a personalized summary about that match.

In this lab, we will use a local [Chroma](https://docs.trychroma.com/) database to store and search for embeddings vectors. In a real-world scenario, you will most likely want to use a persistent data store through [Knowledge Bases for Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/).


You can build the application code by copying the code snippets below and pasting into the indicated Python file.

::::alert{header="Just want to run the app?" type="info"}
You can [jump ahead to run a pre-made application](#run-the-streamlit-app).
::::

---

## Use cases

The personalized recommendations pattern is good for the following use cases:

* Creating personalized product recommendations, including a justification for each recommendation.
* Creating custom "10 best" articles for vacation destinations, colleges, vehicles, or anything else that lends itself to that type of article.

---

## Architecture


![Architecture diagram showing a 4-step flow: General content is converted by Amazon Titan Embeddings into a Vector DB knowledge base (step 1); a User submits a request (step 2); a Relevancy Model using Amazon Titan Embeddings matches the query to vectors in the knowledge base (step 3); the combined Request and Content is sent to an Amazon Bedrock Foundation Model which returns Personalized Recommendations (step 4)](/static/labs/bedrock-personalized-recommendations/architecture.png)

1. A document is broken up into chunks of text. The chunks are passed to Titan Embeddings to be converted to vectors. The vectors are then saved to the vector database.
2. The user submits a request.
3. The question is converted to a vector using Amazon Titan Embeddings, then matched to the closest vectors in the vector database.
4. The combined content and request are then used to generate a personalized recommendation to return to the user.



This application consists of two files: one for the Streamlit front end, and one for the supporting library to make calls to Amazon Bedrock.



---

&nbsp;




# Create the library script

---


First we will create the supporting library to connect the Streamlit front end to the Amazon Bedrock back end.


&nbsp;


1. Navigate to the **workshop/labs/recommendations** folder, and open the file **recommendations_lib.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)


&nbsp;

2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock and our local Chroma vector database.

    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
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




5. Add the function to create a personalized recommendation based on the user's question and search result item.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_personalized_recommendation(question, description):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        "role": "user",
        "content": [
            { "text": f"<service_description>{description}</service_description>" },
            { "text": "Based on the service description above, please summarize how it addresses the following requirements:" },
            { "text": f"<requirements>{question}</requirements>" }
        ]
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


6. Add the function to handle search requests from the Streamlit UI.

    * This code searches the previously created index based on the user's input, creates a personalized summary based on each match, and returns the results in a flattened form.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_similarity_search_results(question):

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    collection = get_collection("../../data/chroma", "services_collection")
    
    search_results = get_vector_search_results(collection, question)
    
    num_results = len(search_results['documents'][0])
    
    results_list = []
    
    for i in range(num_results):
        personalized_recommendation = get_personalized_recommendation(question, search_results['documents'][0][i])
        
        results_list.append({
            'original': search_results['documents'][0][i],
            'summary': personalized_recommendation,
            'name': search_results['metadatas'][0][i]['name'],
            'url': search_results['metadatas'][0][i]['url'],
        })
    
    return results_list


::::



7. Save the file.

Excellent! You are done with the backing library. Now we will create the front-end application.



&nbsp;



# Create the Streamlit front-end app

---

&nbsp;


1. In the same folder as your lib file, open the file **recommendations_app.py**



&nbsp;


2. Add the import statements.

    * These statements allow us to use Streamlit elements and call functions in the backing library script.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias
import recommendations_lib as glib #reference to local lib script


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Personalized Recommendations", layout="wide") #HTML title
st.title("Personalized Recommendations") #page title


::::



&nbsp;





4. Add the input elements.

    * We are creating a multiline text box and button to get the user's prompt and send it to Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
input_text = st.text_input("Name some key features you need from a cloud service:") #display a multiline text box with no label
go_button = st.button("Go", type="primary") #display a primary button


::::



&nbsp;


5. Add the output elements.

    * We use the `if` block below to handle the button click. We display a spinner while the backing functions are called.
    * We display each result with the product name linked to its URL, its personalized recommendation, and an expander with the source content.


::::code{showCopyAction=true language="python" showLineNumbers=false}
if go_button: #code in this if block will be run when the button is clicked
    
    with st.spinner("Working..."): #show a spinner while the code in this with block runs
        response_content = glib.get_similarity_search_results(question=input_text)
        
        for result in response_content:
            st.markdown(f"### [{result['name']}]({result['url']})")
            st.write(result['summary'])
            with st.expander("Original"):
                st.write(result['original'])


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
cd /environment/workshop/labs/recommendations

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/recommendations

:::

You can now proceed with step 2 below.

::::

:::::







&nbsp;

3. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run recommendations_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


4. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![The Personalized Recommendations Streamlit app at launch, showing the page title, an empty text input labeled "Name some key features you need from a cloud service:", and a red Go button with no results displayed](/static/labs/bedrock-personalized-recommendations/app.png)



&nbsp;

5. Try out some prompts and see the results:

    * :code[A service that allows users to access applications through a virtual desktop]{showCopyAction=true}
    * :code[A cloud NoSQL database service for massive amounts of data]{showCopyAction=true}



![The Personalized Recommendations Streamlit app showing a query for "A cloud NoSQL database service for massive amounts of data" with a result for Amazon DynamoDB and a bulleted personalized recommendation summary](/static/labs/bedrock-personalized-recommendations/app-in-use.png)



&nbsp;

6. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a personalized recommendation app with Amazon Bedrock and Streamlit!]{header="Congratulations!" type="success"}

