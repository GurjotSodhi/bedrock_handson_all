"""Document message example"""
from strands import Agent

with open("local_files/test.pdf", "rb") as f:
    doc_bytes = f.read()

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent(
    [
        {"text": "Briefly describe what's in this document."},
        {
            "document": {
                "format": "pdf",
                "name": "test",
                "source": {
                    "bytes": doc_bytes
                }
            }
        }
    ]
)
