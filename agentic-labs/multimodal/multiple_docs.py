"""Multiple docs example"""

from strands import Agent

import agent_testing_utils
from multimodal_helpers import MultimodalHelper

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

mmh = MultimodalHelper("local_files")

agent(
    [
        {"document": mmh.get_document_content_dict("test2.pdf")},
        {"document": mmh.get_document_content_dict("test.pdf")},
        {"text": "Briefly compare these documents."}
    ]
)

agent_testing_utils.print_messages(agent.messages)
