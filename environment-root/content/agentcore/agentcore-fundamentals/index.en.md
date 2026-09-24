---
title : "🦾 AgentCore fundamentals"
weight : 300
---

:::alert{header="Workspace setup" type="info"}
These labs use the `/environment` folder as the working directory. If your IDE has a different folder open, switch back using **☰ → File → Open Folder**

Alternatively, you can run :code[code /environment --reuse-window]{showCopyAction=true} from the web IDE's terminal.
:::

## Introduction to Amazon Bedrock AgentCore

**[Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)** is a set of managed AWS services for deploying, connecting, and operating AI agents. It includes components for hosting agent code, securely connecting agents to tools, and giving agents persistent memory across conversations.

**[AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)** hosts and runs your agent code as a managed service. It handles request routing, health checks, and session management. The [Bedrock AgentCore Starter Toolkit](https://aws.github.io/bedrock-agentcore-starter-toolkit/index.html) supports local development and testing before deployment.

**[AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)** exposes backend resources as tools that agents can discover and invoke through the Model Context Protocol (MCP). You register your backend services as targets for a gateway, define tool schemas, and agents connect to the gateway's MCP endpoint to access their tools. Gateway supports semantic search across registered tools, so agents can optionally load only the tools relevant to the current request.

**[AgentCore Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html)** provides persistent storage for conversation history and extracted knowledge. Short-term memory stores raw conversation turns within a session. Long-term memory automatically extracts durable information across sessions using configurable strategies.

AgentCore includes additional components beyond what we cover in this series. See the [Amazon Bedrock AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is.html) for the full list of services and capabilities.



## Labs

_Screenshots from some of the labs in this section:_

| | |
| :---: | :---: |
| ![Screenshot of a chatbot web application titled 'Chatbot using AgentCore' with a session ID displayed. A user message reads 'Tell me about the ALF show' and the assistant responds with a detailed answer about the ALF TV show, including sections for 'Plot & Premise' and 'Main Characters', describing it as an American sitcom that aired from 1986 to 1990.](/static/images/agentcore/client/client-app.png) | ![Screenshot of the chatbot demo after a conversation. The left side shows the Memory section with 'Retrieved memory passed to model' containing XML-formatted user context with stored preferences. The right side shows a chat exchange where the user said 'Hello' and the bot responded with a personalized greeting, confirming that the agent successfully used its stored memory to personalize the response.](/static/images/agentcore/memory/memory-app-in-use.png) |

::children

