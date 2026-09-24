"""A basic structured output example"""

from typing import Optional, List, Literal
from enum import Enum

from pydantic import BaseModel, Field

import agent_testing_utils


class GlossaryItem(BaseModel):
    """A listing within a glossary"""

    term: str = Field(
        description="The term. This could be a single word or a few words, depending on what needs to be defined.",
    )

    definition: str = Field(
        description="The definition for the term. This should be a very short description, 1-2 sentences in length.",
    )


class Person(BaseModel):
    """Represents a person"""

    person_name: str = Field(description="The name of the person", min_length=1)


class SentimentEnum(str, Enum):
    """Enumeration of possible sentiment values for a social media post."""

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SocialMediaPost(BaseModel):
    post_summary: str = Field(description="The brief summary of the social media post")

    sentiment: SentimentEnum = Field(description="The author's sentiment towards our company")


SentimentLiteral = Literal["positive", "neutral", "negative"]


class SocialMediaPost2(BaseModel):
    post_summary: str = Field(description="The brief summary of the social media post")

    sentiment: SentimentLiteral = Field(description="The author's sentiment towards our company")


class TestModel(BaseModel):
    """The test model"""

    estimated_star_rating: int = Field(
        description="The estimated star rating based on the review content, between 1 and 5", ge=1, le=5
    )

    refund_request_amount: float = Field(description="The requested refund amount", default=None)

    project_creator: Person = Field("The person who created the project")

    mentioned_company_names: List[str] = Field(
        description="A list of all company names mentioned in the article",
    )

    glossary_items: List[GlossaryItem] = Field(
        description="A collection of items to be included in the glossary", min_length=1, max_length=10
    )



# agent_testing_utils.display_and_test_structured_output(
#     pydantic_class=TestModel,
#     prompt="Generate test data for the tool",
# )

agent_testing_utils.display_and_test_structured_output(
    pydantic_class=SocialMediaPost,
    prompt="Generate test data for the tool",
)

agent_testing_utils.display_and_test_structured_output(
    pydantic_class=SocialMediaPost2,
    prompt="Generate test data for the tool",
)

