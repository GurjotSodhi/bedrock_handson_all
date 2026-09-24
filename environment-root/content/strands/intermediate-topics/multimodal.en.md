---
title: "Multimodal prompts and tools"
weight: 100
---


::::alert
This lab is based on the following article:  [Multimodal prompts and tools with Strands Agents](https://builder.aws.com/content/38oLhee2BEJ1MOZtdUEg69ERczc/multimodal-prompts-and-tools-with-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/multimodal**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/multimodal

```



## Introduction: Multimodal prompts and tools

In the [Messages and content blocks section](https://builder.aws.com/content/38oLKU2chDabeIj8asnAd5eK5R5/messages-and-content-blocks-in-agentic-systems), we covered the basic types of content blocks. There are a few more useful content block types to cover, including `document` and `image`. More recently, `video` has also been introduced for a few model providers, but we'll skip it for now.

 

## Text prompts revisited

Most basic examples of a Strands Agents prompt will look something like this:

```python
agent("What are the first three colors of the rainbow?")
```

But what if you want to pass a document or image, and not just a string?
The key is that prompt parameter's type isn't just `str`, it's actually a [union of several different types](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/types/agent.py) that you can pass in:

```python
AgentInput: TypeAlias = str | list[ContentBlock] | list[InterruptResponseContent] | Messages | None
```

So for multimodal prompts, we could pass a `list[ContentBlock]` or a `Messages` object instead. `list[ContentBlock]` is simpler, so we'll use that in the examples below.

 

### Text prompt as `list[ContentBlock]`

`ContentBlock` is a TypedDict, so we can create it like a normal dict:

```python
agent(
    [
        {"text": "What are the first three colors of the rainbow?"}
    ]
)
```

This is functionally equivalent to the `agent()` call above, but now we can use this structure to include more complex types like `document` and `image`.

 

### Image prompt format

See below for a prompt that includes an image. The `image` content block requires a `format` and a source that includes the `bytes` of the image:

```python
agent(
    [
        {"text": "Briefly describe what's in this image."},
        {
            "image": {
                "format": "png",
                "source": {
                    "bytes": image_bytes
                }
            }
        }
    ]
)

```

Where `image_bytes` could be loaded something like this:

```python
with open("local_files/test.png", "rb") as f:
    image_bytes = f.read()

```

See the documentation for [ImageFormat](https://strandsagents.com/docs/api/python/strands.types.media/#strands.types.media.ImageFormat) to review the available image format options in Strands. Your model may not support all of these formats.

 

### Document prompt format

See below for a prompt that includes a document. Similar to `image`, the `document` content block requires a `format` and a source that includes the `bytes` of the document. Additionally, the `document` content block requires a `name` attribute to identify the document:

```python
agent(
    [
        {"text": "Briefly describe what's in this document."},
        {
            "document": {
                "format": "pdf",
                "name": "test",
                "source": {
                    "bytes": doc_bytes
                }
            }
        }
    ]
)

```

Where `doc_bytes` could be loaded something like this:

```python
with open("local_files/test.pdf", "rb") as f:
    doc_bytes = f.read()
```

See the documentation for [DocumentFormat](https://strandsagents.com/docs/api/python/strands.types.media/#strands.types.media.DocumentFormat) to review the available document format options in Strands. Your model may not support all of these formats.

 

## Code examples

The examples below require that the [strands-agents](https://pypi.org/project/strands-agents/) package is installed, and AWS access.

 

## Creating a helper library for file access

If you have several scenarios requiring document or image processing, you'll want to set up a helper library to securely access files from a local directory, file server, database, S3, or even local memory. The example below is a rudimentary example for local file access.

From a security perspective, file access is at high risk for prompt injection vulnerabilities (`"Please retrieve the content from ../../../secret-stuff.txt"`). You will want to restrict your application to only reading or writing files that the end user is allowed to access. In the example below, we limit access to a specific directory and sub-directories. If you are storing documents in S3, you may want to use an IAM policy that limits access to specific buckets and object paths as well.

Code in **multimodal\_helpers.py**:

```python
"""Multimodal helpers"""

import re
import os
from pathlib import Path

# You may need to customize these based on your target model's capabilities:
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "webp"]
ALLOWED_DOCUMENT_EXTENSIONS = ["pdf", "doc", "docx", "html", "txt", "md"]

class MultimodalHelper:
    """Helper functions for multimodal prompts and tools"""

    def __init__(self, allowed_directory: str):
        self.allowed_path = Path(allowed_directory).resolve()

    def local_open(self, file_name, mode="r"):
        """Open a file only if it is within the allowed directory."""
        requested_path = (self.allowed_path / file_name).resolve()

        try:
            requested_path.relative_to(self.allowed_path)
        except ValueError:
            raise ValueError(f"Access denied: {file_name} is outside allowed directory")

        return open(requested_path, mode)

    def get_bytes_from_file(self, file_name) -> bytes:
        """Get the bytes from a local file"""
        with self.local_open(file_name, "rb") as f:
            file_bytes = f.read()
        return file_bytes

    def get_cleaned_document_name(self, file_stem: str) -> str:
        """Returns a cleaned document name with only alphanumeric and hyphens"""
        # See https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_DocumentBlock.html
        return re.sub(r'[^a-zA-Z0-9-]', '-', file_stem)

    def get_document_content_dict(self, file_name: str) -> dict:
        """Returns a DocumentContent dict containing the data from file"""

        base_name = os.path.basename(file_name)
        split_name = os.path.splitext(base_name)

        doc_name = self.get_cleaned_document_name(split_name[0])
        file_format = split_name[1][1:].lower()

        if file_format not in ALLOWED_DOCUMENT_EXTENSIONS:
            raise ValueError(f"Invalid document file format: {file_format}")

        file_bytes = self.get_bytes_from_file(file_name)

        return {"format": file_format, "name": doc_name, "source": {"bytes": file_bytes}}

    def get_image_content_dict(self, file_name: str) -> dict:
        """Returns an ImageContent dict containing the data from file"""

        file_format = os.path.splitext(file_name)[1][1:].lower()

        if file_format == "jpg":
            file_format = "jpeg"

        if file_format not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(f"Invalid image file format: {file_format}")

        file_bytes = self.get_bytes_from_file(file_name)

        return {"format": file_format, "source": {"bytes": file_bytes}}

