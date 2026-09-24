"""Multimodal tool example: document"""

from typing import Annotated

from strands import Agent, tool

import agent_testing_utils
from multimodal_helpers import MultimodalHelper


@tool(description="Gets the content of a document")
def get_document(
    file_name: Annotated[str, "The file name including the extension"]
):
    """Tool to retrieve a document"""
    try:
        mmh = MultimodalHelper("local_files")
        document_content = mmh.get_document_content_dict(file_name)
        return {
            "status": "success",
            "content": [{"document": document_content}],
        }
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "content": [{"text": str(e)}],
        }


agent = Agent(tools=[get_document], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("Briefly describe what's in test.pdf")

agent_testing_utils.print_messages(agent.messages)
