---
title: "Message compaction"
weight: 500
---



::::alert
This lab is based on the following article: [Message compaction with Strands Agents](https://builder.aws.com/content/38oNwLRwQIiQEsuy2eG1KGZ0HR8/message-compaction-with-strands-agents)
::::



In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/compaction**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/compaction

```



## Introduction to message compaction

In the [Context engineering basics](https://builder.aws.com/content/38oLzpDYZJKUwbbKw3XyKD4Qjdd/introduction-to-context-engineering) section, we discussed the LLM's context window and the need to manage it through the practice of context engineering. In this section, we'll discuss a fundamental technique of context engineering, **message compaction**.

During an agentic workflow or interactive chat session with an LLM, past messages need to be sent to the LLM along with the latest message from the user or application. This allows for continuity in a multi-turn conversation. Over time, these messages can consume a lot of tokens, filling up the context window, adding costs, slowing down responses, and reducing the quality of the LLM's output. At some point, you will need to reduce the size of these messages to optimize the performance of your application.

**Message compaction** is the practice of replacing older messages in a conversation with their summary. This allows us to preserve important information about the conversation while keeping its size manageable.

 

## Conversation management with Strands Agents

To manage message history, Strands Agents offers [Conversation management](https://strandsagents.com/docs/user-guide/concepts/agents/conversation-management/) through the **ConversationManager** base class and two implementations: **SlidingWindowConversationManager** and **SummarizingConversationManager**:

* **SlidingWindowConversationManager** works by removing old messages above a target message count. This means that old messages and any useful information they may have contained are lost.
* **SummarizingConversationManager** works by summarizing old messages when a `ContextWindowOverflowException` is thrown. Older messages are summarized into a summary message, with some of the more recent messages preserved. This is an example of **message compaction**.

The **ConversationManager** base class works through two primary functions:

* `apply_management`: this method is called after each agent loop.
* `reduce_context`: this method is called when a `ContextWindowOverflowException` is thrown by the LLM.

The **SlidingWindowConversationManager** class uses both of these functions to proactively manage the number of messages with each agent loop. The **SummarizingConversationManager** class is purely reactive and only summarizes when the LLM's context window is maxed out.

Only summarizing past messages when the context window overflows means that we can still see negative effects like increased token costs, slower response times, and reduced response quality. Given those issues, a more proactive summarizing conversation manager may be preferable. The good news is that we can inherit from **ConversationManager** or **SummarizingConversationManager** to create a custom conversation manager.

Below, we'll implement a **ProactiveSummarizingConversationManager** so that we can apply more control over when message compaction occurs.

 

## Code examples

The examples below require that the [strands-agents](https://pypi.org/project/strands-agents/) and [streamlit](https://pypi.org/project/streamlit/) packages are installed, and AWS access.

 

## Proactive Summarizing Conversation Manager implementation

Since **SummarizingConversationManager** has most of the functionality we want, we'll have our **ProactiveSummarizingConversationManager** class inherit from it. When [reviewing the code for SummarizingConversationManager](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/agent/conversation_manager/summarizing_conversation_manager.py), we can see that the `apply_management` function contains only a `pass` statement, and the comments mention that it isn't proactive. So that seems like a good place to implement our custom logic.

**SummarizingConversationManager** already includes some useful parameters for summarization including `preserve_recent_messages` and `summary_ratio`. We just need to add a ceiling on message count so that we can proactively summarize when that ceiling is exceeded: `maximum_message_count_before_summarizing`.

In the `__init__` constructor, we validate that `preserve_recent_messages` (the minimum number of messages to preserve) is less than `maximum_message_count_before_summarizing` (the maximum number of messages to preserve).

In `apply_management`, we call `reduce_context` from **SummarizingConversationManager** whenever the message count exceeds `maximum_message_count_before_summarizing`.

Code for **proactive\_conversation\_manager.py**:

```python
"""A proactive conversation summarization manager"""

from typing import Optional, Any

from strands import Agent

from strands.agent.conversation_manager import SummarizingConversationManager

class ProactiveSummarizingConversationManager(SummarizingConversationManager):
    """Proactively summarizes messages after maximum_message_count_before_summarizing is reached"""

    def __init__(
        self,
        summary_ratio: float = 0.3,
        preserve_recent_messages: int = 10,
        summarization_agent: Optional["Agent"] = None,
        summarization_system_prompt: Optional[str] = None,
        maximum_message_count_before_summarizing: int = 20,
    ):
        if maximum_message_count_before_summarizing < preserve_recent_messages + 2:
            raise ValueError(
                "maximum_message_count_before_summarizing must be at least 2 greater than preserve_recent_messages."
            )

        super().__init__(
            summary_ratio=summary_ratio,
            preserve_recent_messages=preserve_recent_messages,
            summarization_agent=summarization_agent,
            summarization_system_prompt=summarization_system_prompt,
        )

        self.maximum_message_count_before_summarizing = maximum_message_count_before_summarizing

    def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
        """Proactively apply summarization after maximum_message_count_before_summarizing"""
        if len(agent.messages) > (self.maximum_message_count_before_summarizing):
            self.reduce_context(agent=agent)

```

 

## Compaction agent

The code for our agent is below. We define our agent, but also a separate agent that will do the summarizing. We're setting `preserve_recent_messages` and `maximum_message_count_before_summarizing` extremely low so that we don't have to wait long to see summarization happen. In real life, you will want higher values for these parameters. We're also returning `proactive_manager` from the `create_agent_and_proactive_manager` function so that we can display the summarization message in our user interface.

Code for **compaction\_agent.py**:

```python
"""A basic reusable agent"""

import math
from typing import Annotated
from strands import Agent, tool

from proactive_conversation_manager import ProactiveSummarizingConversationManager

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

@tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)

