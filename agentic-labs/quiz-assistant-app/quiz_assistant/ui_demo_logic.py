"""The supporting logic for the streamlit app"""

import json

from quiz_assistant.agents import quiz_agent


class ChatMessage:
    """Stores basic text messages for the streamlit app"""

    def __init__(self, role, text):
        self.role = role
        self.text = text


agent = quiz_agent.create_quiz_agent()


def chat_with_agent(message_history, new_text=None):
    """Sends a message to the model"""

    new_text_message = ChatMessage("user", text=new_text)
    message_history.append(new_text_message)

    response = agent(new_text)

    response_message = ChatMessage("assistant", text=response)
    message_history.append(response_message)

    return response


def create_download_content(quiz: dict):
    """Creates JSON output file with quiz content"""

    return json.dumps(quiz, indent=4)
