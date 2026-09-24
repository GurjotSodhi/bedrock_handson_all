---
title: "Lab F-8: Intro to Streamlit"
weight: 10900
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::


# Lab introduction

---

*Final product:*

![Completed Streamlit Demo app with 'green' entered in the text input and the response 'I like green too!' displayed below](/static/labs/streamlit/app-in-use.png)

**Streamlit** is an open-source Python framework for building front-end applications to demo machine learning applications. Streamlit provides a library of commands for displaying web elements. You can see the list of controls in the [Streamlit API reference](https://docs.streamlit.io/library/api-reference).

Streamlit allows you to build simple and attractive user interfaces with a relatively small amount of Python code. For back-end developers, this means you can create demo applications for your code, without having to learn the various programming languages, frameworks, and hosting platforms for front-end development. Even for front-end developers, it allows you to quickly build a proof of concept to validate your approach.

Streamlit is well suited for creating generative AI prototypes. Throughout this workshop, you will have the opportunity to try a wide variety of Streamlit's capabilities that greatly simplify the demo-building process.

You run your Streamlit applications from the command line using the `streamlit run` command. You can find a more in-depth introduction to Streamlit at its [Get started page](https://docs.streamlit.io/library/get-started).

---

&nbsp;






# Create the Streamlit app

---

&nbsp;


1. Navigate to the workshop/labs/simple_streamlit folder, and open the file **simple_streamlit_app.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)

&nbsp;





&nbsp;


2. Add the import statement.

    * This statement allows us to use Streamlit elements and functions.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import streamlit as st #all streamlit commands will be available through the "st" alias


::::



&nbsp;



3. Add the page title and configuration.

    * Here we are setting the page title on the actual page and the title shown in the browser tab. 

::::code{showCopyAction=true language="python" showLineNumbers=false}
st.set_page_config(page_title="Streamlit Demo") #HTML title
st.title("Streamlit Demo") #page title


::::



&nbsp;


4. Add the input elements.

    * We are creating an input text box and button to get a color from the user.

::::code{showCopyAction=true language="python" showLineNumbers=false}
color_text = st.text_input("What's your favorite color?") #display a text box
go_button = st.button("Go", type="primary") #display a primary button


::::



&nbsp;


5. Add the output elements.

    * We use the `if` block below to handle the button click. We then format the submitted color and display it using Streamlit's `write` function.


::::code{showCopyAction=true language="python" showLineNumbers=false}
if go_button: #code in this if block will be run when the button is clicked

    st.write(f"I like {color_text} too!") #display the response content


::::



&nbsp;

6. Save the file.

Outstanding! Now you are ready to run the application!



&nbsp;

# Run the Streamlit app

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/simple_streamlit

::::


:::::alert{header="Just want to run the app?" type="info"}

::::expand{header="Expand here & run this command instead"}

:::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/completed/simple_streamlit

:::

You can now proceed with step 2 below.

::::

:::::





&nbsp;

2. Run the streamlit command from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
streamlit run simple_streamlit_app.py

::::

Ignore the Network URL and External URL links displayed by the Streamlit command. Instead, we will use our development environment's preview feature.

&nbsp;


3. In the popup, select **Open in Browser**.

![Screenshot of a popup notification containing an 'Open in Browser' button](/static/labs/code-preview.png)


You should see a web page like below:

![Streamlit Demo app in its initial state showing the page title 'Streamlit Demo', an empty text input labeled 'What's your favorite color?', and a 'Go' button](/static/labs/streamlit/app.png)



&nbsp;

4. Enter a color and see the results.

![Streamlit Demo app after entering 'green' as a favorite color, with the response 'I like green too!' shown below the input](/static/labs/streamlit/app-in-use.png)



&nbsp;

5. Close the preview tab in the browser. Return to the terminal and press Control-C to exit the application.


---

&nbsp;


::alert[You have successfully built a simple Streamlit app!]{header="Congratulations!" type="success"}




