---
title : "Memory"
weight : 200
---

::::alert
This lab is based on the following article: [Using Amazon Bedrock AgentCore Memory with Strands Agents](https://builder.aws.com/content/3AiwZ4TE46VNMNhuMDJkWu2OD19/using-amazon-bedrock-agentcore-memory-with-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/memory**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/memory
```


## Overview of Amazon Bedrock AgentCore Memory

[AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html) provides persistent storage for conversation-based data. It has two layers: [short-term memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html#short-term-memory) stores raw conversation messages within a session, and [long-term memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html#memory-long-term-memory) extracts durable information from those messages using configurable [memory strategies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-strategies.html).

AgentCore Memory organizes data around two primary identifiers: an **actor** (the user or entity interacting with the agent) and a **session** (a single conversation). These map to the `{actorId}` and `{sessionId}` placeholders you'll see in namespace patterns throughout this article.

When messages are saved to short-term memory, AgentCore runs an asynchronous background process that generates long-term memory records based on the strategies you configure. This process can take a minute or more. See the [documentation on long-term memory creation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-saving-and-retrieving-insights.html) for details.

 

## Short-term memory

[Short-term memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-memory-short-term.html) stores the raw messages from a conversation, organized by session. Each user message and agent response is saved as an event. This gives the agent a complete record of what happened in a session, so it can reload context if the user resumes a past conversation or if the service restarts.

Short-term memory also feeds long-term memory. When events are saved, AgentCore Memory runs a background process that extracts durable records based on the strategies you configure.

 

## Long-term memory

[Long-term memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-memory-long-term.html) stores structured information extracted from short-term memory (like conversation summaries, user preferences, and factual knowledge). Unlike short-term memory, which is tied to a single session, long-term memories persist across sessions and can be retrieved using semantic search. Each long-term memory is produced by a strategy that defines what to extract and how to organize it.

 

### Long-term memory strategy components

Each strategy has a namespace and one or more processing steps.

 

#### Namespaces

**Namespaces** determine where memory records are stored and retrieved. Namespaces use path-like patterns with placeholders like `{actorId}` and `{sessionId}`. See [Memory organization in AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-organization.html) for more on namespaces.

 

#### Steps

**Steps** define how memories are processed. Not every strategy uses every step.

* **Extraction** pulls useful information from short-term memory messages
* **Consolidation** updates or creates long-term memory records
* **Reflection** generates insights across multiple episodes (episodic memory only)

The [AgentCore Memory strategies documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-strategies.html) explains what happens at each step for a given strategy.

 

### Long-term memory built-in strategies

Amazon Bedrock AgentCore supports four built-in long-term memory strategies. Below we'll briefly discuss each strategy.

 

#### Summary strategy

The [summary strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/summary-strategy.html) captures summaries of an ongoing conversation. This is useful when rolling off older messages to reduce context window usage, or for helping users quickly understand what happened during a conversation.

It only includes a consolidation step. A single session can have multiple summary chunks, each covering a portion of the conversation. Together they form the complete summary for the session.

Example record content:

```xml
<topic name="User Identity and Preferences">
User's name is Jason (timestamp: 1771019363362). User likes cats (timestamp: 1771019288279) and favorite color is green (timestamp: 1771019301043).
</topic>
<topic name="Response Formatting Requirements">
User instructed that assistant must always respond using rhyming (timestamp: 1771019324413), described as "critical and must happen." User then added a second requirement to always begin responses with an emoji (timestamp: 1771019344478). Assistant acknowledged and began implementing both rules in subsequent responses.
</topic>
<topic name="Assistant Capabilities">
Assistant mentioned having tools available for mathematical calculations including sine, cosine, and division functions, but clarified these are not applicable to cat-related topics.
</topic>
```

Its default namespace is: `/strategy/{memoryStrategyId}/actor/{actorId}/session/{sessionId}/`.

In our examples below, we use the simplified namespace `/summaries/{actorId}/{sessionId}/`. This is an important design choice when designing your application. In our case, we chose to exclude `memoryStrategyId` for simplicity's sake. You may want to include `memoryStrategyId` in your design if you expect to version your strategies, or if you want to run multiple strategies of the same type in parallel.

Review the [Summary strategy overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/summary-strategy.html) and [System prompt for summary strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-summary-prompt.html) to better understand the internals of the summary strategy.

 

#### Semantic memory (facts) strategy

The [semantic memory strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/semantic-memory-strategy.html) extracts factual information from conversations. This is useful for building a persistent knowledge base about the user, so the agent can reference previously stated details without asking again. It includes extraction and consolidation steps.

Example record content:

```text
The user's name is Jason
```

Its default namespace is: `/strategy/{memoryStrategyId}/actors/{actorId}/`. In our examples below, we use the simplified namespace `/facts/{actorId}/`.

Review the [Semantic memory strategy overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/semantic-memory-strategy.html) and [System prompt for semantic memory strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-system-prompt.html) to better understand the internals of the semantic strategy.

 

#### User preference memory strategy

The [user preference strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/user-preference-memory-strategy.html) extracts user preferences as structured JSON, including context, the preference itself, and categories. This is useful for personalizing responses across sessions, so the agent can adapt its behavior to match what the user has asked for. It includes extraction and consolidation steps.

Example record content:

```json
{
    "context":"The user explicitly requested that all responses should incorporate cat themes and/or cat puns.",
    "preference":"Wants responses to include cat themes and cat puns",
    "categories":["communication style","animals","cats","humor"]
}
```

Its default namespace is: `/strategy/{memoryStrategyId}/actors/{actorId}/`. In our examples below, we use the simplified namespace `/preferences/{actorId}/`.

Review the [User preference strategy overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/user-preference-memory-strategy.html) and [System prompt for user preference strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-user-prompt.html) to better understand the internals of the user preference strategy.

 

#### Episodic memory strategy

The [episodic memory strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/episodic-memory-strategy.html) captures meaningful slices of interactions as structured episodes. It includes extraction, consolidation, and reflection steps. AgentCore automatically detects episode completion within conversations, then consolidates extractions into a single episode record. The reflection step analyzes patterns across multiple episodes to surface higher-level insights.

Episodes are returned as XML with situation, intent, assessment, justification, and episode-level reflection fields. Reflections consolidate across episodes to identify successful strategies, common failure modes, and lessons learned.

Episodes have the default namespace: `/strategy/{memoryStrategyId}/actor/{actorId}/`. Reflections must match or be less nested than the episode namespace. For example, you could keep reflections at the actor level using `/strategy/{memoryStrategyId}/actor/{actorId}/`, or roll up reflections across all users by using the namespace `/strategy/{memoryStrategyId}/`. Our examples below do not use the episodic strategy - it is a more advanced technique beyond the scope of this article.

Review the [Episodic memory strategy overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/episodic-memory-strategy.html) and [System prompt for episodic memory strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-episodic-prompt.html) to better understand the internals of the episodic strategy.

 

#### Customized and self-managed strategies

[Customized built-in strategies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-custom-strategy.html) let you customize the extraction and consolidation behavior of a built-in strategy. You can override the system prompt instructions (to focus extraction on a specific area, for example) or select a different foundation model. The output schema stays the same. See the [custom override example](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-custom-strategies.html) to learn more.

For full control over the memory pipeline, including custom output schemas, you can create a [self-managed strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-self-managed-strategies.html). With a self-managed strategy, you build the extraction, consolidation, and ingestion logic yourself.

Customized and self-managed strategies have different pricing than the built-in strategies, so be sure to review the details of [AgentCore Memory pricing.](https://aws.amazon.com/bedrock/agentcore/pricing/)

 

## Code examples

The examples below require that the [strands-agents](https://pypi.org/project/strands-agents/), [bedrock-agentcore](https://pypi.org/project/bedrock-agentcore/), and [streamlit](https://pypi.org/project/streamlit/) packages are installed, and AWS access.

 

### Create memory

The **create\_memory.py** script creates an AgentCore Memory resource with short-term memory and three long-term memory strategies: summary, user preference, and semantic (fact). The `event_expiry_days=7` setting tells AgentCore to automatically delete short-term memory events after 7 days. You'll want to set this to a duration that makes sense for your use case.

```python
"""Creates AgentCore Memory"""

from bedrock_agentcore.memory import MemoryClient

client = MemoryClient(region_name="us-west-2")

print("Creating AgentCore Memory and waiting (will take a few minutes)")

# create AgentCore Memory for your application
# this will create short term memory (by default) + 3 long term memory strategies
memory = client.create_memory_and_wait(
    name="DemoAgentMemory",
    description="Agent memory with summarization, preferences, and facts.",
    event_expiry_days=7,
    strategies=[
        {
            "summaryMemoryStrategy": {
                "name": "SessionSummaries",
                "description": "Extracts summaries about a session.",
                "namespaces": ["/summaries/{actorId}/{sessionId}/"],
            }
        },
        {
            "userPreferenceMemoryStrategy": {
                "name": "ActorPreferences",
                "description": "Extracts preferences for an actor.",
                "namespaces": ["/preferences/{actorId}/"],
            }
        },
        {
            "semanticMemoryStrategy": {
                "name": "ActorSemanticFacts",
                "description": "Extracts facts about an actor.",
                "namespaces": ["/facts/{actorId}/"],
            }
        },
    ],
)

# Get the AgentCore memory ID
memory_id = memory.get("id")

print("Please copy and run this command to configure your memory clients:")
print(f"export DEMO_MEMORY_ID={memory_id}")
```

From the terminal, run the following command to create your AgentCore Memory:

```bash
python create_memory.py
```

After a few minutes, you will see output like:

```bash
Creating AgentCore Memory and waiting (will take a few minutes)
Please copy and run this command to configure your memory clients:
export DEMO_MEMORY_ID=...
```

Copy the `export` command from your terminal output and run it, so the demo code below can use your configured memory.

 

### Create a demo actor ID

An actor ID identifies the user interacting with the agent. Our memory strategies are scoped to actors, so each actor has their own preferences, facts, and summaries.

Run the following in the terminal to create a unique actor ID for testing:

```bash
export DEMO_ACTOR_ID=$(uuidgen)
echo $DEMO_ACTOR_ID
```

 

### Agent with memory

The **memory\_agent.py** script defines the agent and its memory configuration. It creates an [AgentCoreMemorySessionManager](https://strandsagents.com/docs/community/session-managers/agentcore-memory/) with retrieval settings that control which namespaces are searched and how results are filtered by relevance score.

```python
"""A basic reusable agent"""

import os
import math
from typing import Annotated

from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from strands import Agent, tool

MEM_ID = os.getenv("DEMO_MEMORY_ID")

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

def get_session_manager(session_id: str, actor_id: str) -> AgentCoreMemorySessionManager:
    """Gets a session manager to be used by the Agent for memory management"""
    config = AgentCoreMemoryConfig(
        memory_id=MEM_ID,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            "/preferences/{actorId}/": RetrievalConfig(top_k=5, relevance_score=0.7),
            "/facts/{actorId}/": RetrievalConfig(top_k=10, relevance_score=0.3),
            "/summaries/{actorId}/{sessionId}/": RetrievalConfig(top_k=5, relevance_score=0.5),
        },
    )

    session_manager = AgentCoreMemorySessionManager(config)

    return session_manager

