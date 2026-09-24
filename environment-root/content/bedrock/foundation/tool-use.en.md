---
title : "Lab F-5: Tool use"
weight : 10600
---


# Lab introduction

In this lab, we will walk through a simple tool use example to illustrate how it works. Later labs will dive into more advanced use cases including JSON generation.

The Converse API provides a consistent way to access large language models (LLMs) on Amazon Bedrock. It supports turn-based messages between the user and the generative AI model. It also provides a consistent format for tool definitions for the models that support tool use (aka "function calling").

**Tool use** is a capability that allows a large language model to tell the calling application to invoke a function with parameters supplied by the model. The available functions and supported parameters are passed to the model along with a prompt. It's important to note that the large language model does not call a function itself - it just returns JSON and lets the calling application do the rest.

Why is native tool use so important? Because now we get built-in support for turning free-form content into automation-friendly and analytics-friendly structured data. While advanced prompt engineers had some success manually building tool use applications with existing large language models, it was often brittle, or XML-based, or susceptible to creating invalid JSON.

Tool Use with the Amazon Bedrock Converse API follows these steps:

1. The calling application passes (A) tool definitions and (B) a triggering message to the large language model.
2. If the request matches a tool definition, the model generates a tool use request, including the parameters to pass to the tool.
4. The calling application extracts the parameters from the model’s tool use request and passes them to the corresponding local function for the tool.
4. The calling application can then either use the tool result directly, or pass the tool result back to the model to get a follow-on response.
5. The model either returns a final response, or requests another tool.


::alert[Not every model supports all of the capabilities of the Converse API, so it’s important to review the [supported model features](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-supported-models-features) in the official documentation.]{header="Note" type="info"}


# Code walkthrough: tool use with the Amazon Bedrock Converse API

We'll be writing a Python script that you can run from the command line. We will demonstrate basic tool definition, passing generated parameters to a function, returning a tool result to the model, and error handling.


## Create the Python script


1. Navigate to the **workshop/labs/tool_use** folder, and open the file **tool_use.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)

&nbsp;




## Defining a tool and sending a message that will make Claude ask for tool use

Let’s start by defining a cosine tool using the Converse API tool definition format. You can learn more about the tool definition format here: https://community.aws/content/2hWA16FSt2bIzKs0Z1fgJBwu589/generating-json-with-the-amazon-bedrock-converse-api

We’ll then create a simple message to trigger the tool use request and add it to an empty list of messages. We’re creating a message from the “user” role. Within that message, we can include a list of content blocks. In this example, we have a single `text` content block where we ask the model to "What is the cosine of 7?"

We’re now ready to pass the tool definition and message to Amazon Bedrock. We specify Anthropic’s Claude 3 Sonnet as the target model. We can limit the number of tokens in the model’s response by setting the `maxTokens` value. We also set the `temperature` to zero to minimize the variability of responses.

Note that we set a system message here so that Claude won’t attempt to do any math itself. The current generation of large language models cannot reliably do math.



2. Use the copy button in the box below to automatically copy its code, then paste it into the **tool_use.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3, json, math

print("\n----Defining a tool and sending a message that will make Claude ask for tool use----\n")

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

tool_list = [
    {
        "toolSpec": {
            "name": "cosine",
            "description": "Calculate the cosine of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function."
                        }
                    },
                    "required": ["x"]
                }
            }
        }
    }
]

message_list = []

initial_message = {
    "role": "user",
    "content": [
        { "text": "What is the cosine of 7?" } 
    ],
}

message_list.append(initial_message)

response = bedrock.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=message_list,
    inferenceConfig={
        "maxTokens": 2000,
    },
    toolConfig={
        "tools": tool_list
    },
    system=[{"text":"You must only do math by using a tool."}]
)

response_message = response['output']['message']
print(json.dumps(response_message, indent=4))
message_list.append(response_message)


::::

This will generate a response similar to the following:

::::code{showCopyAction=false language="json" showLineNumbers=false}
{
    "role": "assistant",
    "content": [
        {
            "text": "Here is how we can calculate the cosine of 7 using the available tool:"
        },
        {
            "toolUse": {
                "toolUseId": "tooluse_xH3ljaGCQwGqx2wdlG8dnA",
                "name": "cosine",
                "input": {
                    "x": 7
                }
            }
        }
    ]
}
::::


There are a few things to note here:

* In this case, Claude also generated some text prefacing its tool use request. Claude will only do this some of the time. Sometimes it just generates a tool use request with no text accompanying it.
* The toolUse block includes a toolUseId. You can use the toolUseId to help Claude connect the initial tool request with a corresponding tool result you send back to Claude for additional processing.
* The toolUse block includes the tool name to invoke, in this case `cosine`.
* The `input` property contains the JSON structure of arguments to pass to the tool. You can also use this JSON directly. In this case, Claude is asking the calling application to pass the `cosine` function an argument `x` with value `7`.

## Calling a function based on the toolUse content block.

We’ll now loop through the response message’s content blocks. We’ll use the cosine tool if requested, and print any text content blocks from the LLM’s message.


3. Use the copy button in the box below to automatically copy its code, then paste it into the **tool_use.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Calling a function based on the toolUse content block.----\n")

response_content_blocks = response_message['content']

