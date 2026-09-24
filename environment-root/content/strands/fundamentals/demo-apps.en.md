---
title: "Building agentic demo apps"
weight: 700
---


::::alert
This lab is based on the following article: [Building agentic demo apps](https://builder.aws.com/content/38oLfyfksQOGKf9TxnJSAEIOVeB/building-agentic-demo-apps-with-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/demo-apps**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/demo-apps

```



## Introduction: building simple demo apps with Strands Agents

In previous sections, we've covered the basics of [agents](https://builder.aws.com/content/38oL9fya9bzlvJYSVlgRqIWdGqn/understanding-agents-and-agentic-applications), [messages](https://builder.aws.com/content/38oL9fya9bzlvJYSVlgRqIWdGqn/understanding-agents-and-agentic-applications), and [tools](https://builder.aws.com/content/38oLPJ7KYLglawz3dScA5q8H4XJ/tool-function-decorators-for-strands-agents). Now that we are ready to start building, let's think about how to test and show off our agentic proofs of concept.

We may have an initial audience of technical colleagues - at that stage, a Jupyter notebook or one-off CLI script might be fine to show some code and results.

You may also have situations where you want to test some random inputs - a simple command line app is probably sufficient. You could also use notebooks to test these prompts, but it requires changing the notebook's code each time.

Or maybe you need to interactively chat with the agent - this is another area where notebooks aren't great, because you need to change the notebook's code for each message. A simple CLI-based chat app could work in this case.

Once you need to share with business stakeholders, you're going to want something visual and user-friendly. This is where [Streamlit](https://docs.streamlit.io/develop/api-reference) really shines. **Streamlit** is a framework for building basic web applications in Python. Streamlit is nice when you are already prototyping in Python, and don't want to context-switch to another set of languages and frameworks for a front-end demo.

Streamlit is great for demos, but you should treat it like a bridge to an eventual production platform. The Streamlit code should ultimately be thrown away.

For any prototype, you may progress from some combination of hardcoded scripts, to CLIs, to a Streamlit UI, to an API endpoint, to a web application, or to an event-driven process. Separating your agent logic from presentation logic early on is helpful - a mishmash of code can be hard to disentangle later. Our goal is to move quickly from prototype to production, and separation of concerns from the start can be helpful.

 

## A basic demo script

Let's start with a basic demo script. This could be the initial validation of a concept in a Jupyter notebook or CLI:

```python
"""A demo script"""

import math
from typing import Annotated
from strands import Agent, tool

@tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)

@tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)

@tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y

agent = Agent(tools=[cosine, sine, divide], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("What is the tangent of 8.12515? Provide accuracy to 5 places.")

```

This might be fine at the beginning, but you'll eventually want to test the functionality either interactively or with different inputs.

 

## Code examples

The examples below require the [strands-agents](https://pypi.org/project/strands-agents/) and [streamlit](https://pypi.org/project/streamlit/) packages to be installed, and AWS access.

&#x20;

### Creating a basic reusable agent

It's great to get ahead of things before we end up with a big ball of spaghetti. So we'll first separate the agent logic into its own module (**basic\_agent.py**):

```python
"""A basic reusable agent"""

import math
from typing import Annotated
from strands import Agent, tool

@tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)

@tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)

@tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y

def create_agent():
    """Creates and returns an agent with some basic math tools"""
    agent = Agent(tools=[cosine, sine, divide], model="us.anthropic.claude-haiku-4-5-20251001-v1:0")
    return agent

```

As your app grows in complexity, you may also choose to separate out your tools into their own files as well. We're keeping them with the agent for now, since they are so basic.

We also add an optional but recommended `create_agent` method here. This can be helpful when you want to ensure that an agent is created with the appropriate tools, system prompt, model, hooks, and other configuration options.

Now we can use that same agent in different ways.

 

## Basic CLI app

Let's build a basic CLI app (**cli.py**) that can take a prompt as an argument. We'll use Python's built-in [argparse](https://docs.python.org/3/library/argparse.html) library, although you could use something fancier like [Typer](https://typer.tiangolo.com/) or [Click](https://click.palletsprojects.com/en/stable/) if you prefer. We use the `create_agent()` function from the `basic_agent` module to create our agent, and then pass it the prompt from the command line.

```python
"""Command line interface for the agent."""

import argparse
from basic_agent import create_agent

def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", help="The prompt to send to the agent.", required=True)
    return parser.parse_args()

def main(prompt: str):
    """Main logic for command line interface"""
    agent = create_agent()

    agent(prompt)

if __name__ == "__main__":
    args = parse_args()
    main(args.prompt)