def create_agent(session_manager: AgentCoreMemorySessionManager):
    """Creates and returns an agent"""

    agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        session_manager=session_manager,
        tools=[cosine, sine, divide],
    )

    return agent
```

The `retrieval_config` parameter maps namespace patterns to retrieval settings. On each new conversation turn, the session manager searches these namespaces for relevant long-term memories and injects them into the agent's context. The `top_k` parameter limits how many records are returned, and `relevance_score` sets the minimum similarity threshold. Consider these just example settings - you will want to optimize these for your specific use case.

 

### Streamlit app with memory viewer

Now we'll create a demo app with Streamlit to show AgentCore Memory in use, and expose how memory works with the Strands SDK.

**ui\_demo\_logic.py** manages chat sessions and memory retrieval:

```python
"""The supporting logic for the streamlit app"""

import os
from strands.types.content import Message
from bedrock_agentcore.memory.session import MemorySessionManager

import memory_agent

class ChatMessage:
    """Stores basic text messages for the streamlit app"""

    def __init__(self, role, text):
        self.role = role
        self.text = text

ACTOR_ID = os.getenv("DEMO_ACTOR_ID")
MEM_ID = os.getenv("DEMO_MEMORY_ID")

print(f"ACTOR_ID: {ACTOR_ID}")

