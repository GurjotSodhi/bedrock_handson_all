"""Constraints example with enums and validation"""

from enum import Enum
from typing import List, Literal
from pydantic import BaseModel, Field

import agent_testing_utils


class SentimentEnum(str, Enum):
    """Enumeration of possible sentiment values for external requests."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TargetDepartmentEnum(str, Enum):
    """Enumeration of departments that can handle external requests."""
    PUBLIC_RELATIONS = "public-relations"
    INVESTOR_RELATIONS = "investor-relations"
    CUSTOMER_SUPPORT = "customer-support"
    HUMAN_RESOURCES = "human-resources"
    SALES = "sales"
    GENERAL_INBOX = "general-inbox"


class ExternalRequest(BaseModel):
    """Represents a request from an external party"""

    request_summary: str = Field(description="The brief summary of the request", min_length=1)

    urgency: Literal["low", "medium", "high"] = Field(description="The urgency of the request")

    request_tags: List[
        Literal[
            "customer-complaint", "support-request", "sales-opportunity", "information-request", "employment-inquiry"
        ]
    ] = Field("The tags assigned to the request (select up to 3)", min_length=0, max_length=3)

    sentiment: SentimentEnum = Field(description="The customer sentiment")

    route_to_departments: List[TargetDepartmentEnum] = Field(
        "The departments to route the message to (select up to 3)", min_length=1, max_length=3
    )


if __name__ == "__main__":

    external_request_text = """
Hi there,

I'm currently using your Basic plan but I'm hitting the 10GB storage
limit every month.

Is there a way to get more storage without upgrading to Enterprise?
The Enterprise plan seems like overkill for my small business,
but I really need about 25GB of storage.

Also, I've been having some sync issues with the mobile app -
files aren't updating properly between my phone and desktop.

Thanks,
Mike Green
"""

    agent_testing_utils.display_and_test_structured_output(
        pydantic_class=ExternalRequest,
        prompt=external_request_text,
        system_prompt="Analyze the external request.",
    )
