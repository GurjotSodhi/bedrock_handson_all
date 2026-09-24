"""Reverse string tool example"""

from typing import Annotated

from strands import tool

import agent_testing_utils


@tool(description="Reverses a string")
def reverse_string(
    text_to_reverse: Annotated[str, "The text to reverse"],
    make_uppercase: Annotated[bool, "Whether to make the reversed string uppercase."],
) -> str:
    """Tool to reverse a string."""

    reversed_text = text_to_reverse[::-1]
    if make_uppercase:
        reversed_text = reversed_text.upper()

    return reversed_text


agent_testing_utils.display_and_test_decorated_function(reverse_string)
