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
