---
title: "Tool function decorators"
weight: 400
---

::::alert
This lab is based on the following article: [Tool function decorators for Strands Agents](https://builder.aws.com/content/38oLPJ7KYLglawz3dScA5q8H4XJ/tool-function-decorators-for-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/function-parameters**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/function-parameters

```



## Introduction: defining tool function parameters

When building agentic applications, you need to define tools that your AI agent can call. The Strands SDK makes this straightforward with its [tool function decorator](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/) that can turn functions into tools.

The decorated function's parameters become the tool's input schema. The agent will use the underlying input schema to know what data to pass to your tool.

Your parameters' names, data types, and annotations directly influence how well the agent can use your tools.

In this section, we'll explore how different parameter configurations translate into tool schemas.

 

### A simple example

Let's start with a simple tool created with the @tool decorator.

We use `Annotated` type hints to provide the data types and descriptions that help the LLM understand what each parameter represents. We use the `description` parameter of the @tool decorator to describe the tool in general.

```python
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

```

Strands will automatically generate the following tool spec based on the decorated `reverse_string` function:

```json
{
    "name": "reverse_string",
    "description": "Reverses a string",
    "inputSchema": {
        "json": {
            "properties": {
                "text_to_reverse": {
                    "description": "The text to reverse",
                    "type": "string"
                },
                "make_uppercase": {
                    "description": "Whether to make the reversed string uppercase.",
                    "type": "boolean"
                }
            },
            "required": [
                "text_to_reverse",
                "make_uppercase"
            ],
            "type": "object"
        }
    }
}
```

When the tool is called, the LLM will create a tool request that looks like this:

```json
    {
        "toolUse": {
            "toolUseId": "tooluse_MLS7OOCBQJ-iftqmwINgrw",
            "name": "reverse_string",
            "input": {
                "text_to_reverse": "Hello World",
                "make_uppercase": false
            }
        }
    }
```

Under the hood, you can think of Strands calling the function similar to this:

```python
result = reverse_string(text_to_reverse="Hello World", make_uppercase=False)
```

Then Strands will return the result to the LLM like this:

```json
    {
        "toolResult": {
            "toolUseId": "tooluse_MLS7OOCBQJ-iftqmwINgrw",
            "status": "success",
            "content": [
                {
                    "text": "dlroW olleH"
                }
            ]
        }
    }
```

Now we'll walk through the major data types you can use for tool function parameters.

 

## Data types for tool function parameters

### bool

A true/false value.

```python
    dark_mode: Annotated[bool, "Whether the image should have a dark background."],
```

Maps to a `boolean` type in the tool schema:

```json
    "dark_mode": {
        "description": "Whether the image should have a dark background.",
        "type": "boolean"
    }

```

 

### str

A string value.

```python
    text_to_draw: Annotated[str, "The text to draw in the image"],
```

Maps to a `string` type in the tool schema:

```json
    "text": {
        "description": "The text to draw in the image",
        "type": "string"
    },
```

 

### int

A whole number.

```python
    line_width: Annotated[int, "Width of the line in pixels"],
```

Maps to an `integer` type in the tool schema:

```json
    "line_width": {
        "description": "Width of the line in pixels",
        "type": "integer"
    },
```

 

### float

A whole or floating-point number.

```python
    text_x: Annotated[float, "The x coordinate of the text"],
```

Maps to a `number` type in the tool schema:

```json
    "text_x": {
        "description": "The x coordinate of the text",
        "type": "number"
    },
```

 

### list\[T]

An array of values of type `T`.

```python
    xy: Annotated[List[float], "List of x,y coordinates defining the line path"],
```

Maps to an `array` type in the tool schema. The `type` attribute under `items` indicates the type of the elements of the array:

```json
    "xy": {
        "description": "List of x,y coordinates defining the line path",
        "items": {
            "type": "number"
        },
        "type": "array"
    },
```

 

### literal

A list of allowed values for a parameter.

```python
    line_color: Annotated[Literal["red", "green", "blue", "yellow", "orange", "purple"], "Color of the line"],
```

Maps to the `enum` constraint for a tool schema property:

```json
    "line_color": {
        "description": "Color of the line",
        "enum": [
            "red",
            "green",
            "blue",
            "yellow",
            "orange",
            "purple"
        ],
        "type": "string"
    },
```

 

### dict

A dictionary of key-value pairs.

```python
    product_attributes: Annotated[dict, "The product attributes as key-value pairs"],
```

Maps to an `object` type in the tool schema:

```json
    "product_attributes": {
        "description": "The product attributes as key-value pairs",
        "type": "object"
    }
```

 

### Setting a default

A default value can be assigned to the function parameter:

```python
make_lowercase: Annotated[bool, "Whether to make the reversed string lowercase."] = False,
```

Maps to the `default` attribute for a tool schema property:

```json
    "make_lowercase": {
        "default": false,
        "description": "Whether to make the reversed string lowercase.",
        "type": "boolean"
    }

```

A field with a default value will also be excluded from the `"required"` array of the schema.

 

## Code examples

The examples below require the [strands-agents](https://pypi.org/project/strands-agents/) and [pillow](https://pypi.org/project/pillow/) packages to be installed, and AWS access.

 

### Creating a helper module

We'll use the **agent\_testing\_utils.py** module to show the details of the conversation:

```python
"""Testing utils for understanding Strands agents"""

import json
import textwrap

from strands import Agent
from strands.tools.decorator import DecoratedFunctionTool

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

def display_decorated_function_tool_spec(decorated_function: DecoratedFunctionTool):
    """Displays the generated tool spec based on the decorated function"""

    print("DECORATED FUNCTION'S TOOL SPEC:")
    print(json.dumps(decorated_function.tool_spec, indent=4))
    print("-" * 40)

def test_decorated_function_result(
    decorated_function: DecoratedFunctionTool, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Runs and displays the generated result for the decorated function"""

    agent = Agent(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0", system_prompt=system_prompt, tools=[decorated_function]
    )
    agent(prompt)

    print_messages(agent.messages)

def display_and_test_decorated_function(
    decorated_function: DecoratedFunctionTool, prompt="Please pass sample data to the tool", system_prompt=None
):
    """Displays and tests the tool spec and results for a decorated tool function"""
    display_decorated_function_tool_spec(decorated_function=decorated_function)

    test_decorated_function_result(decorated_function=decorated_function, prompt=prompt, system_prompt=system_prompt)

```

 

## Tool example with no parameters

Let's start with the simplest case - a tool that takes no parameters in **get\_date.py**:

```python
"""A tool with no parameters"""

from datetime import datetime, timezone

from strands import tool

import agent_testing_utils

@tool(description="Returns the current UTC date in ISO 8601 format")
def get_current_utc_date() -> str:
    """Tool to return current UTC date in "2025-01-30" format."""
    return datetime.now(timezone.utc).date().isoformat()

if __name__ == "__main__":
    agent_testing_utils.display_and_test_decorated_function(get_current_utc_date, prompt="What UTC date is it?")

```

Run it:

```bash
python get_date.py
```

The derived tool spec will look like this:

```json
{
    "name": "get_current_utc_date",
    "description": "Returns the current UTC date in ISO 8601 format",
    "inputSchema": {
        "json": {
            "properties": {},
            "type": "object"
        }
    }
}
```

And the conversation will look something like this:

```bash
🙂user:

    text: What UTC date is it?

🤖assistant:

    toolUse: {"toolUseId": "tooluse_WYPPJ7xoRXqJ12cSQn0qfw", "name":
    "get_current_utc_date", "input": {}}

🙂user:

    toolResult: {"toolUseId": "tooluse_WYPPJ7xoRXqJ12cSQn0qfw", "status":
    "success", "content": [{"text": "2025-12-14"}]}

🤖assistant:

    text: The current UTC date is **December 14, 2025**.
```

In this case, the `input` attribute will just be an empty dictionary, since the tool takes no parameters.

 

## Tool example with multiple data types

This example in **draw\_image.py** uses several types: lists, integers, strings, floats, booleans, and literals.

```python
"""Tool with basic types"""

import time
from typing import Annotated, List, Literal

from PIL import Image, ImageDraw, ImageColor
from strands import tool

import agent_testing_utils

@tool(description="Draws an image with a multi-segment line and text")
def draw_image_with_line_and_text(
    xy: Annotated[List[float], "List of x,y coordinates defining the line path"],
    line_width: Annotated[int, "Width of the line in pixels"],
    line_color: Annotated[Literal["red", "green", "blue", "yellow", "orange", "purple"], "Color of the line"],
    text: Annotated[str, "The text to draw in the image"],
    text_x: Annotated[float, "The x coordinate of the text"],
    text_y: Annotated[float, "The y coordinate of the text"],
    dark_mode: Annotated[bool, "Whether the image should have a dark background."],
):
    """The image drawing tool"""

    background_color = (0, 0, 0) if dark_mode else (255, 255, 255)

    im = Image.new("RGB", (200, 200), background_color)
    draw = ImageDraw.Draw(im)
    color = ImageColor.getrgb(line_color)

    draw.line(xy=xy, fill=color, width=line_width)

    text_color = (255, 255, 255) if dark_mode else 0

    draw.text(xy=(text_x, text_y), text=text, fill=text_color)

    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")

    im.save(f"line_drawing_{timestamp}.png", "PNG")

if __name__ == "__main__":
    agent_testing_utils.display_and_test_decorated_function(
        draw_image_with_line_and_text,
        system_prompt="You are a drawing assistant. You have a 200x200 canvas to work with. You can only use the tool one time.",
        prompt="Draw a haunted castle.",
    )

```

Run it:

```bash
python draw_image.py
```

The derived tool spec will look like this:

```json
{
    "name": "draw_image_with_line_and_text",
    "description": "Draws an image with a multi-segment line and text",
    "inputSchema": {
        "json": {
            "properties": {
                "xy": {
                    "description": "List of x,y coordinates defining the line path",
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
                },
                "line_width": {
                    "description": "Width of the line in pixels",
                    "type": "integer"
                },
                "line_color": {
                    "description": "Color of the line",
                    "enum": [
                        "red",
                        "green",
                        "blue",
                        "yellow",
                        "orange",
                        "purple"
                    ],
                    "type": "string"
                },
                "text": {
                    "description": "The text to draw in the image",
                    "type": "string"
                },
                "text_x": {
                    "description": "The x coordinate of the text",
                    "type": "number"
                },
                "text_y": {
                    "description": "The y coordinate of the text",
                    "type": "number"
                },
                "dark_mode": {
                    "description": "Whether the image should have a dark background.",
                    "type": "boolean"
                }
            },
            "required": [
                "xy",
                "line_width",
                "line_color",
                "text",
                "text_x",
                "text_y",
                "dark_mode"
            ],
            "type": "object"
        }
    }
}
```

And the conversation will look something like this:

```bash
🙂user:

    text: Draw a haunted castle.

🤖assistant:

    text: I'll draw a haunted castle for you using a multi-segment line to
    create the castle silhouette with some spooky text.
    toolUse: {"toolUseId": "tooluse_A2UerJg4SXigOPenqteFXw", "name":
    "draw_image_with_line_and_text", "input": {"xy": [20, 150, 20, 100, 40,
    100, 40, 80, 35, 80, 35, 60, 45, 60, 45, 80, 55, 80, 55, 100, 75, 100, 75,
    70, 70, 70, 70, 50, 80, 50, 80, 70, 85, 70, 85, 100, 105, 100, 105, 90,
    115, 90, 115, 100, 145, 100, 145, 90, 155, 90, 155, 100, 175, 100, 175, 70,
    170, 70, 170, 50, 180, 50, 180, 70, 185, 70, 185, 100, 205, 100, 205, 80,
    200, 80, 200, 60, 210, 60, 210, 80, 215, 80, 215, 100, 235, 100, 235, 150,
    20, 150], "line_width": 3, "line_color": "purple", "text": "HAUNTED",
    "text_x": 85, "text_y": 175, "dark_mode": true}}

🙂user:

    toolResult: {"toolUseId": "tooluse_A2UerJg4SXigOPenqteFXw", "status":
    "success", "content": [{"text": "None"}]}

🤖assistant:

    text: I've drawn a haunted castle for you! The image features a spooky
    purple castle silhouette on a dark background with multiple towers and
    turrets of varying heights, creating that classic haunted castle look. The
    word "HAUNTED" appears at the bottom to complete the eerie atmosphere. 🏰👻
```

And the generated image (in **line\_drawing\_...png**) could look something like this:


![A rudimentary drawing of a castle on a dark background](/static/images/agentic-fundamentals/decorator-parameters/haunted-castle.png)

*Note: This is at the edge of current-generation LLM capabilities, so you might not get as nice a picture. I happened to get lucky on the first try with this prompt.* [See more examples of drawing with LLMs in this article.](https://builder.aws.com/content/37UNhzA1lKjjLI0dKvgAxZIwLpo/creating-a-simple-line-drawing-agent-with-strands-agents)

 

## Tool example with a dictionary

You can use a `dict` data type to accept an arbitrary set of key-value pairs. Here is the code for **get\_attributes.py**. In this example, the LLM generates the data, and then you can choose to save that data or pass it along to a downstream system.

```python
"""A tool with a dict parameter"""

from typing import Annotated

from strands import tool

import agent_testing_utils

@tool(description="Generates a set of product attributes")
def get_product_attributes(
    product_attributes: Annotated[dict, "The product attributes as key-value pairs"],
) -> str:
    """Tool to collect a dictionary of product attributes."""

    # PLACEHOLDER: Save attributes to database or something
    _ = product_attributes

    return "Successfully saved the attributes."

if __name__ == "__main__":
    agent_testing_utils.display_and_test_decorated_function(get_product_attributes)

```

Run it:

```bash
python get_attributes.py
```

The derived tool spec will look like this:

```json
{
    "name": "get_product_attributes",
    "description": "Generates a set of product attributes",
    "inputSchema": {
        "json": {
            "properties": {
                "product_attributes": {
                    "description": "The product attributes as key-value pairs",
                    "type": "object"
                }
            },
            "required": [
                "attributes"
            ],
            "type": "object"
        }
    }
}
```

And the conversation will look something like this:

```bash
🙂user:

    text: Please pass sample data to the tool

🤖assistant:

    text: I'll generate a set of sample product attributes for you.
    toolUse: {"toolUseId": "tooluse_4xumgv_bSU2YSjdkjHguuQ", "name":
    "get_attributes", "input": {"attributes": {"product_name": "Wireless
    Bluetooth Headphones", "brand": "AudioTech", "color": "Black", "price":
    79.99, "in_stock": true, "category": "Electronics", "rating": 4.5,
    "warranty_years": 2, "features": ["Noise Cancelling", "30-hour battery",
    "Foldable design"], "weight_grams": 250}}}

🙂user:

    toolResult: {"toolUseId": "tooluse_4xumgv_bSU2YSjdkjHguuQ", "status":
    "success", "content": [{"text": "Successfully saved the attributes."}]}

🤖assistant:

    text: Perfect! I've successfully passed sample product attributes to the
    tool. The sample data included various types of attributes like: -
    **Product details**: name, brand, category - **Specifications**: features,
    color, weight - **Pricing**: price, rating - **Availability**: in_stock
    status - **Other**: warranty information  The function accepted the
    attributes and saved them successfully.
```

Notice that the `dict` parameter becomes an object with no properties in the schema.

 

## Challenge yourself

1. Create a tool that accepts two numbers, an operation ("add", "subtract", "multiply", "divide"), and whether to round the result.

 





Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)
