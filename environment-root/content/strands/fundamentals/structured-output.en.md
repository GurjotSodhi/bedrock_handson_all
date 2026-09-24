---
title: "Structured output"
weight: 500
---




::::alert
This lab is based on the following article: [Structured output with Pydantic and Strands Agents](https://builder.aws.com/content/38oLeEDz9rpomVmcycQYCJtFBU0/structured-output-with-pydantic-and-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/structured-output**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/structured-output

```



## Introduction to structured output.

One of the most valuable capabilities of large language models is the ability to generate structured data from unstructured content. The unstructured content could be emails, social media posts, documents, images, meeting notes, videos, or anything else an LLM can understand. Conventional tool use allows you to both generate function parameters and structured JSON. But what if you want the LLM to generate structured data in line with a class definition, with validation, and have direct access to the output? This is where structured output is helpful.

**Structured output** is a special mode in Strands Agents (and some model providers) that allows you to define a data format for LLM-powered data extraction. Strands uses [Pydantic](https://docs.pydantic.dev/latest/) classes to define the data format.

To use structured output, you define a Python class that inherits from Pydantic's `BaseModel`, and pass it to your Strands agent with the `structured_output_model` parameter. Under the hood, Strands automatically converts your Pydantic model into a tool spec. We'll walk through what that looks like later in this section.

 

## A simple Pydantic class example

Here's a basic Pydantic class that can be used to generate structured output:

```python
from pydantic import BaseModel, Field
from strands import Agent

class EmailAnalysis(BaseModel):
    """The analysis of an email message"""
    one_line_summary: str = Field(description="One-line summary of the email", min_length=1)
    requires_urgent_response: bool = Field(
        description="Indicates if the email requires an immediate response", default=False
    )

```

In addition to inheriting from Pydantic's `BaseModel`, we also use Pydantic's `Field` class to set attributes' description, constraints, and defaults.

We can now pass that class to the agent using the `structured_output_model` parameter. In the below example, we just ask the LLM to make something up, but in real life you would pass an email message in the prompt.

```python
agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

result = agent("Generate a sample output using the tool.", structured_output_model=EmailAnalysis)
```

Then `result.structured_output` will be an object of type `EmailAnalysis`, and look something like this:

```python
EmailAnalysis(
    one_line_summary='Meeting rescheduled to Friday at 2 PM due to client availability conflict',
    requires_urgent_response=False
)
```

*Note: We can also pass* `structured_output_model` *to the* `Agent()` *constructor if we only plan to use that agent for structured output based on that class.*

Under the hood, the Pydantic class definition was converted into the tool schema below:

```json
{
    "name": "EmailAnalysis",
    "description": "The analysis of an email message",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "one_line_summary": {
                    "description": "One-line summary of the email",
                    "minLength": 1,
                    "title": "One Line Summary",
                    "type": "string"
                },
                "requires_urgent_response": {
                    "default": false,
                    "description": "Indicates if the email requires an immediate response",
                    "title": "Requires Urgent Response",
                    "type": [
                        "boolean",
                        "null"
                    ]
                }
            },
            "title": "EmailAnalysis",
            "description": "The analysis of an email message",
            "required": [
                "one_line_summary"
            ]
        }
    }
}
```

Note the following:

1. The class's docstring `"""The analysis of an email message"""` became the description of the tool schema. You'll want to be careful about what goes into your docstring, to minimize noise that can consume tokens and confuse the LLM.
2. Since `requires_urgent_response` has a default value, it was not included in the `required` section of the tool spec.

Now we'll walk through the core data types for Pydantic-based structured output.

 

## Common Pydantic field types

### bool

A simple true/false value. Maps to `boolean` in the tool spec. **default** is optional.

```python
is_correct_answer: bool = Field(
    description="Indicates whether this is the correct answer for the question",
)
```

Corresponding tool schema property:

```json
"is_correct_answer": {
    "description": "Indicates whether this is the correct answer for the question",
    "type": "boolean"
}
```

Sample object attribute in structured output:

```python
    is_correct_answer = True
```

 

### str

A string value. Maps to `string` in the tool spec. **min\_length** and **max\_length** are optional.

```python
article_title: str = Field(
    description="The title of the article", 
    min_length=1, 
    max_length=60
)
```

Corresponding tool schema property:

```json
"article_title": {
    "description": "The title of the article",
    "minLength": 1,
    "maxLength": 60,
    "type": "string"
}
```

Sample object attribute in structured output:

```python
    article_title = "Breaking: New AI Framework Revolutionizes Development"
