"""A basic structured output example"""

from typing import Optional, List

from pydantic import BaseModel, Field

import agent_testing_utils


class ReturnRequestAnalysis(BaseModel):
    """The result of the product return request"""

    one_line_summary: str = Field(description="One-line summary of the request")

    order_number: Optional[str] = Field(description="The order number")

    requires_translation: bool = Field(description="Indicate if this message is not in the processing team's language")

    number_of_units_to_return: int = Field(description="The number of units to be returned", default=1)

    refund_request_amount: float = Field(description="The requested refund amount", default=None)

    product_names: List[str] = Field(description="Product names that appear in the request")


if __name__ == "__main__":

    return_request_text = """
I would like to return the AnyCompany WX99 wireless headphones I purchased last week (Order #901422).

The left earpiece stopped working after just 3 days of use.
I paid $149.99 for the item and would like a full refund of that amount.
The headphones are still in their original packaging with all accessories included.
Please let me know the return process and if you need any additional information from me.
"""

    agent_testing_utils.display_and_test_structured_output(
        pydantic_class=ReturnRequestAnalysis,
        prompt=return_request_text,
        system_prompt="Analyze the return request. The processing team's language is German.",
    )
