---
title: "Lab F-3: Converse API"
weight: 10300
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting this lab.
::::

# Lab introduction

The Amazon Bedrock Converse API provides a consistent way to access large language models (LLMs) using Amazon Bedrock. It supports turn-based messages between the user and the generative AI model. It also provides a consistent format for tool definitions for the models that support tool use (aka "function calling").

Why is the Converse API so important? Previously, with the InvokeModel API, you needed to use different JSON request and response structures for each model provider. The Converse API allows us to use a single format for requests and responses across all large language models on Amazon Bedrock.

Note that as of this article's writing, the Converse API only supports text generation models. Embeddings models and image generation models still require InvokeModel. You can find the list of [Converse API supported models and features](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-supported-models-features) in the official documentation.



::alert[Not every model supports all of the capabilities of the Converse API, so it’s important to review the [supported model features](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-supported-models-features) in the official documentation.]{header="Note" type="info"}


&nbsp;


# Code walkthrough: using the Amazon Bedrock Converse API

Let’s start by writing a Python script that you can run from the command line. We will demonstrate basic text messages, image-based messages, system prompts, and response metadata.

## Create the Python script


1. Navigate to the **workshop/labs/converse** folder, and open the file **converse_api.py**

![Screenshot of development environment showing the file explorer on the left with the workshop folder tree expanded](/static/labs/code-browser.png)

&nbsp;

## A basic call to the Converse API

Let’s start by defining a simple message and add it to an empty list of messages. We’re creating a message from the “user” role. Within that message, we can include a list of content blocks. In this example, we have a single `text` content block where we ask the model "How are you today?".

We’re now ready to pass that message to Amazon Bedrock. We specify Anthropic’s Claude 3 Sonnet as the target model. We can limit the number of tokens in the model’s response by setting the `maxTokens` value. We also set the `temperature` to zero to minimize the variability of responses.

2. Use the copy button in the box below to automatically copy its code, then paste it into the **converse_api.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
import boto3, json

print("\n----A basic call to the Converse API----\n")

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

message_list = []

initial_message = {
    "role": "user",
    "content": [
        { "text": "How are you today?" } 
    ],
}

message_list.append(initial_message)

response = bedrock.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=message_list,
    inferenceConfig={
        "maxTokens": 2000,
    },
)

response_message = response['output']['message']
print(json.dumps(response_message, indent=4))


::::


This will generate a response similar to the following:

::::code{showCopyAction=false language="json" showLineNumbers=false}
{
    "role": "assistant",
    "content": [
        {
            "text": "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, harmless, and honest."
        }
    ]
}
::::

&nbsp;

## Alternating user and assistant messages

You can use the Converse API to send a list of previous messages along with a new message to the LLM to continue the conversation. You must alternate between messages from the “user” and “assistant” roles. The last message in the list should be from the “user” role, so that the LLM can respond to it.

3. Use the copy button in the box below to automatically copy its code, then paste it into the **converse_api.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Alternating user and assistant messages----\n")

message_list.append(response_message)

print(json.dumps(message_list, indent=4))


::::


This will display our conversation so far:


::::code{showCopyAction=false language="json" showLineNumbers=false}
[
    {
        "role": "user",
        "content": [
            {
                "text": "How are you today?"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "text": "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, harmless, and honest."
            }
        ]
    }
]
::::

We'll need to add another "user" message to the list before we can send a request to the model.

&nbsp;

## Including an image in a message

See the [Converse API ImageBlock documentation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ImageBlock.html) for the list of supported image types, and [Anthropic's vision documentation](https://docs.anthropic.com/en/docs/vision#image-size) for image size constraints.

Now we’ll load a local image file and add its bytes to an image content block. We follow Anthropic’s vision prompting tips and preface our image with the label “Image 1:”, then follow the image with our request.

4. Use the copy button in the box below to automatically copy its code, then paste it into the **converse_api.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Including an image in a message----\n")

with open("image.webp", "rb") as image_file:
    image_bytes = image_file.read()

image_message = {
    "role": "user",
    "content": [
        { "text": "Image 1:" },
        {
            "image": {
                "format": "webp",
                "source": {
                    "bytes": image_bytes #no base64 encoding required!
                }
            }
        },
        { "text": "Please describe the image." }
    ],
}

message_list.append(image_message)

response = bedrock.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=message_list,
    inferenceConfig={
        "maxTokens": 2000,
    },
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
            "text": "The image shows a miniature model of a house, likely a decorative ornament or toy. The house has a blue exterior with white window frames and a red tiled roof. It appears to be made of ceramic or a similar material. The miniature house is placed on a surface with some greenery and yellow flowers surrounding it, creating a whimsical and natural setting. The background is slightly blurred, allowing the small house model to be the focal point of the image."
        }
    ]
}
::::

