"""Multimodal prompting example: document"""

from strands import Agent

import agent_testing_utils
from multimodal_helpers import MultimodalHelper

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

mmh = MultimodalHelper("local_files")

document_content = mmh.get_document_content_dict("test.pdf")

agent(
    [
        {"text": "Briefly describe what's in this document."},
        {"document": document_content},
    ]
)

agent_testing_utils.print_messages(agent.messages)
