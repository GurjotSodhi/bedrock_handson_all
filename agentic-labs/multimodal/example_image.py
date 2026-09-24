"""Image message example"""
from strands import Agent

with open("local_files/test.png", "rb") as f:
    image_bytes = f.read()

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent(
    [
        {"text": "Briefly describe what's in this image."},
        {
            "image": {
                "format": "png",
                "source": {
                    "bytes": image_bytes
                }
            }
        }
    ]
)