Note: we’re not printing the message with the image bytes because it will be really long and really not interesting.



You can learn more about Claude 3’s vision capabilities here: https://docs.anthropic.com/en/docs/vision

&nbsp;

## Setting a system prompt

You can set a system prompt to communicate basic instructions for the large language model outside of the normal conversation. System prompts are generally used by the developer to define the tone and constraints for the conversation. In this case, we’re instructing Claude to act like a pirate.

5. Use the copy button in the box below to automatically copy its code, then paste it into the **converse_api.py** file.

::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Setting a system prompt----\n")

summary_message = {
    "role": "user",
    "content": [
        { "text": "Can you please summarize our conversation so far?" } 
    ],
}

message_list.append(summary_message)

response = bedrock.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=message_list,
    system=[
        { "text": "Please respond to all requests in the style of a pirate." }
    ],
    inferenceConfig={
        "maxTokens": 2000,
    },
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
            "text": "Arr, matey! Let me spin ye a tale of our conversatin' thus far. Ye greeted me shipshape, askin' how I was farin' on this fine day. I replied that I be doin' well as yer trusty AI pirate mate, ready to lend a hand. Then ye showed me a pretty little image of a wee house ornament, all blue an' red with windows an' surrounded by greenery. I described to ye what I spotted in that thar image, not lettin' any details go unnoticed by me eagle eyes. Now ye be askin' ol' Claude to summarize our whole parley up to this point. I aimed to give ye a full account, regaled in true pirate style, of how our voyage has gone so far. Arrr, how'd I do wit' that summary, matey?"
        }
    ]
}
::::

For those who don't want to horizontally scroll, here's our piratized summary of the conversation so far:

> Arr, matey! Let me spin ye a tale of our conversatin' thus far. Ye greeted me shipshape, askin' how I was farin' on this fine day. I replied that I be doin' well as yer trusty AI pirate mate, ready to lend a hand. Then ye showed me a pretty little image of a wee house ornament, all blue an' red with windows an' surrounded by greenery. I described to ye what I spotted in that thar image, not lettin' any details go unnoticed by me eagle eyes. Now ye be askin' ol' Claude to summarize our whole parley up to this point. I aimed to give ye a full account, regaled in true pirate style, of how our voyage has gone so far. Arrr, how'd I do wit' that summary, matey?


You can learn more about system prompts here: https://docs.anthropic.com/en/docs/system-prompts

&nbsp;

## Getting response metadata and token counts

The Converse method also returns metadata about the API call.

* The `stopReason` property tells us why the model completed the message. This can be useful for your application logic, error handling, or troubleshooting.

* The `usage` property includes details about the input and output tokens. This can help you understand the charges for your API call.


6. Use the copy button in the box below to automatically copy its code, then paste it into the **converse_api.py** file.


::::code{showCopyAction=true language="python" showLineNumbers=false}
print("\n----Getting response metadata and token counts----\n")

print("Stop Reason:", response['stopReason'])
print("Usage:", json.dumps(response['usage'], indent=4))


::::

This will generate a response similar to the following:

::::code{showCopyAction=false language="text" showLineNumbers=false}
Stop Reason: end_turn
Usage: {
    "inputTokens": 629,
    "outputTokens": 154,
    "totalTokens": 783
}
::::

In this case, Claude stopped because it had nothing left to say for now. Other stop reasons include hitting the response token limit (`max_tokens`), requesting a tool (`tool_use`), or triggering a content filter (`content_filtered`). Review the official documentation for the [full list of stop reasons](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html#API_runtime_Converse_ResponseSyntax).

Keep in mind that the displayed usage numbers are only for the last API call we made. You can use these token counts to determine the cost of the API call. You can learn more about [token-based pricing](https://aws.amazon.com/bedrock/pricing/) on the Amazon Bedrock website.

&nbsp;

7. Save the file.

Great! Now you are ready to run the script!

&nbsp;

# Run the script

---

&nbsp;

1. Select the **Terminal** in your development environment and change directory.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
cd /environment/workshop/labs/converse

::::



&nbsp;

2. Run the script from the terminal.

::::code{showCopyAction=true language="bash" showLineNumbers=false}
python3 converse_api.py

::::



&nbsp;

3. The results should be displayed in the terminal.



---

&nbsp;





::alert[You have successfully called the Amazon Bedrock Converse API!]{header="Congratulations!" type="success"}
