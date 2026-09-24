---
title: "Lab F-7: Embeddings"
weight: 10800
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Terminal output showing cosine similarity scores for two query phrases, listing ranked matches including translations in French, Japanese, German, and Spanish alongside their numerical similarity values](/static/labs/embedding/app-in-use.png)


In this lab, we will learn the basics of embeddings. We will use [Amazon Titan Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) to help find the relative similarity of text content.

**Embeddings** capture the meaning of a piece of text in a series of numbers called a **vector**. We can then use these vectors to determine how similar pieces of text are to each other.

We can use a **vector database** to store these embeddings and perform fast similarity searches. Embeddings paired with a vector database are a core component of **retrieval-augmented generation**, a key pattern that we will learn more about in later labs.


In the lab below, we will compare the similarity of meaning between various pieces of text, including some translations.

You can build the application code by copying the code snippets below and pasting into the indicated Python file.

---

&nbsp;


# Create the Python script
---

&nbsp;

1. Navigate to the **workshop/labs/embedding** folder, and open the file **bedrock_embedding.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)




&nbsp;

2. Add the import statements.

    * These statements allow us to use Python to call Amazon Bedrock, and make the necessary calculations to compare vectors.
    * You can use the copy button in the box below to automatically copy its code:

::::code{showCopyAction=true language="python" showLineNumbers=false}
import json
import boto3
from numpy import dot
from numpy.linalg import norm


::::




&nbsp;

3. Define the function to get an embedding from Amazon Bedrock.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def get_embedding(text):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')
    
    response = bedrock.invoke_model(
        body=json.dumps({ "inputText": text }), 
        modelId="amazon.titan-embed-text-v2:0", 
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['embedding']


::::

&nbsp;



4. Define the classes to store embeddings and the comparison results.

::::code{showCopyAction=true language="python" showLineNumbers=false}
class EmbedItem:
    def __init__(self, text):
        self.text = text
        self.embedding = get_embedding(text)

class ComparisonResult:
    def __init__(self, text, similarity):
        self.text = text
        self.similarity = similarity


::::

&nbsp;



5. Define the function to compare the similarity of two vectors.

    * This implements the [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity) equation.

::::code{showCopyAction=true language="python" showLineNumbers=false}
def calculate_similarity(a, b): #See Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity
    return dot(a, b) / (norm(a) * norm(b))


::::


&nbsp;



6. Build a list of embeddings from the items.txt file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
#Build the list of embeddings to compare
items = []

with open("items.txt", "r") as f:
    text_items = f.read().splitlines()

for text in text_items:
    items.append(EmbedItem(text))


::::

&nbsp;


7. Compare embeddings and display lists to show how similar or different the various texts are.

    * A similarity value of 1 means exactly the same.
    * The smaller the similarity, the less similar are the embeddings.

::::code{showCopyAction=true language="python" showLineNumbers=false}
for e1 in items:
    print(f"Closest matches for '{e1.text}'")
    print ("----------------")
    cosine_comparisons = []
    
    for e2 in items:
        similarity_score = calculate_similarity(e1.embedding, e2.embedding)
        
        cosine_comparisons.append(ComparisonResult(e2.text, similarity_score)) #save the comparisons to a list
        
    cosine_comparisons.sort(key=lambda x: x.similarity, reverse=True) # list the closest matches first
    
    for c in cosine_comparisons:
        print("%.6f" % c.similarity, "\t", c.text)
    
    print()


::::

&nbsp;





8. Save the file.

Great! Now you are ready to run the script!



&nbsp;

# Run the script

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/embedding

::::



&nbsp;

2. Run the script from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 bedrock_embedding.py

::::



&nbsp;

3. The results should be displayed in the terminal. Note the relative similarities.


![Terminal output showing cosine similarity scores for two query phrases, listing ranked matches including translations in French, Japanese, German, and Spanish alongside their numerical similarity values](/static/labs/embedding/app-in-use.png)

---

&nbsp;


::alert[You have successfully demonstrated embeddings and vector similarities!]{header="Congratulations!" type="success"}