```

Run it:

```bash
python cli.py --prompt "What is the cosine of 1.4 radians?"
```

This should generate output similar to this:

```text
I'll calculate the cosine of 1.4 radians for you.
Tool #1: cosine
The cosine of 1.4 radians is approximately 0.170.
```

In this case, a single `--prompt` argument was fine, but in later sections we'll need multiple parameters for our CLI apps.

 

## Basic CLI chat app

For a more interactive experience, you can build a chat interface that maintains conversation history. Like the cli app, we use the `create_agent()` function from the `basic_agent` module to create our agent. Unlike the single-prompt CLI app, this version preserves the agent's conversation history across multiple messages, allowing for follow-up questions and multi-turn conversations. We use a while loop and Python's built-in `input()` function to receive the user's prompts.

In the **cli\_chat.py** code below, we use [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) to set the bot's text to bold (1;) and cyan (36), and the user's text to plain (0;) and yellow (33). You could also achieve this using the [rich](https://github.com/Textualize/rich) library.

The agent maintains conversation history as long as the script is running. Exit by entering "exit", "quit", "done", "bye", or pressing Ctrl+C.

```python
"""
A simple command-line interface for chatting with an agent.
"""

from basic_agent import create_agent

BOT_PREFIX = "\033[1;36m\n🤖Bot:"
HUMAN_PREFIX = "\033[0;33m\n\n🙂Me:\n"

def main():
    """Runs a CLI-based chat with the agent"""
    agent = create_agent()

    print(
        f"""{BOT_PREFIX}
Welcome! Type your message below and hit return to send.
Type "exit", "quit", "done", "bye" or press Ctrl-C to exit."""
    )

    while True:  # loop until exited
        try:
            prompt = input(f"{HUMAN_PREFIX}")

            if prompt.lower() in ["exit", "quit", "done", "bye"]:
                break

            print(f"{BOT_PREFIX}")
            agent(prompt)
        except KeyboardInterrupt:
            print("\nBye!\n")
            break

if __name__ == "__main__":
    main()

```

Run it:

```bash
python cli_chat.py
```

You'll see something similar to this:


![Terminal screenshot showing a CLI chat interface where an AI agent uses mathematical tools to answer user questions about division and trigonometry](/static/images/agentic-fundamentals/demo-apps/cli-chat.png)

Command lines can be easy to work with, but they aren't great for demos. Sometimes we need to present our demo to a broader audience. So we should try to use something more familiar, like a web application. Additionally, there are certain use cases that will only present well with a graphical user interface, even if it is for a technical audience.

 

## Basic Streamlit app

[Streamlit](https://streamlit.io/) is a framework for building basic web applications in Python. It's great for demos and prototypes, though you'll want a more robust framework for production applications.

To avoid the big ball of spaghetti, we'll also separate the Streamlit app into two modules: An "app" module that contains presentation layer things, and a "logic" module that includes any supporting logic and connections between the presentation layer and the agent. It may be helpful to think of the "app" portion as completely disposable, to be replaced by a HTML/JavaScript/CSS front end. And think of the "logic" module as partially disposable, with portions that might end up in a backing API.

Supporting logic in **ui\_demo\_logic.py**:

```python
"""The supporting logic for the streamlit app"""

from basic_agent import create_agent

class ChatMessage:
    """Stores basic text messages for the streamlit app"""

    def __init__(self, role, text):
        self.role = role
        self.text = text

agent = create_agent()

def chat_with_agent(message_history, new_text=None):
    """Sends a message to the model"""

    new_text_message = ChatMessage("user", text=new_text)
    message_history.append(new_text_message)

    response = agent(new_text)

    response_message = ChatMessage("assistant", text=response)
    message_history.append(response_message)

    return response

```

This includes the following:

1. A `ChatMessage` class to store messages for the user interface
2. A `chat_with_agent` function to bridge between the user interface and the agent object

Because we separate out this logic into a separate file, the `agent` object created in the script will persist between Streamlit UI updates. This allows us to more easily maintain message history without a lot of additional code.

 

Presentation layer in **ui\_demo\_app.py**:

```python
"""The presentation layer for the streamlit app"""

import streamlit as st  # all streamlit commands will be available through the "st" alias
import ui_demo_logic  # reference to local logic script

st.set_page_config(page_title="Chatbot")  # HTML title
st.title("Chatbot")  # page title

if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history

chat_container = st.container()

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # loop through the chat history
    # renders a chat line for the given role, containing everything in the with block
    with chat_container.chat_message(message.role):
        st.markdown(message.text)  # display the chat content

input_text = st.chat_input("Chat with your bot here")  # display a chat input box

if input_text:
    with chat_container.chat_message("user"):
        st.markdown(input_text) # Display user's posted message

    with st.spinner("Thinking...."):
        response = ui_demo_logic.chat_with_agent(message_history=st.session_state.chat_history, new_text=input_text)

        with chat_container.chat_message("assistant"):  # display user message in chat message container
            st.markdown(response)

```

Run it:

```bash
streamlit run ui_demo_app.py
```

You should then be able to view the result in a browser, like this:


![Screenshot of a web-based chatbot interface showing a user asking: What is the tangent of 1.23?; and the bot responding: The tangent of 1.23 radians is approximately 2.82.](/static/images/agentic-fundamentals/demo-apps/chatbot.png)

 

## Challenge yourself

1. Familiarize yourself with the [Streamlit API reference](https://docs.streamlit.io/develop/api-reference). What kind of page elements are available?
2. Try creating a Streamlit app without a chat interface. Allow the user to pass a single prompt to the agent, then display the response.

 



Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)


