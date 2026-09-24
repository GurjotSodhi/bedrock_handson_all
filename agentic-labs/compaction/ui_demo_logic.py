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
