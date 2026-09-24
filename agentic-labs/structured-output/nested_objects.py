"""Nested objects example"""

from typing import List

from pydantic import BaseModel, Field

import agent_testing_utils


class Product(BaseModel):
    """Represents a product"""

    product_name: str = Field(description="The name of the product", min_length=1)


class FeatureRequest(BaseModel):
    """Represents a person"""

    feature_title: str = Field(description="The name of the requested feature", min_length=1)

    feature_description: str = Field(description="The description of the requested feature", min_length=1)

    primary_product: Product = Field("The primary product for the requested feature")

    related_products: List[Product] = Field("Other related products for the feature")

    additional_properties: dict = Field(
        description="Any additional custom properties for the project, as a series of key/value pairs"
    )


if __name__ == "__main__":

    feature_request_text = """I would like to request a new feature for AnyCompanyHeadphones.
I would like the headphones to automatically connect to my AnyCompanyPhone whenever I pick them up.
"""

    agent_testing_utils.display_and_test_structured_output(
        pydantic_class=FeatureRequest,
        prompt=feature_request_text,
        system_prompt="Analyze the feature request.",
    )