def create_agent_and_proactive_manager():
    """Creates and returns an agent"""

    summarizing_agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

    proactive_manager = ProactiveSummarizingConversationManager(
        preserve_recent_messages=4,  # set too low, for demo purposes only!
        maximum_message_count_before_summarizing=8,  # set too low, for demo purposes only!
        summarization_agent=summarizing_agent,
        summary_ratio=0.8,
    )

    main_agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        conversation_manager=proactive_manager,
        tools=[cosine, sine, divide, raise_to_power],
    )

    return main_agent, proactive_manager

```

 

## Demo Streamlit app

For the Streamlit app, we will implement a standard chatbot interface,
but with a side panel that shows the latest summary and message counts.

Code for **ui\_demo\_logic.py**:

```python
"""The supporting logic for the streamlit app"""

from compaction_agent import create_agent_and_proactive_manager

class ChatMessage:
    """Stores basic text messages for the streamlit app"""

    def __init__(self, role, text):
        self.role = role
        self.text = text

agent, proactive_manager = create_agent_and_proactive_manager()

def chat_with_agent(message_history, new_text=None):
    """Sends a message to the model"""

    new_text_message = ChatMessage("user", text=new_text)
    message_history.append(new_text_message)

    response = agent(new_text)

    response_message = ChatMessage("assistant", text=response)
    message_history.append(response_message)

    return response, proactive_manager.get_state(), agent.messages

```

 

Code for **ui\_demo\_app.py**:

```python
"""The presentation layer for the streamlit app"""

import streamlit as st  # all streamlit commands will be available through the "st" alias
import ui_demo_logic  # reference to local logic script

st.set_page_config(page_title="Compaction Chatbot", layout="wide")  # HTML title
st.title("Compaction Chatbot")  # page title

if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history

internals_column, chat_column = st.columns(2)

with chat_column:
    chat_container = st.container(height=500)

with internals_column:
    internals_container = st.container()

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # loop through the chat history
    # renders a chat line for the given role, containing everything in the with block
    with chat_container.chat_message(message.role):
        st.markdown(message.text)  # display the chat content

input_text = st.chat_input("Chat with your bot here")  # display a chat input box

if input_text:
    with chat_container.chat_message("user"):
        st.markdown(input_text)  # Display user's posted message

    with st.spinner("Thinking...."):
        response, summarization_state, agent_messages = ui_demo_logic.chat_with_agent(
            message_history=st.session_state.chat_history, new_text=input_text
        )

        with chat_container.chat_message("assistant"):  # display user message in chat message container
            st.markdown(response)

        with internals_container:
            st.markdown("**Summary**:")
            summary_message = summarization_state.get("summary_message")
            if summary_message:
                st.write(summary_message["content"][0]["text"])

            st.markdown(f"**Removed messages count:** {summarization_state["removed_message_count"]}")

            st.markdown(f"**Current messages count:** {len(agent_messages)}")

            with st.expander("Current messages of the agent:"):
                st.json(agent_messages)

```

 

Run it:

```bash
streamlit run ui_demo_app.py
```

You should then be able to view the result in a browser, like this:


![Screenshot of a Compaction Chatbot interface showing a conversation between a user named Jason and Claude, an AI assistant. The left sidebar displays summary information including 'Removed messages count: 0' and 'Current messages count: 2' with a collapsible section for 'Current messages of the agent'. The main chat area shows two messages: Jason's introduction asking 'My name is Jason, what's your name?' and Claude's response greeting Jason and offering assistance. A text input field at the bottom prompts 'Chat with your bot here'](/static/images/intermediate/compaction/chatbot-with-message.png)

After 8 messages, the summary should be displayed:


![Screenshot of a compaction chatbot interface showing a conversation summary panel on the left and chat messages on the right. The summary lists 4 conversation points including a location discussion, a math question about cosine of 2, the bot's answer, and a summary request. It shows 14 messages were removed and 5 current messages remain. The right panel displays a German language conversation about trigonometric calculations, with user messages in red and bot responses in orange, discussing the cosine of 2 in radians versus degrees and the cosine of 3.12.](/static/images/intermediate/compaction/chatbot-with-summary.png)

## Notes on the Proactive Summarizing Conversation Manager

When summarization should happen, the following steps occur:

* The number of old messages to summarize and remove is calculated based on the summary ratio, total messages, and number of recent messages to preserve.
* The oldest messages are summarized and removed from the conversation history
* The summary is added as a user message at the beginning of the conversation history

This is a fairly naive implementation. For example, it does not take into account the actual size of the LLM's context, or the size of the messages themselves. A few really large messages could still max out the context window. In that case, the overflow-based summarization would still occur.

A more sophisticated implementation would take into account total message size (including text, image, documents, etc.). See this [context compression feature request](https://github.com/strands-agents/sdk-python/issues/555) for more on the topic.

 

## Next steps

For another example of a custom context manager, see [Never Forget a Thing: Building AI Agents with Hybrid Memory Using Strands Agents](https://dev.to/aws/never-forget-a-thing-building-ai-agents-with-hybrid-memory-using-strands-agents-2g66)



Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)