```

 

### int

A whole number. Maps to `integer` in the tool spec. `ge` (greater or equal) and `le` (less or equal) are optional:

```python
estimated_star_rating: int = Field(
    description="The estimated star rating based on the review content, between 1 and 5", ge=1, le=5
)
```

You can alternatively set `gt` (greater than) or `lt` (less than) if that makes more sense for your use case.

Corresponding tool schema property:

```json
    "estimated_star_rating": {
        "description": "The estimated star rating based on the review content, between 1 and 5",
        "maximum": 5,
        "minimum": 1,
        "title": "Estimated Star Rating",
        "type": "integer"
    }
```

Sample object attribute in structured output:

```python
    estimated_star_rating=4
```

 

### float

A whole or floating-point number. Maps to `number` in the tool spec. `default`, `ge` (greater or equal), and `le` (less or equal) are optional.

```python
refund_request_amount: float = Field(description="The requested refund amount", default=None)
```

Like `int`, you can alternatively set "gt" or "lt" if that makes more sense for your use case.

Corresponding tool schema property:

```json
    "refund_request_amount": {
        "default": null,
        "description": "The requested refund amount",
        "title": "Refund Request Amount",
        "type": [
            "number",
            "null"
        ]
    },
```

Sample object attribute in structured output:

```python
    refund_request_amount=149.99
```

 

### Nested object

A nested object. This object's class should also inherit from `BaseModel`.

In the example below, the `project_creator` attribute is of type `Person`, a Pydantic class:

```python
class Person(BaseModel):
    """Represents a person"""

    person_name: str = Field(description="The name of the person", min_length=1)

```

```python
class SomeOtherClass(BaseModel):
    project_creator: Person = Field("The person who created the project")
```

Corresponding tool schema property:

```json
    "project_creator": {
        "type": [
            "object",
            "null"
        ],
        "description": "The project_creator",
        "properties": {
            "person_name": {
                "description": "The name of the person",
                "minLength": 1,
                "title": "Person Name",
                "type": "string"
            }
        },
        "required": [
            "person_name"
        ]
    },
```

Sample object attribute in structured output:

```python
    project_creator=Person(person_name='Sarah Johnson')
```

 

### List of primitives

An array of values. Maps to `array` in the tool spec. You can also constrain the number of list items through optional `min_length` and `max_length` arguments.

```python
mentioned_company_names: List[str] = Field(
    description="A list of all company names mentioned in the article",
)
```

Corresponding tool schema property:

```json
    "mentioned_company_names": {
        "description": "A list of all company names mentioned in the article",
        "items": {
            "type": "string"
        },
        "title": "Mentioned Company Names",
        "type": "array"
    },
```

Sample object attribute in structured output:

```python
    mentioned_company_names=['TechCorp', 'InnovateSoft', 'DataSystems Inc', 'CloudBase Solutions'],
```

 

### List of objects

An array of objects. Maps to `array` in the tool spec. You can also constrain the number of list items through optional `min_length` and `max_length` arguments.

```python
class GlossaryItem(BaseModel):
    """A listing within a glossary"""

    term: str = Field(
        description="The term. This could be a single word or a few words, depending on what needs to be defined.",
    )

    definition: str = Field(
        description="The definition for the term. This should be a very short description, 1-2 sentences in length.",
    )
```

```python
class SomeOtherClass(BaseModel):
    glossary_items: List[GlossaryItem] = Field(
        description="A collection of items to be included in the glossary",
        min_length=1,
        max_length=10
    )
```

Corresponding tool schema property:

```json
    "glossary_items": {
        "description": "A collection of items to be included in the glossary",
        "items": {
            "description": "A listing within a glossary",
            "title": "GlossaryItem",
            "type": "object",
            "properties": {
                "term": {
                    "description": "The term. This could be a single word or a few words, depending on what needs to be defined.",
                    "title": "Term",
                    "type": "string"
                },
                "definition": {
                    "description": "The definition for the term. This should be a very short description, 1-2 sentences in length.",
                    "title": "Definition",
                    "type": "string"
                }
            },
            "required": [
                "term",
                "definition"
            ]
        },
        "maxItems": 10,
        "minItems": 1,
        "title": "Glossary Items",
        "type": "array"
    }
```

Sample object attribute in structured output:

```python
glossary_items=[
    GlossaryItem(
        term='Machine Learning', 
        definition='A subset of artificial intelligence that enables systems to learn and improve from experience without explicit programming.'
    ),
    GlossaryItem(
        term='Microservices',
        definition='An architectural style that structures an application as a collection of loosely coupled services.'
    )
]

