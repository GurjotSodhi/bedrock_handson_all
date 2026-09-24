"""Multimodal prompting example: image"""

from strands import Agent

import agent_testing_utils
from multimodal_helpers import MultimodalHelper

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

mmh = MultimodalHelper("local_files")

image_content = mmh.get_image_content_dict("test.png")

agent(
    [
        {"text": "Briefly describe what's in this image."},
        {"image": image_content},
    ]
)

agent_testing_utils.print_messages(agent.messages)
