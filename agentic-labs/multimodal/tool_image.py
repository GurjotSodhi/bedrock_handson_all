"""Multimodal tool example: image"""

from typing import Annotated

from strands import Agent, tool

import agent_testing_utils
from multimodal_helpers import MultimodalHelper


@tool(description="Gets the content of an image")
def get_image(
    file_name: Annotated[str, "The file name including the extension"]
):
    """Tool to retrieve an image"""
    try:
        mmh = MultimodalHelper("local_files")
        image_content = mmh.get_image_content_dict(file_name)
        return {
            "status": "success",
            "content": [{"image": image_content}],
        }
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "content": [{"text": str(e)}],
        }


agent = Agent(tools=[get_image], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("Briefly describe what's in test.png")

agent_testing_utils.print_messages(agent.messages)