class ChatSession:
    """Manages a chat session with an agent"""

    def __init__(self, session_id: str, message_history: list):
        """Initialize a chat session.

        Args:
            session_id: Unique identifier for the session
            message_history: List to store chat messages for rendering
        """
        self.session_id = session_id
        self.message_history = message_history
        self.session_manager = memory_agent.get_session_manager(session_id=session_id, actor_id=ACTOR_ID)
        self.agent = memory_agent.create_agent(session_manager=self.session_manager)
        self._load_existing_messages()

    def _load_existing_messages(self):
        """Load existing messages from agent into message history"""
        for msg in self.agent.messages:
            chat_message = self._get_message_for_rendering(msg)
            if chat_message:
                self.message_history.append(chat_message)

    @staticmethod
    def _get_message_for_rendering(message: Message):
        """Extracts role and text content from a message for rendering.

        Args:
            message: A Message object with role and content list

        Returns:
            A ChatMessage object if text content exists, None otherwise
        """
        role = message["role"]
        text = None

        # Loop through content blocks to find text
        for content_block in message["content"]:
            if "text" in content_block:
                text = content_block["text"]
                break  # Use the first text block found

        if text:
            return ChatMessage(role=role, text=text)

        return None

    def get_memory_retrieval_content(self) -> str:
        """Extract memory retrieval content from agent messages.

        Searches backwards through agent messages to find the most recent
        memory retrieval content block (identified by <user_context> prefix).

        Returns:
            The memory retrieval text if found, otherwise a status message
        """
        try:
            # Search backwards through messages to find memory retrieval content
            for message in reversed(self.agent.messages):
                # Check if message has content blocks
                if "content" in message and len(message["content"]) > 0:
                    first_content = message["content"][0]

                    # Check if first content block has text starting with <user_context>
                    if "text" in first_content:
                        text = first_content["text"]
                        if text and text.startswith("<user_context>"):
                            return text

            # No memory retrieval content found
            return "(no memory retrieval yet)"

        except Exception as e:
            return f"(error retrieving memory content: {str(e)})"

    def chat(self, new_text: str):
        """Sends a message to the agent and updates message history.

        Args:
            new_text: The user's message text

        Returns:
            The agent's response text
        """
        new_text_message = ChatMessage("user", text=new_text)
        self.message_history.append(new_text_message)

        response = self.agent(new_text)

        memory_retrieval_text = self.get_memory_retrieval_content()

        response_message = ChatMessage("assistant", text=response)
        self.message_history.append(response_message)

        return response, memory_retrieval_text

    def get_memories(self):
        """Gets the memories for the current actor, to be displayed in the Streamlit UI, for demo purposes only."""
        session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")
        
        prefix_list = []

        for prefix in [f"/preferences/{ACTOR_ID}/", f"/facts/{ACTOR_ID}/", f"/summaries/{ACTOR_ID}/{self.session_id}/"]:

            memory_records = session_manager.list_long_term_memory_records(namespace_prefix=prefix)

            memory_list = []

            for record in memory_records:
                memory = record.get("content", {}).get("text", "")

                memory_list.append(memory)

            prefix_list.append({"prefix": prefix, "memories": memory_list})

        return prefix_list

