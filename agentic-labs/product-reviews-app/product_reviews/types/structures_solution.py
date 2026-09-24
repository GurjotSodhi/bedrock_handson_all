"""Data structures for product review analysis."""

from typing import Literal, List
from pydantic import BaseModel, Field

# BEGIN CHALLENGE CONTENT: Create the ReviewAnalysis class ------------------------------------------------


class ProductAspectSentiment(BaseModel):
    """Captures the consumer's sentiment towards an aspect of the product."""

    aspect_name: Literal["Taste", "Appearance", "Smell", "Nutrition", "Value"] = Field(
        description="The aspect of the product"
    )

    relevant_quote: str = Field(description="A relevant quote from the review towards this aspect")

    sentiment: Literal["positive", "negative"] = Field(description="The consumer's sentiment towards this aspect")


class ReviewAnalysis(BaseModel):
    """Analysis results for a product review, including sentiment for different aspects."""

    aspect_sentiments: List[ProductAspectSentiment] = Field(
        description="A list of the aspects of the product towards which the consumer has an identifiable sentiment"
    )

    estimated_star_rating: int = Field(
        description="The estimated star rating based on the review content, between 1 and 5", ge=1, le=5
    )


# END CHALLENGE CONTENT --------------------------------------------------------------------------------
