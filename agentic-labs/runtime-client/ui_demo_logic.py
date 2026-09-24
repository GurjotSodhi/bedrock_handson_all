"""The supporting logic for the streamlit app"""

import math_client


class ChatMessage:
    """Stores basic text messages for the streamlit app"""

    def __init__(self, role, text):
        self.role = role
        self.text = text


def chat_with_agent(message_history, session_id: str, new_text: str):
    """Sends a message to the model"""

    new_text_message = ChatMessage("user", text=new_text)
    message_history.append(new_text_message)

    result = math_client.invoke_agentcore_runtime(prompt=new_text, session_id=session_id)

    response = result.get("result")

    response_message = ChatMessage("assistant", text=response)
    message_history.append(response_message)

    return response