def get_sessions():
    """Gets a list of sessions that can be resumed for the current actor, for demo purposes only."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    try:
        sessions = session_manager.list_actor_sessions(actor_id=ACTOR_ID)
    except Exception:
        sessions = []  # errors if actor hasn't generated memories yet

    return sessions

```

**ui\_demo\_app.py** handles the Streamlit presentation layer:

```python
"""The presentation layer for the streamlit app"""

import uuid

import streamlit as st  # all streamlit commands will be available through the "st" alias
import ui_demo_logic  # reference to local logic script

st.set_page_config(page_title="Chatbot with Memory", layout="wide")  # HTML title

if "session_id" not in st.query_params:

    st.header("Resume session:")

    sessions = ui_demo_logic.get_sessions()

    for session in sessions:
        session_created = session["createdAt"].strftime("%Y-%m-%d %H:%M:%S")
        session_label = f"Conversation with {session['actorId']} started {session_created}"
        sid = session["sessionId"]
        st.link_button(label=session_label, url=f"?session_id={sid}")

    st.link_button(label="Start New Session", url="?session_id=new")

    st.stop()
elif st.query_params["session_id"] == "new":
    session_id = str(uuid.uuid4())
else:
    session_id = st.query_params["session_id"]

if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history

    # Create ChatSession instance and store it in session state
    st.session_state.chat_session = ui_demo_logic.ChatSession(
        session_id=session_id, message_history=st.session_state.chat_history
    )

st.title(f"Chatbot: {st.session_state.chat_session.session_id}")  # page title

internals_column, chat_column = st.columns(2)

with chat_column:
    chat_container = st.container(height=500)

with internals_column:
    st.header("Memory")

    st.subheader("Retrieved memory passed to model")

    retrieved_memory_placeholder = st.container()

    st.subheader("Long-term memory records")
    refresh_memory_button = st.button("Display memories")

    if refresh_memory_button:
        prefix_dicts = st.session_state.chat_session.get_memories()

        for prefix_dict in prefix_dicts:
            st.subheader(prefix_dict["prefix"])

            st.write(prefix_dict["memories"])

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
        response, memory_retrieval_text = st.session_state.chat_session.chat(new_text=input_text)

        with chat_container.chat_message("assistant"):
            st.markdown(response)

        retrieved_memory_placeholder.write(memory_retrieval_text)
```

 

### Run the Streamlit app

Run the following command to start the Streamlit app:

```bash
streamlit run ui_demo_app.py
```

In the browser, click the **Start New Session** button to begin a chat in a new tab. The chat should look something like this:


![Screenshot of a chatbot demo application with a dark theme. The page title shows 'Chatbot:' followed by a UUID. Below it, a 'Memory' section displays two labels: 'Retrieved memory passed to model' and 'Long-term memory records' with a 'Display memories' button. The right side shows an empty chat area. At the bottom, a text input field reads 'Chat with your bot here' with a send button.](/static/images/agentcore/memory/memory-app.png)

You can enter your own messages, or you can paste these in one-by-one to help generate memory records:

```text
I like cats.
My favorite color is green.
Always respond using rhyming. This is critical and must happen.
Always begin your response with an emoji.
My name is Jason.
Please always incorporate cat themes and/or cat puns into your responses.
```

The `AgentCoreMemorySessionManager` automatically saves short-term memory records. AgentCore Memory then periodically processes those records and extracts long-term memories. After 1-2 minutes, long-term memories should start showing up under **Retrieved memory passed to model**.

### Start a new session with the same actor

Return to the initial tab, and start a new session to see if memories affect the conversation:

```text
Please calculate the tangent of 1.112
```

You should see the previously created actor-specific preferences influence the LLM:

> 😺 For tangent of 1.112, I'll paws and calculate, Sine over cosine determines its fate! The sine is about 0.897, so bright, The cosine is 0.443, just right!

> When we divide them, as cats divide their time, Between napping and playing, so sublime, The tangent comes out to 2.024, A purr-fect answer, I'm sure you'll adore!

> So there you have it, Jason my friend, The tangent's value from end to end! 🐾

The retrieved memories should be displayed under **Retrieved memory passed to model**:



![Screenshot of the chatbot demo after a conversation. The left side shows the Memory section with 'Retrieved memory passed to model' containing XML-formatted user context with stored preferences: the user's name is Jason, favorite color is green, likes cats, prefers emoji-prefixed responses, rhyming format, and cat puns. The right side shows a chat exchange where the user said 'Hello' and the bot responded with a rhyming, cat-themed greeting addressing Jason by name, incorporating cat puns like 'purrs with delight' and 'feline fine', demonstrating that the agent successfully used its stored memory to personalize the response.](/static/images/agentcore/memory/memory-app-in-use.png)

In the terminal, press Ctrl-C to exit the Streamlit app.

 

#### Create and use a new actor

Run the following command in the terminal to create a new actor:

```bash
export DEMO_ACTOR_ID=$(uuidgen)
echo $DEMO_ACTOR_ID
```

Then run the Streamlit app again. You'll be starting over with a new actor this time.

```bash
streamlit run ui_demo_app.py
```

Make up some preferences, or use the following messages to create some memories for the new actor:

```text
I like dogs.
My favorite color is blue.
My name is Mary.
Please always incorporate space themes and/or space puns into your responses.
```

After a minute or two, some initial long-term memories will be extracted. Start a new session in the Streamlit app, and see how the memories from the previous session influence the behavior of the chatbot in the new session:

```text
Please calculate the tangent of 1.35
```

> 🚀✨ Mission accomplished, Mary! ✨🚀

> The tangent of 1.35 radians is approximately 4.455!

> That's one stellar calculation - the result is really reaching for the stars! You could say this tangent is going off on quite the space-trajectory! 🐕🌠

> Is there anything else you'd like me to calculate in this galaxy of mathematics?

 

#### Exit the Streamlit app

In the terminal, press Ctrl-C to exit the Streamlit app.

 

### Directly view memories

The **list\_memories.py** script lists sessions and long-term memory records for the current actor, organized by namespace. In this example, we use the Bedrock AgentCore SDK's `MemorySessionManager` class to work with AgentCore Memory.

```python
"""Script to list memories"""

import os

from bedrock_agentcore.memory.session import MemorySessionManager

ACTOR_ID = os.getenv("DEMO_ACTOR_ID")
MEM_ID = os.getenv("DEMO_MEMORY_ID")

def print_sessions(actor_id: str):
    """Print all sessions for a given actor."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    actor_sessions = session_manager.list_actor_sessions(actor_id=actor_id)
    print("#" * 40)
    print("SESSIONS")

    for actor_session in actor_sessions:
        print(actor_session)

