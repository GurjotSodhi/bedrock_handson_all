"""Default value tool example"""

from typing import Annotated

from strands import tool

import agent_testing_utils


@tool(description="Reverses a string")
def reverse_string(
    text_to_reverse: Annotated[str, "The text to reverse"],
    make_lowercase: Annotated[bool, "Whether to make the reversed string lowercase."] = False,
) -> str:
    """Tool to reverse a string."""

    reversed_text = text_to_reverse[::-1]
    if make_lowercase:
        reversed_text = reversed_text.lower()

    return reversed_text


agent_testing_utils.display_and_test_decorated_function(reverse_string)