```

 

### Enum

Enums and literals are used to restrict allowed values within a list of options. Both map to `enum` in the tool spec. They can be numeric or strings, but strings are the most common type.

```python
class SentimentEnum(str, Enum):
    """Enumeration of possible sentiment values for a social media post."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class SocialMediaPost(BaseModel):
    post_summary: str = Field(description="The brief summary of the social media post")

    sentiment: SentimentEnum = Field(description="The author's sentiment towards our company")
```

Corresponding tool schema property:

```json
    "sentiment": {
        "description": "The author's sentiment towards our company",
        "enum": [
            "positive",
            "neutral",
            "negative"
        ],
        "title": "SentimentEnum",
        "type": "string"
    }
```

Sample object attribute in structured output:

```python
SocialMediaPost(
    post_summary='Customer praised the excellent customer service and fast delivery times',
    sentiment=<SentimentEnum.POSITIVE: 'positive'>
)
```

 

### Literal

Literals work in a similar way to Enums. The choice is really dependent on how your code processes the structured output. Ex: you have existing Enum definitions you want to use, or you have conditional logic based on enum values. Literals are nice for basic one-off constraints on values.

```python
SentimentLiteral = Literal["positive", "neutral", "negative"]

class SocialMediaPost2(BaseModel):
    post_summary: str = Field(description="The brief summary of the social media post")

    sentiment: SentimentLiteral = Field(description="The author's sentiment towards our company")
```

Corresponding tool schema property:

```json
    "sentiment": {
        "description": "The author's sentiment towards our company",
        "enum": [
            "positive",
            "neutral",
            "negative"
        ],
        "title": "Sentiment",
        "type": "string"
    }
```

Sample object attribute in structured output:

```python
SocialMediaPost2(
    post_summary='Customer praises excellent customer service and fast delivery',
    sentiment='positive'
)
```

 

## Code examples

The examples below require the [strands-agents](https://pypi.org/project/strands-agents/) package to be installed, and AWS access. [Pydantic](https://pypi.org/project/pydantic/) is automatically installed as a dependency for Strands Agents.

 

## Basic structured output pattern

At a minimum, structured output usage will look something like this:

```python
agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

result = agent("UNSTRUCTURED CONTENT GOES HERE", structured_output_model=MyPydanticClass)

object_instance_of_my_pydantic_class = result.structured_output
```

 

## Creating a script to help understand structured output class definitions

We'll use the **agent\_testing\_utils.py** module to show how structured output works. This script provides functions to display the generated tool specifications and test the agents.

A few things to note:

1. We reference the Strands SDK's `convert_pydantic_to_tool_spec` function from `strands.tools.structured_output.structured_output_utils` so we can see how Strands converts a Pydantic class to a tool spec.
2. We automatically create and invoke an agent using the indicated Pydantic class, then process the resulting `result.structured_output` property to view the extracted data.
3. The examples below will also show the messages that are part of the structured output generation.

```python
"""Testing utils for understanding Strands agents"""

import json
import textwrap
import pprint

from pydantic import BaseModel
from strands import Agent
from strands.tools.structured_output.structured_output_utils import convert_pydantic_to_tool_spec

def print_messages(messages):
    """Prints the formatted messages and content blocks from the agent"""
    for message in messages:
        message_role = message["role"]

        if message_role == "assistant":
            message_prefix = "\033[1;36m\n🤖"  # bold cyan
        else:
            message_prefix = "\033[1;33m\n🙂"  # bold yellow

        print(f"{message_prefix}{message_role}:\n")

        for content in message["content"]:
            for key, value in content.items():
                if isinstance(value, dict):
                    value = json.dumps(value, default=lambda n: "**UNSERIALIZABLE**")

                wrapped_line = textwrap.fill(text=f"    {key}: {value}", subsequent_indent="    ", width=79)
                print(wrapped_line)

def display_structured_output_tool_spec(pydantic_class: BaseModel):
    """Displays the generated tool spec based on the Pydantic class"""
    tool_spec = convert_pydantic_to_tool_spec(pydantic_class)

    print("STRUCTURED OUTPUT CLASS' TOOL SPEC:")
    print(json.dumps(tool_spec, indent=4))
    print("-" * 40)

def test_structured_output_result(
    pydantic_class: BaseModel, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Runs and displays the generated structured output for the Pydantic class"""
    agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0", system_prompt=system_prompt)
    result = agent(prompt, structured_output_model=pydantic_class)
    generated_output: pydantic_class = result.structured_output

    print("STRUCTURED OUTPUT RESULT:")
    pprint.pp(generated_output)
    print("-" * 40)

    print("STRUCTURED OUTPUT RESULT AS JSON:")
    print(generated_output.model_dump_json(indent=4))
    print("-" * 40)

    print_messages(agent.messages)