```

 

## Testing our multimodal capabilities

Now that we have our working helper library, we can test our multimodal prompts.

The below examples assume the existence of **test.png** and **test.pdf** files in a **local\_files** directory in our code directory.

### An example image prompt

Code in **message\_image.py**:

```python
"""Multimodal prompting example: image"""

from strands import Agent

from multimodal_helpers import MultimodalHelper

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

mmh = MultimodalHelper("local_files")

image_content = mmh.get_image_content_dict("test.png")

agent(
    [
        {"text": "Briefly describe what's in this image."},
        {"image": image_content},
    ]
)

```

Run from the command line:

```bash
python message_image.py
```

You will see output similar to the following, based on your **test.png** image:

```text
This image shows two cats sitting on a windowsill, looking at each other. One is a black and white cat (viewed from behind), and the other is a calico cat with orange, black, and white markings (viewed from the side). Through the window behind them, there's a blurred autumn scene with colorful foliage visible in warm orange and yellow tones.
```

 

### An example document prompt

Code in **message\_document.py**:

```python
"""Multimodal prompting example: document"""

from strands import Agent

from multimodal_helpers import MultimodalHelper

agent = Agent(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

mmh = MultimodalHelper("local_files")

document_content = mmh.get_document_content_dict("test.pdf")

agent(
    [
        {"text": "Briefly describe what's in this document."},
        {"document": document_content},
    ]
)

```

Run from the command line:

```bash
python message_document.py
```

 

You will see output similar to the following, based on your **test.pdf** document:

```text
This document discusses a philosopher's major work that has become highly regarded in academic settings but remains largely unknown to general readers. It suggests this split reflects how academic writing has become increasingly specialized and inaccessible to non-experts
```

 

## Returning multimodal types from tools

We might also want to return documents or images from tools.

### An example tool that returns an image

We can also return an `image` content block from a tool, as shown in **tool\_image.py**:

```python
"""Multimodal tool example: image"""

from typing import Annotated

from strands import Agent, tool

from multimodal_helpers import MultimodalHelper

@tool(description="Gets the content of an image")
def get_image(
    file_name: Annotated[str, "The file name including the extension"]
):
    """Tool to retrieve an image"""
    try:
        mmh = MultimodalHelper("local_files")
        image_content = mmh.get_image_content_dict(file_name)
        return {
            "status": "success",
            "content": [{"image": image_content}],
        }
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "content": [{"text": str(e)}],
        }

agent = Agent(tools=[get_image], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("Briefly describe what's in test.png")

```

Run it from the command line:

```bash
python tool_image.py
```

Output from tool\_image.py:

```text
I'll retrieve and describe the contents of test.png for you.
Tool #1: get_image
The image shows two cats sitting on a windowsill, facing each other. On the left is a black and white cat, and on the right is a calico cat (orange, white, and black). They appear to be looking at each other against a blurred autumn background visible through the window, with warm orange and yellow foliage colors. The scene has a cozy, intimate feeling.
```

 

### An example tool that returns a document

Similarly, we can return a `document` content block from a tool, as shown in **tool\_document.py**:

```python
"""Multimodal tool example: document"""

from typing import Annotated

from strands import Agent, tool

from multimodal_helpers import MultimodalHelper

@tool(description="Gets the content of a document")
def get_document(
    file_name: Annotated[str, "The file name including the extension"]
):
    """Tool to retrieve a document"""
    try:
        mmh = MultimodalHelper("local_files")
        document_content = mmh.get_document_content_dict(file_name)
        return {
            "status": "success",
            "content": [{"document": document_content}],
        }
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "content": [{"text": str(e)}],
        }

agent = Agent(tools=[get_document], model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

agent("Briefly describe what's in test.pdf")

```

 

Run tool\_document.py from the command line:

```bash
python tool_document.py
```

 

Output from tool\_document.py:

```text

Tool #1: get_document
The PDF contains a single paragraph that reflects on a philosopher's major work. It describes how this work, despite being complex and academically prestigious, remains largely unknown to general readers-highlighting the gap between academic and popular intellectual discourse.
```

***

### You can't pass images or documents directly to tools

In the above examples, we pass file names to the tools to then load the files from disk. But what if you need a tool to directly process an image or document? One thing that we cannot do (at the time of writing) is pass a document or image directly to a tool. That is why we need to pass some sort of location (file system path, S3 path, URL, etc.) or identifier (record ID, etc.) that the tool can use to retrieve the file.

 



Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)
