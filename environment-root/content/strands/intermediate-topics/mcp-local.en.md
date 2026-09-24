---
title : "MCP"
weight : 3000
---

::::alert
This lab is based on the following article: [Introduction to MCP with Strands Agents](https://builder.aws.com/content/3AizXP3Yi8KOr7XnuF71LcN4jXX/introduction-to-mcp-with-strands-agents)
::::


In your workshop development environment, the code can be found under **/environment/workshop/agentic-labs/mcp-local**

In the workshop environment's terminal, change directory using the following command:

```bash
cd /environment/workshop/agentic-labs/mcp-local
```



## Overview of Model Context Protocol (MCP)

The Model Context Protocol (MCP) is an open standard for connecting AI agents to external tools and data sources. It follows a client-server architecture: an MCP client (typically an agent) connects to an MCP server, which exposes capabilities the client can discover and invoke.

Strands Agents supports [defining tools as Python functions](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/), which works well when the tool logic lives in the same codebase as the agent. MCP is useful when you want to share tools across multiple agents or frameworks, expose tools written in other languages, or consume third-party tools.

*Note: This article is based on the* [2025-11-25 version of the MCP specification.](https://modelcontextprotocol.io/specification/2025-11-25)

 

### MCP primitives

MCP servers can expose three types of primitives: **tools**, **resources**, and **prompts**:

* [Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) are callable functions with typed inputs and outputs
* [Resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources) are read-only text or binary content like documents, images, data files, etc.
* [Prompts](https://modelcontextprotocol.io/specification/2025-11-25/server/prompts) are reusable prompt templates

We'll demonstrate MCP tools in the code examples below.

 

### MCP transports

The protocol defines two standard transports, **stdio** and **Streamable HTTP**:

* [stdio](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports#stdio) has the client launch the server as a local subprocess and communicate over stdin/stdout (like a command line app)
* [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports#streamable-http) has the server run independently, with the client using HTTP requests to communicate with the server

 

## Code examples

The examples below require the [strands-agents](https://pypi.org/project/strands-agents/) and [fastmcp](https://pypi.org/project/fastmcp/) packages to be installed, and AWS access.

 

### A note on `mcp` vs. `fastmcp` Python libraries

Strands Agents includes Anthropic's [mcp Python library](https://github.com/modelcontextprotocol/python-sdk), which includes version 1 of the [FastMCP](https://gofastmcp.com/getting-started/welcome) library.

Since then, FastMCP 2 came out, with significant enhancements and thorough documentation. One example: FastMCP 2 supports using `Annotated` for tool field definitions (like Strands does), which is nice when moving from local Strands Python tools to MCP tools.

So it's a bit ridiculous, but we're importing two different MCP libraries in the examples below. Welcome to bleeding-edge technology!

The "PFJ" scene from *Monty Python's Life of Brian* covers it nicely:


![Meme from Monty Python's Life of Brian showing mirrored characters arguing, with the caption 'SPLITTERS!!' at the top. The left side reads 'FROM FASTMCP IMPORT FASTMCP' and the right side reads 'FROM MCP.SERVER IMPORT FASTMCP', joking about the two competing Python import paths for the FastMCP library.](/static/images/intermediate/mcp-local/splitters-mcp.png)
 

### Creating a basic MCP server using FastMCP

In **math\_fastmcp\_server.py** we create an MCP server using the fastmcp Python library:

```python
"""Math MCP server implemented with fastmcp library"""

import math
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP(name="MathServer")

@mcp.tool(description="Calculates the cosine of x")
def cosine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Cosine tool"""
    return math.cos(x)

@mcp.tool(description="Calculates the sine of x")
def sine(x: Annotated[float, "The value of x in radians"]) -> float:
    """Sine tool"""
    return math.sin(x)

@mcp.tool(description="Divides x by y")
def divide(x: Annotated[float, "The numerator"], y: Annotated[float, "The denominator"]) -> float:
    """Divide tool"""
    return x / y

@mcp.tool(description="Raise x to the power y")
def raise_to_power(x: Annotated[float, "The base"], y: Annotated[float, "The exponent"]) -> float:
    """Raise to power tool"""
    return math.pow(x, y)

if __name__ == "__main__":
    mcp.run()
```

Since our clients are using the [stdio transport layer](https://modelcontextprotocol.io/docs/learn/architecture#transport-layer), we don't need to run this script directly. The client apps will execute the script themselves.

 

### Listing tools from an MCP server

In **list\_mcp\_tools.py** we load the MCP server from math\_fastmcp\_server.py through stdio and display its tools:

```python
"""List MCP tools"""

import json
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="python", args=["math_fastmcp_server.py"]))
)

with stdio_mcp_client:
    tools = stdio_mcp_client.list_tools_sync()

    for mcp_tool in tools:
        print("-" * 50)
        print(mcp_tool.tool_name)
        print("-" * 50)
        print(json.dumps(mcp_tool.tool_spec, indent=4))
```

Run the following from your terminal:

```bash
python list_mcp_tools.py
```

This will output the tool names and tool specs retrieved from **math\_fastmcp\_server.py**. Here is an example of one of the tool specs:

```json
--------------------------------------------------
raise_to_power
--------------------------------------------------
{
    "inputSchema": {
        "json": {
            "properties": {
                "x": {
                    "description": "The base",
                    "type": "number"
                },
                "y": {
                    "description": "The exponent",
                    "type": "number"
                }
            },
            "required": [
                "x",
                "y"
            ],
            "type": "object"
        }
    },
    "name": "raise_to_power",
    "description": "Raise x to the power y",
    "outputSchema": {
        "json": {
            "properties": {
                "result": {
                    "type": "number"
                }
            },
            "required": [
                "result"
            ],
            "type": "object",
            "x-fastmcp-wrap-result": true
        }
    }
}
```

 

### Using the MCP server with Strands Agents

In **mcp\_client.py** we load math\_fastmcp\_server.py through stdio and invoke it with a Strands agent. The `MCPClient` must be used inside a `with` block, which manages the lifecycle of the connection to the MCP server. It opens the stdio transport on entry and shuts it down on exit.

```python
"""Basic local MCP client"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="python", args=["math_fastmcp_server.py"]))
)

with stdio_mcp_client:
    tools = stdio_mcp_client.list_tools_sync()
    agent = Agent(tools=tools, model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

    agent("What is the secant squared of 1.4?")
```

Run the following command from your terminal:

```bash
python mcp_client.py
```

Example output:

```text
I need to calculate the secant squared of 1.4. The secant is the reciprocal of cosine, so sec²(x) = 1/cos²(x).

Let me first find the cosine of 1.4, then calculate the secant squared.
Tool #1: cosine
Now I need to calculate 1/cos²(1.4). First, let me square the cosine value:
Tool #2: raise_to_power
Now I'll calculate the reciprocal to get sec²(1.4):
Tool #3: divide
The secant squared of 1.4 is approximately **34.62**.
```

 

### Interactive CLI chat with MCP tools

In **cli\_mcp\_chat.py** we wrap the same MCP server in a simple command-line chat loop. The chat loop runs inside the `with` block so the MCP connection stays open for the entire conversation. If the connection closes, the agent loses access to the MCP tools.

```python
"""
A simple command-line interface for chatting with an agent.
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

BOT_PREFIX = "\033[1;36m\n🤖Bot:"
HUMAN_PREFIX = "\033[0;33m\n\n🙂Me:\n"

def main():
    """Runs a CLI-based chat with the agent"""

    mcp_client = MCPClient(
        lambda: stdio_client(StdioServerParameters(command="python", args=["math_fastmcp_server.py"]))
    )

    with mcp_client:
        tools = mcp_client.list_tools_sync()
        agent = Agent(tools=tools, model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

        print(
            f"""{BOT_PREFIX}
    Welcome! Type your message below and hit return to send.
    Type "exit", "quit", "done", "bye" or press Ctrl-C to exit."""
        )

        while True:  # loop until exited
            try:
                prompt = input(f"{HUMAN_PREFIX}")

                if prompt.lower() in ["exit", "quit", "done", "bye"]:
                    print("EXITING!!!")
                    break

                print(f"{BOT_PREFIX}")
                agent(prompt)
            except KeyboardInterrupt:
                print("\nBye!\n")
                break

if __name__ == "__main__":
    main()
```

Run the following command from your terminal:

```bash
python cli_mcp_chat.py
```

Example output:

```text
🤖Bot:
    Welcome! Type your message below and hit return to send.
    Type "exit", "quit", "done", "bye" or press Ctrl-C to exit.

🙂Me:
what is the tangent of 1.385?

🤖Bot:
To calculate the tangent of 1.385, I need to use the identity tan(x) = sin(x)/cos(x). Let me calculate the sine and cosine of 1.385 first.
Tool #1: sine

Tool #2: cosine
Now I'll divide the sine by the cosine to get the tangent:
Tool #3: divide
The tangent of 1.385 radians is approximately **5.32**.

🙂Me:
exit
```

 

### Using the local MCP server from Kiro

You can also connect your local MCP server to [Kiro](https://kiro.dev/) for interactive testing. In the `~/.kiro/settings/mcp.json` file, add an entry under `"mcpServers"`. The `command` path must point to the Python binary inside your active virtual environment, and the `args` path must be the absolute path to your MCP server script. Use `which python` in your terminal (with the venv activated) to get the correct Python path.

```json
{
  "mcpServers": {
    "local-math-mcp": {
      "command": "/Users/your_user_name/path_to_venv/.venv/bin/python",
      "args": [
        "/Users/your_user_name/path_to_code/math_fastmcp_server.py"
      ],
      "disabled": false,
      "autoApprove": [
        "cosine",
        "raise_to_power",
        "divide",
        "sine"
      ]
    }
  }
}
```

You can then invoke your local MCP tools from Kiro:

![Screenshot of Kiro responding to the prompt 'what is the tangent of 1.2?' by calling three MCP tools (sine, cosine, and divide), then returning the result: 'The tangent of 1.2 is approximately 2.572.'](/static/images/intermediate/mcp-local/kiro-mcp-use.png)

This is a quick and dirty way to experiment with MCP servers.

Many published MCP servers are distributed as Python or Node.js packages. When you see an MCP server configured with `"command": "uvx"`, that's using [uv](https://docs.astral.sh/uv/) to run the server in a temporary isolated environment, downloading the package and its dependencies on the fly without permanently installing anything.

Check out the code for the [Strands MCP Servers](https://github.com/strands-agents/mcp-server) or [AWS MCP servers](https://github.com/awslabs/mcp) to see how others have built and distributed their MCP servers.

You should also check out [this blog on creating MCP servers](https://modelcontextprotocol.io/docs/develop/build-server) from the official MCP site. It includes a Python example using uv, plus examples with other programming languages.

[Learn more about configuring MCP servers in Kiro.](https://kiro.dev/docs/mcp/configuration/)

 

## Alternative: using the `mcp` library for your server

If you wanted to use the official `mcp` Python library (which includes FastMCP 1), you can still define tools with field descriptions. You just have to use a Pydantic Field object:

```python
"""Math MCP server implemented with mcp library"""

import math
from pydantic import Field

from mcp.server import FastMCP

# Create a server instance
mcp = FastMCP(name="MathServer")

@mcp.tool(description="Calculates the cosine of x.")
def cosine(x: float = Field(description="The value of x in radians")) -> float:
    """Cosine tool"""
    return math.cos(x)

@mcp.tool(description="Calculates the sine of x")
def sine(x: float = Field(description="The value of x in radians")) -> float:
    """Sine tool"""
    return math.sin(x)

@mcp.tool(description="Divides x by y")
def divide(x: float = Field(description="The numerator"), y: float = Field(description="The denominator")) -> float:
    """Divide tool"""
    return x / y

@mcp.tool(description="Raise x to the power y")
def raise_to_power(x: float = Field(description="The base"), y: float = Field(description="The exponent")) -> float:
    """Raise to power tool"""
    return math.pow(x, y)

if __name__ == "__main__":
    mcp.run()
```

 

## Next steps

Learn more:

* [Strands Agents and MCP](https://strandsagents.com/docs/user-guide/concepts/tools/mcp-tools/)
* [Anthropic: Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
* [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/getting-started/intro)

Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)