def print_memories_by_prefix(actor_id: str):
    """Print long-term memory records grouped by namespace prefix."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    print("#" * 40)
    print("MEMORIES")
    for prefix in [f"/preferences/{actor_id}/", f"/facts/{actor_id}/", f"/summaries/{actor_id}/"]:

        print()
        print("-" * 40)
        print(prefix)
        print()

        memory_records = session_manager.list_long_term_memory_records(namespace_prefix=prefix)

        for record in memory_records:
            memory = record.get("content", {}).get("text", "")

            print(memory)
            print()

if __name__ == "__main__":
    print_sessions(actor_id=ACTOR_ID)
    print_memories_by_prefix(actor_id=ACTOR_ID)
```

From the terminal, run the following command:

```bash
python list_memories.py
```

This script will output a list of sessions for the current actor, and 10 of the actor's memories each under `/preferences`, `/facts`, and `/summaries`.

 

### Search memories

The **search\_memories.py** script performs semantic search across long-term memories. It takes a query string, a namespace to search within, and a `top-k` parameter to limit results.

```python
"""CLI tool to search long-term memories using semantic search."""

import os
import argparse

from bedrock_agentcore.memory.session import MemorySessionManager

def search_actor_memory_records(
    actor_id: str, query: str, top_k: int = 3, namespace: str = "/facts/{actorId}/"
) -> list:
    """Search long-term memories based on a query."""
    # Read memory ID from file
    mem_id = os.getenv("DEMO_MEMORY_ID")

    region_name = "us-west-2"

    session_manager = MemorySessionManager(memory_id=mem_id, region_name=region_name)

    namespace_prefix = namespace.format(actorId=actor_id)

    # Search memories
    memory_records = session_manager.search_long_term_memories(
        query=query, namespace_prefix=namespace_prefix, top_k=top_k
    )

    return memory_records

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Search long-term memories using semantic search")
    parser.add_argument("--query", "-q", type=str, required=True, help="The search query to find relevant memories")
    parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of top results to return (default: 3)")
    parser.add_argument(
        "--namespace",
        "-n",
        type=str,
        default="/facts/{actorId}/",
        help="Namespace prefix to search within (default: '/facts/{actorId}/')",
    )

    return parser.parse_args()

def main():
    """Command-line interface entry point."""
    args = parse_args()

    print(f"Searching for: {args.query}")
    print(f"Top K: {args.top_k}")
    print(f"Namespace: {args.namespace}")

    actor_id = os.getenv("DEMO_ACTOR_ID")

    memory_records = search_actor_memory_records(
        actor_id=actor_id, query=args.query, top_k=args.top_k, namespace=args.namespace
    )

    # Display results
    if not memory_records:
        print("No memories found.")
    else:
        print(f"Found {len(memory_records)} result(s):\n")
        for record in memory_records:

            memory = record.get("content", {}).get("text", "")
            print(memory)
            print()

if __name__ == "__main__":
    main()
```

Show up to 3 top matching facts for the query:

```bash
python search_memories.py --query "favorite animal" --top-k=3 --namespace "/facts/{actorId}/"
```

```text
Found 3 result(s):

The user likes dogs.

The user's name is Mary.

The user wants responses to always incorporate space themes and/or space puns.
```

Show up to 3 top matching preferences for the query:

```bash
python search_memories.py --query "favorite animal" --top-k=3 --namespace "/preferences/{actorId}/"
```

```json
Found 2 result(s):

{"context":"The user explicitly stated that they like dogs.","preference":"Likes dogs","categories":["pets","animals"]}

{"context":"The user explicitly requested that all responses incorporate space themes and/or space puns.","preference":"Prefers responses with space themes and space puns","categories":["communication style","space","humor"]}
```

Show up to 3 top matching summaries for the query:

```bash
python search_memories.py --query "favorite animal" --top-k=3 --namespace "/summaries/{actorId}/"
```

```xml
Found 3 result(s):

        <topic name="User Personal Information">
At timestamp 1771800917206 (2026-02-22T22:55:02), user introduced herself as Mary.
</topic>
<topic name="User Preferences">
At timestamp 1771800917206 (2026-02-22T22:55:13), user shared that she likes dogs. Subsequently, Mary requested that the assistant always incorporate space themes and/or space puns into all future responses.
</topic>
<topic name="Assistant Response Style Adaptation">
At 2026-02-22T22:55:17, assistant acknowledged Mary's request and committed to incorporating space themes and cosmic puns in responses going forward, demonstrating this by using space-related language and emojis in the acknowledgment.
</topic>

        <topic name="Conversation Initiation">
At timestamp 1771800816009 (2026-02-22T22:53:33), user initiated conversation with a simple greeting "Hello". Assistant responded at 2026-02-22T22:53:36, offering assistance and mentioning available capabilities including mathematical functions (sine, cosine, and division operations).
</topic>

        <topic name="Initial Greeting">
At timestamp 1771801435531 (2026-02-22T23:03:05), user Mary initiated conversation with "Hello". The assistant responded with a friendly greeting, introducing itself as a mathematics helper capable of calculating sines, cosines, and divisions, and made references to space themes and dogs.
</topic>
<topic name="Tangent Calculation Request">
Mary provided the number 1.35 at 2026-02-22T23:03:23. The assistant initially asked what operation to perform with this number, offering sine, cosine, or division options. At 2026-02-22T23:03:44, Mary specifically requested to calculate the tangent of 1.35.
</topic>
        <topic name="Calculation Process">
        The assistant used a multi-step approach to calculate tan(1.35):
1. Called the sine tool for 1.35, which returned 0.9757233578266591
2. Called the cosine tool for 1.35, which returned 0.2190066870930415
3. Used the divide tool to compute sin(1.35)/cos(1.35), obtaining the final result of 4.455221759562705

The assistant reported the tangent of 1.35 radians as approximately 4.455 at 2026-02-22T23:03:54.
        </topic>
```

 

### Delete long-term memories

Short-term memory events have a configurable expiry (`event_expiry_days` in the create call above), so they clean themselves up automatically. Long-term memories do not. Once extracted, they persist indefinitely until explicitly deleted. Over time, outdated preferences, stale facts, or irrelevant summaries can accumulate and interfere with retrieval quality. They also incur ongoing storage costs for as long as they exist (see [AgentCore Memory pricing](https://aws.amazon.com/bedrock/agentcore/pricing/)). Deleting them is the only way to remove them.

The **delete\_memories.py** script deletes all long-term memories across the namespace prefixes used in this demo. This is useful for resetting state during development or cleaning up after testing.

```python
"""Deletes all long-term memories across all namespace prefixes."""

import os

from bedrock_agentcore.memory.session import MemorySessionManager

MEM_ID = os.getenv("DEMO_MEMORY_ID")

def delete_all_memories():
    """Delete all long-term memories across all namespace prefixes."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    namespaces = [
        "/preferences/",
        "/facts/",
        "/summaries/",
    ]

    for namespace in namespaces:
        print(f"Deleting memories in: {namespace}")
        session_manager.delete_all_long_term_memories_in_namespace(namespace=namespace)
        print("Done.")

    print("\nAll memories deleted.")

