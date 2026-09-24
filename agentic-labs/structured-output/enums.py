import pprint
from typing import Literal
from enum import Enum
from pydantic import BaseModel, Field
from strands import Agent

import agent_testing_utils


# agent_testing_utils.display_and_test_structured_output(pydantic_class=EmailAnalysis)


class SentimentEnum(str, Enum):
    """Enumeration of possible sentiment values for a social media post."""

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


SentimentLiteral = Literal["positive", "neutral", "negative"]

class SocialMediaPost(BaseModel):
    post_summary: str = Field(description="The brief summary of the social media post")

    sentiment1: SentimentEnum = Field(description="The author's sentiment towards our company")

    sentiment2: Literal["positive", "neutral", "negative"] = Field(
        description="The author's sentiment towards our company"
    )

    sentiment3: SentimentLiteral = Field(
        description="The author's sentiment towards our company"
    )


agent_testing_utils.display_structured_output_tool_spec(SocialMediaPost)
