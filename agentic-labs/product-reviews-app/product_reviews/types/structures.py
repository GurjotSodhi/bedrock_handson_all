"""Data structures for product review analysis."""

from typing import Literal, List
from pydantic import BaseModel, Field

# BEGIN CHALLENGE CONTENT: Create the ReviewAnalysis class ------------------------------------------------


class ReviewAnalysis(BaseModel):
    """Analysis results for a product review, including sentiment for different aspects."""


# END CHALLENGE CONTENT --------------------------------------------------------------------------------