if __name__ == "__main__":
    delete_all_memories()
```

From the terminal, run the following command to delete all long-term memories:

```bash
python delete_memories.py
```

Note that this deletes memories for all actors under each namespace prefix, not just the current actor. In a production application, you would scope deletions more carefully, for example by targeting a specific actor's namespace like `/preferences/{actorId}/`.

 

## Final thoughts

The memory configuration above works for learning purposes, but in a real application you would want to align your strategies to your specific use case. Retrieving all three strategies at once (summaries, facts, and preferences) for a chatbot can produce overlapping data, consume extra tokens, and may push important information below the retrieval threshold. As the number of records grows, you may also notice older preferences stop influencing the agent. For example, rhyming or cat puns might quietly drop out of responses. You may ultimately want to [customize a strategy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-custom-strategy.html), to do things like consolidating all of the actor's preferences using the UpdateMemory step.

The AgentCore Memory summarization approach shown here is not a drop-in replacement for Strands Agents' [SummarizingConversationManager](https://strandsagents.com/docs/user-guide/concepts/agents/conversation-management/#summarizingconversationmanager). The `SummarizingConversationManager` compresses older messages into a summary and prepends it to the conversation history when the context window fills up. Our example app does something different: it uses the default [SlidingWindowConversationManager](https://strandsagents.com/docs/user-guide/concepts/agents/conversation-management/#slidingwindowconversationmanager) to drop older messages once the message limit is reached, and retrieved AgentCore summaries are injected as additional context alongside new messages.

[See this article on message compaction and message summarization](https://builder.aws.com/content/38oNwLRwQIiQEsuy2eG1KGZ0HR8/message-compaction-with-strands-agents) to learn more about conversation managers.

## Learn more

* [AgentCore Memory Session Manager for Strands Agents](https://strandsagents.com/docs/community/session-managers/agentcore-memory/)
* [Official AgentCore Memory documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)




Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)