for content_block in response_content_blocks:
    if 'toolUse' in content_block:
        tool_use_block = content_block['toolUse']
        tool_use_name = tool_use_block['name']
        
        print(f"Using tool {tool_use_name}")
        
        if tool_use_name == 'cosine':
            tool_result_value = math.cos(tool_use_block['input']['x'])
            print(tool_result_value)
            
    elif 'text' in content_block:
        print(content_block['text'])


::::

This will generate a response similar to the following:

::::code{showCopyAction=false language="text" showLineNumbers=false}
Here is how we can calculate the cosine of 7 using the available tool:
Using tool cosine
0.7539022543433046
::::


The above pattern might be totally adequate for your use case. If you don't need to pass the tool result back to Claude, then you can just have your application proceed with the direct tool call result. In the next section, we will send a follow-up request to Claude to get a final response.

## Passing the tool result back to Claude

Now we’ll loop through the content blocks from the response message, and check for a tool use request. If there’s a tool use request, we’ll call the named tool and pass it the input parameters provided by Claude. We’ll then build a message with a `toolResult` content block to send back to Claude for a final response.


4. Use the copy button in the box below to automatically copy its code, then paste it into the **tool_use.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Passing the tool result back to Claude----\n")

follow_up_content_blocks = []

for content_block in response_content_blocks:
    if 'toolUse' in content_block:
        tool_use_block = content_block['toolUse']
        tool_use_name = tool_use_block['name']
        
        
        if tool_use_name == 'cosine':
            tool_result_value = math.cos(tool_use_block['input']['x'])
            
            follow_up_content_blocks.append({
                "toolResult": {
                    "toolUseId": tool_use_block['toolUseId'],
                    "content": [
                        {
                            "json": {
                                "result": tool_result_value
                            }
                        }
                    ]
                }
            })

if len(follow_up_content_blocks) > 0:
    
    follow_up_message = {
        "role": "user",
        "content": follow_up_content_blocks,
    }
    
    message_list.append(follow_up_message)

    response = bedrock.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=message_list,
        inferenceConfig={
            "maxTokens": 2000,
        },
        toolConfig={
            "tools": tool_list
        },
        system=[{"text":"You must only do math by using a tool."}]
    )
    
    response_message = response['output']['message']
    
    message_list.append(response_message)
    print(json.dumps(message_list, indent=4))


::::

This will generate a response similar to the following:

::::code{showCopyAction=false language="json" showLineNumbers=false}
[
    {
        "role": "user",
        "content": [
            {
                "text": "What is the cosine of 7?"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "text": "Here is how we can calculate the cosine of 7 using the available tool:"
            },
            {
                "toolUse": {
                    "toolUseId": "tooluse_ohIdXqhRTWOeQphBAGqa_Q",
                    "name": "cosine",
                    "input": {
                        "x": 7
                    }
                }
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": "tooluse_ohIdXqhRTWOeQphBAGqa_Q",
                    "content": [
                        {
                            "json": {
                                "result": 0.7539022543433046
                            }
                        }
                    ]
                }
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "text": "So the cosine of 7 is 0.7539022543433046."
            }
        ]
    }
]
::::


Great! That’s worked so far. But what happens when tool use fails?

## Error handling - letting Claude know that tool use failed

Now we’re going to take a step back and manufacture an error to send back to the LLM. We set the `status` attribute to `error` so that Claude can decide what to do next.




5. Use the copy button in the box below to automatically copy its code, then paste it into the **tool_use.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Error handling - letting Claude know that tool use failed----\n")

del message_list[-2:] #Remove the last request and response messages

content_block = next((block for block in response_content_blocks if 'toolUse' in block), None)

if content_block:
    tool_use_block = content_block['toolUse']
    
    error_tool_result = {
        "toolResult": {
            "toolUseId": tool_use_block['toolUseId'],
            "content": [
                {
                    "text": "invalid function: cosine"
                }
            ],
            "status": "error"
        }
    }
    
    follow_up_message = {
        "role": "user",
        "content": [error_tool_result],
    }
    
    message_list.append(follow_up_message)
    
    response = bedrock.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=message_list,
        inferenceConfig={
            "maxTokens": 2000,
        },
        toolConfig={
            "tools": tool_list
        },
        system=[{"text":"You must only do math by using a tool."}]
    )
    
    response_message = response['output']['message']
    print(json.dumps(response_message, indent=4))
    message_list.append(response_message)


::::
    
This will generate a response similar to the following:

::::code{showCopyAction=false language="json" showLineNumbers=false}
{
    "role": "assistant",
    "content": [
        {
            "text": "Apologies, it seems the \"cosine\" tool is not available in this environment. Without access to mathematical functions, I cannot directly calculate the cosine of 7. As an AI assistant without built-in math capabilities, I do not have a way to compute trigonometric functions like cosine from first principles. I should have acknowledged the limitations of the available tools upfront. Please let me know if there are any other tasks I can assist with within the provided toolset."
        }
    ]
}
::::


So in this case, Claude is out of options and has to give up on the tool request.





&nbsp;

6. Save the file.

Great! Now you are ready to run the script!

&nbsp;

# Run the script

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/tool_use

::::



&nbsp;

2. Run the script from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 tool_use.py

::::



&nbsp;

3. The results should be displayed in the terminal.



---

&nbsp;





::alert[You have successfully demonstrated tool use with the Amazon Bedrock Converse API!]{header="Congratulations!" type="success"}

