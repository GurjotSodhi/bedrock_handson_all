"""A tool with a dict parameter"""

from typing import Annotated

from strands import tool

import agent_testing_utils


@tool(description="Generates a set of product attributes")
def get_product_attributes(
    product_attributes: Annotated[dict, "The product attributes as key-value pairs"],
) -> str:
    """Tool to collect a dictionary of product attributes."""

    # Save attributes to database or something
    _ = product_attributes

    return "Successfully saved the attributes."


agent_testing_utils.display_and_test_decorated_function(get_product_attributes)