def display_and_test_structured_output(
    pydantic_class: BaseModel, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Displays and tests the tool spec and results for a Pydantic class"""
    display_structured_output_tool_spec(pydantic_class=pydantic_class)

    test_structured_output_result(pydantic_class=pydantic_class, prompt=prompt, system_prompt=system_prompt)

```

 

## Structured output example with basic types

The example below could take an emailed or messaged return request, and convert it into a format for automated processing.

Here's the code for **basic\_fields.py**:

```python
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

```

Run it:

```bash
python basic_fields.py
```

The Pydantic class is turned into this tool spec:

```json
{
    "name": "ReturnRequestAnalysis",
    "description": "The result of the product return request",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "one_line_summary": {
                    "description": "One-line summary of the request",
                    "title": "One Line Summary",
                    "type": "string"
                },
                "order_number": {
                    "type": [
                        "string",
                        "null"
                    ],
                    "description": "The order number"
                },
                "requires_translation": {
                    "description": "Indicate if this message is not in the processing team's language",
                    "title": "Requires Translation",
                    "type": "boolean"
                },
                "number_of_units_to_return": {
                    "default": 1,
                    "description": "The number of units to be returned",
                    "title": "Number Of Units To Return",
                    "type": [
                        "integer",
                        "null"
                    ]
                },
                "refund_request_amount": {
                    "default": null,
                    "description": "The requested refund amount",
                    "title": "Refund Request Amount",
                    "type": [
                        "number",
                        "null"
                    ]
                },
                "product_names": {
                    "description": "Product names that appear in the request",
                    "items": {
                        "type": "string"
                    },
                    "title": "Product Names",
                    "type": "array"
                }
            },
            "title": "ReturnRequestAnalysis",
            "description": "The result of the product return request",
            "required": [
                "one_line_summary",
                "requires_translation",
                "product_names"
            ]
        }
    }
}
```

And when called, returns this object:

```python
ReturnRequestAnalysis(
    one_line_summary='Customer wants to return defective AnyCompany WX99 wireless headphones with non-functioning left earpiece for full refund of $149.99', 
    order_number='901422', 
    requires_translation=True, 
    number_of_units_to_return=1, 
    refund_request_amount=149.99, 
    product_names=['AnyCompany WX99 wireless headphones']
)
```

 

## Structured output example with constraints

The example below could be used to process emails sent to a general inbox. We set constraints on fields using Enums, Literals, and length restrictions.

Here's the code for **constraints.py**:

```python
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

```

Run it:

```bash
python constraints.py
```

The Pydantic class is turned into this tool spec:

```json
{
    "name": "ExternalRequest",
    "description": "Represents a request from an external party",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "request_summary": {
                    "description": "The brief summary of the request",
                    "minLength": 1,
                    "title": "Request Summary",
                    "type": "string"
                },
                "urgency": {
                    "description": "The urgency of the request",
                    "enum": [
                        "low",
                        "medium",
                        "high"
                    ],
                    "title": "Urgency",
                    "type": "string"
                },
                "request_tags": {
                    "default": "The tags assigned to the request (select up to 3)",
                    "items": {
                        "enum": [
                            "customer-complaint",
                            "support-request",
                            "sales-opportunity",
                            "information-request",
                            "employment-inquiry"
                        ],
                        "type": "string"
                    },
                    "maxItems": 3,
                    "minItems": 0,
                    "title": "Request Tags",
                    "type": [
                        "array",
                        "null"
                    ]
                },
                "sentiment": {
                    "description": "The customer sentiment",
                    "enum": [
                        "positive",
                        "neutral",
                        "negative"
                    ],
                    "title": "SentimentEnum",
                    "type": "string"
                },
                "route_to_departments": {
                    "default": "The departments to route the message to (select up to 3)",
                    "items": {
                        "description": "Enumeration of departments that can handle external requests.",
                        "enum": [
                            "public-relations",
                            "investor-relations",
                            "customer-support",
                            "human-resources",
                            "sales",
                            "general-inbox"
                        ],
                        "title": "TargetDepartmentEnum",
                        "type": "string"
                    },
                    "maxItems": 3,
                    "minItems": 1,
                    "title": "Route To Departments",
                    "type": [
                        "array",
                        "null"
                    ]
                }
            },
            "title": "ExternalRequest",
            "description": "Represents a request from an external party",
            "required": [
                "request_summary",
                "urgency",
                "sentiment"
            ]
        }
    }
}
```

And when called, returns this object:

```python
ExternalRequest(
    request_summary='Customer on Basic plan needs more storage (25GB vs current 10GB limit) without upgrading to Enterprise, and experiencing mobile app sync issues between phone and desktop',
    urgency='medium', 
    request_tags=['customer-complaint', 'support-request', 'sales-opportunity'], 
    sentiment=<SentimentEnum.NEUTRAL: 'neutral'>, 
    route_to_departments=[<TargetDepartmentEnum.CUSTOMER_SUPPORT: 'customer-support'>, <TargetDepartmentEnum.SALES: 'sales'>]
)
```

 

## Structured output example with nested objects

The example below could be used to populate a structured feature request ticket based on a free-form submission.

Here's the code for **nested\_objects.py**:

```python
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

```

Run it:

```bash
python nested_objects.py
```

The Pydantic class is turned into this tool spec:

```json
{
    "name": "FeatureRequest",
    "description": "Represents a person",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "feature_title": {
                    "description": "The name of the requested feature",
                    "minLength": 1,
                    "title": "Feature Title",
                    "type": "string"
                },
                "feature_description": {
                    "description": "The description of the requested feature",
                    "minLength": 1,
                    "title": "Feature Description",
                    "type": "string"
                },
                "primary_product": {
                    "type": [
                        "object",
                        "null"
                    ],
                    "description": "The primary_product",
                    "properties": {
                        "product_name": {
                            "description": "The name of the product",
                            "minLength": 1,
                            "title": "Product Name",
                            "type": "string"
                        }
                    },
                    "required": [
                        "product_name"
                    ]
                },
                "related_products": {
                    "default": "Other related products for the feature",
                    "items": {
                        "description": "Represents a product",
                        "title": "Product",
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "description": "The name of the product",
                                "minLength": 1,
                                "title": "Product Name",
                                "type": "string"
                            }
                        },
                        "required": [
                            "product_name"
                        ]
                    },
                    "title": "Related Products",
                    "type": [
                        "array",
                        "null"
                    ]
                },
                "additional_properties": {
                    "additionalProperties": true,
                    "description": "Any additional custom properties for the project, as a series of key/value pairs",
                    "title": "Additional Properties",
                    "type": "object"
                }
            },
            "title": "FeatureRequest",
            "description": "Represents a person",
            "required": [
                "feature_title",
                "feature_description",
                "additional_properties"
            ]
        }
    }
}
```

And when called, returns this object:

```python
FeatureRequest(
    feature_title='Automatic Connection on Pickup', 
    feature_description='Enable the headphones to automatically connect to AnyCompanyPhone whenever the user picks them up, providing seamless connectivity without manual pairing.', 
    primary_product=Product(
        product_name='AnyCompanyHeadphones'
    ), 
    related_products=[Product(product_name='AnyCompanyPhone')], 
    additional_properties={'trigger_action': 'picking up headphones', 'target_device': 'AnyCompanyPhone', 'connection_type': 'automatic'}
    )
```

 

## Review of structured output field types and parameters

Here is a summary of the most common constructs used for structured output Pydantic class definitions:

#### Basic field types

* `str` - Text fields with optional `min_length`/`max_length` constraints
* `int`, `float` - Numeric fields with optional `ge`/`le` (greater/less than) constraints
* `bool` - Boolean true/false values
* `List[T]` - Arrays with optional `min_length`/`max_length` constraints
* `dict` - Flexible key-value objects for additional properties

#### Optional and default values

* `Optional[T]` - Fields that can be null/None
* `field: str = "default"` - Fields with default values
* `Field(default=None)` - Explicit default specification

#### Constraints and validation

* `Field(min_length=1, max_length=100)` - String length limits
* `Field(ge=0, le=100)` - Numeric range limits
* `Field(min_length=1, max_length=5)` - List size limits
* `Literal["option1", "option2"]` - Specific string choices
* `Enum` classes - Predefined value sets with descriptions

#### Complex structures

* Nested model classes for hierarchical data
* `List[T]` - Arrays of structured objects

#### Field and object descriptions

* `Field(description="")` - Guides the language model's understanding
* Model docstrings - Provide context for the overall structure

## Challenge yourself

1. **Named entity extraction**: Create a model that extracts people, organizations, and locations from news articles.
2. **Image analysis**: Design a structured output model that determines if an image matches a product listing's description, and what angle of the product it shows (side, front, top, etc.). Hint: you'll want to review the [Multimodal section](https://builder.aws.com/content/38oLhee2BEJ1MOZtdUEg69ERczc/multimodal-prompts-and-tools-with-strands-agents) first.

 



Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)

