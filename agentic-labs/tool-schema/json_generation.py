"ToolContext JSON generation example"

import json

from strands import ToolContext, tool, Agent


@tool(
    context=True,
    description="Generates product information based on the supplied content.",
    inputSchema={
        "json": {
            "properties": {
                "product_name": {"description": "The name of the product", "type": "string"},
                "items_per_package": {
                    "default": 1,
                    "description": "The number of items per package",
                    "type": "integer",
                },
                "weight_in_kilograms": {
                    "default": None,
                    "description": "Weight of product in kilograms.",
                    "type": "number",
                },
                "discontinued": {
                    "default": None,
                    "description": "Whether the product is discontinued",
                    "type": "boolean",
                },
            },
            "required": ["product_name"],
            "type": "object",
        }
    },
)
def extract_product_data(tool_context: ToolContext) -> str:

    product_json = json.dumps(tool_context.tool_use["input"], indent=4)

    # At this point you might save the product data to a database or route it for review
    print(product_json)

    return "Successfully extracted product data!"


PRODUCT_CONTENT = """
Product Specification Sheet

Product Name: UltraGrip Pro Wireless Mouse
Category: Computer Peripherals
Model: UGP-2024

Package Details:
- Items per package: 2 units (mouse + charging dock)
- Package dimensions: 25cm x 15cm x 8cm
- Weight: 0.85 kilograms total package weight

Product Status:
- Currently in production
- Available for retail distribution
- Not discontinued

Technical Specifications:
- Wireless connectivity: Bluetooth 5.2 and 2.4GHz USB receiver
- Battery life: Up to 90 days on single charge
- DPI range: 800-4000 adjustable
- Compatible with Windows, macOS, and Linux
"""

agent = Agent(
    system_prompt="Use the tool to extract product data from the product spec sheet",
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    tools=[extract_product_data],
)

agent(prompt=PRODUCT_CONTENT)
