---
title: "Tool schema"
weight: 300
---



::::alert
This lab is based on the following article: [JSON schema for Strands Agents tool definitions](https://builder.aws.com/content/38oLMHnkvCjaoGqlnEvJ5Ljnsj0/json-schema-for-strands-agents-tool-definitions)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/tool-schema**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/tool-schema

```


## Introduction: JSON Schema for agent tool definitions

In the [previous section on messages](https://builder.aws.com/content/38oLKU2chDabeIj8asnAd5eK5R5/messages-and-content-blocks-in-agentic-systems), we showed some simple tool definitions using basic type hints and function parameters. While a framework like Strands makes it easy to get started with the `@tool` decorator and function arguments or docstring-based tool definitions, understanding the underlying JSON Schema that gets generated is crucial for several reasons:

1. The JSON schema format is closely aligned to the tool definition format used by the LLM. This can be very helpful when troubleshooting a tool.
2. It's easy to make mistakes that impact the quality of a tool definition. For example, missing a field parameter annotation or having non-essential content in a docstring.
3. Using function arguments to define @tool parameters work well with basic data types (like int, float, string, list, and bool), but not as well with custom classes or other data types.
4. Function argument-based tool definition has no support for field value constraints beyond enums.

 

## JSON Schema overview

We can use JSON Schema to define our tools in Strands. This is the most powerful tool definition method, and is closest to the actual tool definitions sent to the LLM. In the following sections we'll review [simpler methods for defining tools](https://builder.aws.com/content/38oLPJ7KYLglawz3dScA5q8H4XJ/tool-function-decorators-for-strands-agents), but let's understand the underlying format first.

We'll start with a simple blueprint for a Strands tool defined with an `inputSchema` argument. Review the code and inline comments below:

```python
from strands import tool

@tool(  # converts the function into a tool that can be used by an agent
    description="Brief description of what your tool does",
    inputSchema={  # defines the expected structure of a tool use request made by an LLM
        "json": {  # the root of the tool definition schema
            "type": "object",  # always use the object type for the root schema
            "properties": {  # these properties map to the function's arguments
                "parameter_1": {  # Maps to the parameter_1: str argument in the function
                    "type": "string",  # Maps to the str type
                    "description": "Tells the LLM what this parameter is for",
                    # Add default and/or constraints here
                }
            },
            "required": ["parameter_1"],  # indicate the required fields here
        }
    },
)
def your_function(  # the function name becomes the name of the tool
    parameter_1: str,  # the function parameter names should map to the keys under "properties" in the tool definition
) -> str:  # return type will normally be either a simple type like a string or a number, or a dictionary
    result = parameter_1.upper()  # advanced custom tool logic in the function
    return f"Result: {result}"  # this is returned to the LLM to interpret the tool result

```

When the tool is called, the LLM will create a tool request that looks like this:

```json
{
    "toolUse": {
        "toolUseId": "tooluse_WSS0hHASShOWXgD3G2MYfw",
        "name": "your_function", 
        "input": {
            "parameter_1": "This is sample data for testing"
        }
    }
}
```

And under the hood, you can imagine Strands will call the function similar to this\*:

```python
result = your_function(parameter_1="This is sample data for testing")
```

*\* Not really - it's actually* [way fancier than that](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/tools/_caller.py)*. But this is close enough for our purposes.*

And then Strands will return the tool result to the LLM like this:

```json
{
    "toolResult": {
        "toolUseId": "tooluse_WSS0hHASShOWXgD3G2MYfw",
        "status": "success",
        "content": [
            { "text": "Result: THIS IS SAMPLE DATA FOR TESTING"}
        ]
    }
}
```

 

## Common JSON schema property types

Let's review the core data types for JSON Schema:

### boolean

A simple true/false value. Maps to `bool` in Python. `default` is optional:

```json
"shadow": {
    "type": "boolean",
    "description": "Whether to draw a shadow beneath the pie chart",
    "default": False,
},
```

This would map to a tool function parameter like this:

```python
shadow: bool = False,
```

 

### string

A string value. Maps to `str` in Python. `default`, `minLength`, and `maxLength` are optional:

```json
"pie_chart_title": {
    "type": "string",
    "description": "Title for the pie chart",
    "default": "My pie chart",
    "minLength": 2,
    "maxLength": 50
},
```

This would map to a tool function parameter like this:

```python
pie_chart_title: str = "My pie chart",
```

 

### integer

A whole number. Maps to `int` in Python. `default`, `minimum`, and `maximum` are optional:

```json
"startangle": {
    "type": "integer",
    "description": "The starting angle for the pie chart.", 
    "default": 0, 
    "minimum": 0,
    "maximum": 359
},
```

You can alternatively set "exclusiveMinimum" or "exclusiveMaximum" if that makes more sense for your use case.

This would map to a tool function parameter like this:

```python
startangle: int = 0,
```

 

### number

A whole or floating-point number. Maps to `float` in Python. `default`, `minimum`, and `maximum` are optional:

```json
 "x": {
    "type": "number",
    "description": "The value of x",
    "default": 0, 
    "minimum": 0,
    "maximum": 1000000
},
```

Like `integer`, you can alternatively set "exclusiveMinimum" or "exclusiveMaximum" if that makes more sense for your use case.

This would map to a tool function parameter like this:

```python
x: float = 0.0,
```

 

### object

An object with one or more of its own properties. `required` is optional, if no fields are required.

```json
"product_details": {
    "type": "object",
    "description": "Attributes about the product",
    "properties": {
        "product_name": {
            "description": "The name of the product",
            "type": "string"
        },
        "discontinued": {
            "type": "boolean",
            "description": "Whether the product is discontinued",
            "default": false,
        }
    },
    "required": ["product_name"]
},
```

This would map to a tool function parameter like this:

```python
product_details: dict
```

 

### array (of primitives)

An array of values. Maps to `list` in Python. The `items` element has a `type` property that indicates the type of the array's items, and can have its own constraints (like `minimum` of zero for pie slice values below). You can also constrain the number of array items through optional `minItems` and `maxItems` values.

Array of primitive types:

```json
"pie_slice_values": {
    "type": "array",
    "description": "List of numeric values for each pie slice",
    "items": {
        "type": "number",
        "minimum": 0
    },
    "minItems": 1,
    "maxItems": 15,
},
```

This would map to a tool function parameter like this:

```python
pie_slice_values: list[float]
```

 

### array of objects:

```json
    "to_do_list_items": {
        "type": "array",
        "description": "The list of to-do items",
        "items": {
            "type": "object",
            "description": "The to-do list item",
            "properties": {
                "to_do_item_title": {
                    "type": "string",
                    "description": "The title of the to-do item"
                },
                "to_do_item_details": {
                    "type": "string",
                    "description": "Details about the to-do item"
                }
            },
            "required": [
                "to_do_item_title"
            ]
        }
    }
```

This would map to a tool function parameter like this:

```python
to_do_list_items: list[dict]
```

 

Readability starts to suffer with nested objects or objects in arrays. With nested objects, you might want to break up your nested schema into separate dictionaries, and then reference that dictionary from the root schema definition.

### enum

Enums are a special type of constraint, to restrict allowed values within a list of options. Maps to `Literal` or `Enum` in Python. Enums can be numeric or strings, but strings are the most useful and common scenario.

```json
"product_size": {
    "type": "string",
    "description": "The size of the product",
    "enum": [
        "small",
        "medium",
        "large",
        "xlarge"
    ]
},
```

This would map to a tool function parameter like this:

```python
product_size: Literal["small", "medium", "large", "xlarge"]
```

 

## Using ToolContext for advanced tool use scenarios

Strands also support a special `context` parameter for the @tool decorator that allows you to access additional properties about the agent and tool call.

In the example below, we pass `context=True` to the tool decorator, which allows us to add an argument of type `ToolContext` to our function. We can use `tool_context.tool_use` to directly access the tool call inputs:

```python
@tool(
    context=True,
    description="Creates a new string by repeating a string a certain number of times",
    inputSchema={
        "json": {
            "properties": {
                "string_to_repeat": {
                    "type": "string",
                    "description": "The string to be repeated",
                    "minLength": 1,
                },
                "times_to_repeat": {
                    "type": "integer",
                    "description": "The number of times to repeat the string.",
                    "minimum": 0,
                },
            },
            "required": ["string_to_repeat", "times_to_repeat"],
        }
    },
)
def repeat_string(tool_context: ToolContext) -> str:

    print(tool_context.tool_use)

    string_to_repeat = tool_context.tool_use["input"]["string_to_repeat"]

    times_to_repeat = tool_context.tool_use["input"]["times_to_repeat"]

    resulting_string = string_to_repeat * times_to_repeat

    return {
        "status": "success",
        "content": [{"text": resulting_string}],
    }

```

While this is overkill for this specific scenario, this approach can be very handy when dealing with complex parameter types or advanced tool logic, where you just want direct access to the underlying dictionary of inputs.

See the Strands documentation for more on [ToolContext](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/#toolcontext)

 

## Code examples

The examples below require the [strands-agents](https://pypi.org/project/strands-agents/) and [matplotlib](https://pypi.org/project/matplotlib/) packages are installed, and AWS access.

 

### Creating a helper module

We'll use the **agent\_testing\_utils.py** module to show the details of the conversation, display the full tool spec, and test the tool with made-up parameters.

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

 

## Simple tool example: Square root tool

Let's start with a tool that calculates the square root of a number, in **square\_root\_tool.py**. This creates the tool, then uses the `display_and_test_decorated_function` function to test the tool with LLM-generated mock data.

```python
"""Square root tool schema example"""

import math

from strands import tool

import agent_testing_utils

@tool(
    description="Calculates the square root of x",
    inputSchema={
        "json": {
            "type": "object",
            "properties": {
                "x": {
                    "description": "The value of x",
                    "type": "number"
                }
            },
            "required": ["x"],
        }
    },
)
def square_root(x: float) -> float:
    return math.sqrt(x)

if __name__ == "__main__":
    agent_testing_utils.display_and_test_decorated_function(square_root)

```

Run it:

```bash
python square_root_tool.py
```

Sample output:

```bash
🙂user:

    text: Please pass sample data to the tool

🤖assistant:

    text: I will call the square_root function with some sample data.
    toolUse: {"toolUseId": "tooluse_Rg_GSgmeThyLRPJSofAZ9g", "name":
    "square_root", "input": {"x": 16}}

🙂user:

    toolResult: {"toolUseId": "tooluse_Rg_GSgmeThyLRPJSofAZ9g", "status":
    "success", "content": [{"text": "4.0"}]}

🤖assistant:

    text: Great! I called the `square_root` tool with the sample value of
    16, and it returned 4.0, which is correct since √16 = 4.  Would you like me
    to test it with other sample values?
```

The `x` parameter came through as expected, and the square root tool worked properly.

Let's try something a bit more involved now.

 

## Example with more data types: Pie chart tool

Now we'll create a pie chart generator tool that shows more parameter scenarios, including arrays and enums. This tool wraps the `pie` method from **matplotlib**. Below is the code for **pie\_chart\_tool.py**:

```python
"""Pie chart tool schema example"""

from typing import List

import matplotlib
import matplotlib.pyplot as plt
from strands import tool

import agent_testing_utils

@tool(
    description="Create a pie chart and save it as a PNG file.",
    inputSchema={
        "json": {
            "properties": {
                "title": {"description": "Title for the pie chart", "type": "string", "minLength": 2, "maxLength": 50},
                "labels": {
                    "description": "List of labels for each pie slice",
                    "items": {"type": "string", "minLength": 1},
                    "type": "array",
                    "minItems": 1,
                },
                "values": {
                    "description": "List of numeric values for each pie slice",
                    "items": {"type": "number", "minimum": 0},
                    "type": "array",
                    "minItems": 1,
                },
                "shadow": {
                    "default": False,
                    "description": "Whether to draw a shadow beneath the pie chart",
                    "type": "boolean",
                },
                "startangle": {"default": 0, "description": "The starting angle for the pie chart.", "type": "integer"},
                "color_sequence": {
                    "description": "The matplotlib color sequence for the chart",
                    "enum": ["tab10", "Pastel1", "Accent"],
                    "type": "string",
                    "default": "tab10",
                },
            },
            "required": ["title", "labels", "values"],
            "type": "object",
        }
    },
)
def create_pie_chart(
    title: str,
    labels: List[str],
    values: List[float],
    shadow: bool = False,
    startangle: int = 0,
    color_sequence: str = "tab10",
) -> str:
    """Pie chart tool"""

    matplotlib.use("agg")
    fig, ax = plt.subplots()

    colors = matplotlib.color_sequences.get(color_sequence, matplotlib.color_sequences["Pastel1"])

    ax.pie(values, labels=labels, autopct="%1.1f%%", shadow=shadow, startangle=startangle, colors=colors)
    ax.set_title(title)
    file_name = "pie_chart.png"
    fig.savefig(file_name)
    plt.close(fig)

    return f"Successfully created {file_name}!"

if __name__ == "__main__":
    agent_testing_utils.display_and_test_decorated_function(
        create_pie_chart, prompt="Create a pastel pie with some made-up data."
    )

```

Run it:

```bash
python pie_chart_tool.py
```

Sample output:

```bash
🙂user:

    text: Create a pastel pie with some made-up data.

🤖assistant:

    toolUse: {"toolUseId": "tooluse_4-EndB7JSQSxaw8uLlVNiA", "name":
    "create_pie_chart", "input": {"title": "Favorite Ice Cream Flavors",
    "labels": ["Vanilla", "Chocolate", "Strawberry", "Mint", "Cookie Dough"],
    "values": [30, 25, 20, 15, 10], "color_sequence": "Pastel1"}}

🙂user:

    toolResult: {"toolUseId": "tooluse_4-EndB7JSQSxaw8uLlVNiA", "status":
    "success", "content": [{"text": "Successfully created pie_chart.png!"}]}

🤖assistant:

    text: I've created a pastel-colored pie chart showing made-up data about
    favorite ice cream flavors! The chart has been saved as "pie_chart.png" and
    uses soft pastel colors to display the distribution across five flavors:
    Vanilla (30%), Chocolate (25%), Strawberry (20%), Mint (15%), and Cookie
    Dough (10%).
```

The tool creates a pie chart image like this and saves it to **pie\_chart.png**:


![A pie chart reflecting the data indicated above](/static/images/agentic-fundamentals/tool-schema/pie_chart.png)

You can also experiment with calling the agent directly to test other parameters:

```python
from strands import Agent
agent = Agent(tools=[create_pie_chart], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("""Create a pie chart for the population of the world by continent, based on your current best estimates.
Apply a shadow to the chart, and start at a 30 degree angle.""")
```

In this case, we see the shadow and the start angle applied, but we just use the default color scheme:


![A pie chart showing the continents and their percentage of the world's population](/static/images/agentic-fundamentals/tool-schema/continents_chart.png)

 

## Example with complex objects: To-do tool

Our final example demonstrates nested objects and arrays of objects. Here is the code for **to\_do\_tool.py**:

```python
"""To-do tool schema example"""

from strands import tool

import agent_testing_utils

@tool(
    description="Adds, updates, or deletes a to-do list",
    inputSchema={
        "json": {
            "properties": {
                "to_do_list_attributes": {  # Nested object
                    "type": "object",
                    "description": "Attributes about the to-do list and what kind of action to take",
                    "properties": {
                        "to_do_list_name": {"type": "string", "description": "The name of the to-do list"},
                        "to_do_list_action": {
                            "type": "string",
                            "description": "The action to take on the to-do list",
                            "enum": ["create", "update", "delete"],
                        },
                    },
                },
                "to_do_list_items": {
                    "type": "array",
                    "description": "The list of to-do items",
                    "items": {
                        "type": "object",
                        "description": "The to-do list item",
                        "properties": {
                            "to_do_item_title": {
                                "type": "string",
                                "description": "The title of the to-do item",
                            },
                            "to_do_item_details": {
                                "type": "string",
                                "description": "Details about the to-do item",
                            },
                        },
                        "required": ["to_do_item_title"],
                    },
                },
            },
            "required": ["to_do_list_attributes"],
        }
    },
)
def to_do_list_editor(to_do_list_attributes, to_do_list_items) -> str:
    """To-do list editor tool"""

    # Some logic here to retrieve or create a list, and save changes to a database.
    _ = (to_do_list_attributes, to_do_list_items)  # do something with these later

    return "List modified successfully!"

if __name__ == "__main__":
    agent_testing_utils.display_and_test_decorated_function(
        to_do_list_editor,
        prompt="Create a new to-do list called 'Winter prep'. Add items for calling the plow service and buying a shovel",
    )

```

Run it:

```bash
python to_do_tool.py
```

Sample output:

```bash
🙂user:

    text: Create a new to-do list called 'Winter prep'. Add items for calling
    the plow service and buying a shovel

🤖assistant:

    toolUse: {"toolUseId": "tooluse_DzYsqaPdT-mHsNmm3DIkYg", "name":
    "to_do_list_editor", "input": {"to_do_list_attributes":
    {"to_do_list_action": "create", "to_do_list_name": "Winter prep"},
    "to_do_list_items": [{"to_do_item_title": "Call the plow service"},
    {"to_do_item_title": "Buy a shovel"}]}}

🙂user:

    toolResult: {"toolUseId": "tooluse_DzYsqaPdT-mHsNmm3DIkYg", "status":
    "success", "content": [{"text": "List modified successfully!"}]}

🤖assistant:

    text: I've successfully created a new to-do list called "Winter prep" with
    two items: 1. Call the plow service 2. Buy a shovel  Your winter
    preparation list is ready to go!
```

 

## Using ToolContext for JSON generation

ToolContext can also be helpful if all you want is the JSON generated by the LLM when calling the tool.

Here is the code for **json\_generation.py**:

```python
"ToolContext JSON generation example"

import json

from strands import ToolContext, tool, Agent

@tool(
    context=True,
    description="Generates product information based on the supplied content.",
    inputSchema={
        "json": {
            "properties": {
                "product_name": {"description": "The name of the product", "type": "string"},
                "items_per_package": {
                    "default": 1,
                    "description": "The number of items per package",
                    "type": "integer",
                },
                "weight_in_kilograms": {
                    "default": None,
                    "description": "Weight of product in kilograms.",
                    "type": "number",
                },
                "discontinued": {
                    "default": None,
                    "description": "Whether the product is discontinued",
                    "type": "boolean",
                },
            },
            "required": ["product_name"],
            "type": "object",
        }
    },
)
def extract_product_data(tool_context: ToolContext) -> str:

    product_json = json.dumps(tool_context.tool_use["input"], indent=4)

    # At this point you might save the product data to a database or route it for review
    print(product_json)

    return "Successfully extracted product data!"

if __name__ == "__main__":
    PRODUCT_CONTENT = """
    Product Specification Sheet

    Product Name: UltraGrip Pro Wireless Mouse
    Category: Computer Peripherals
    Model: UGP-2024

    Package Details:
    - Items per package: 2 units (mouse + charging dock)
    - Package dimensions: 25cm x 15cm x 8cm
    - Weight: 0.85 kilograms total package weight

    Product Status:
    - Currently in production
    - Available for retail distribution
    - Not discontinued

    Technical Specifications:
    - Wireless connectivity: Bluetooth 5.2 and 2.4GHz USB receiver
    - Battery life: Up to 90 days on single charge
    - DPI range: 800-4000 adjustable
    - Compatible with Windows, macOS, and Linux
    """

    agent = Agent(
        system_prompt="Use the tool to extract product data from the product spec sheet",
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        tools=[extract_product_data],
    )

    agent(prompt=PRODUCT_CONTENT)

```

Run it:

```bash
python json_generation.py
```

This will print the following JSON based on `PRODUCT_CONTENT`:

```json
{
    "product_name": "UltraGrip Pro Wireless Mouse",
    "items_per_package": 2,
    "weight_in_kilograms": 0.85,
    "discontinued": false
}
```

You can also use structured output to extract data from unstructured content. We'll cover that in a [later section](https://builder.aws.com/content/38oLeEDz9rpomVmcycQYCJtFBU0/structured-output-with-pydantic-and-strands-agents).

 

## Challenge yourself

1. Review the [matplotlib library](https://matplotlib.org/stable/api/pyplot_summary.html) and try creating a `create_bar_chart` tool. How does its parameters differ from the pie chart tool?

 

### Learn more about JSON Schema

We covered the majority of useful JSON Schema elements for tool use above, but you can review the [JSON Schema reference](https://json-schema.org/understanding-json-schema/reference/type) to learn more.

 



Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)
