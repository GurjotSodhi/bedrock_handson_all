# Content Guide for Learning Assistant

Use this guide to match users to appropriate learning material based on their interests and experience level. All file paths are relative to `/environment/content/`.

---

## Foundational Concepts (`bedrock/foundation/`)

Best for: users new to Amazon Bedrock who need to understand the core APIs and tools before building anything.

| File | Summary |
|------|---------|
| `bedrock/foundation/index.en.md` | Overview of the Foundational Concepts Labs section. |
| `bedrock/foundation/bedrock-intro.en.md` | **Lab F-1** — Introduction to Amazon Bedrock: key concepts, foundation models, serverless architecture, and the Converse API. |
| `bedrock/foundation/bedrock-apis.en.md` | **Lab F-2** — Make a basic API call to Amazon Bedrock using the InvokeModel API with Boto3. |
| `bedrock/foundation/converse-api.en.md` | **Lab F-3** — Walk through the Converse API: text/image messages, system prompts, and response metadata. |
| `bedrock/foundation/bedrock-inference-parameters.en.md` | **Lab F-4** — Pass inference parameters (maxTokens, stopSequences) via the Converse API; temperature is introduced conceptually but demonstrated in a separate lab. |
| `bedrock/foundation/tool-use.en.md` | **Lab F-5** — Use function calling (tool use) with the Converse API, including defining tools and handling results. |
| `bedrock/foundation/streaming-intro.en.md` | **Lab F-6** — Make a streaming API call using `converse_stream` and print response chunks as they arrive. |
| `bedrock/foundation/bedrock-embedding.en.md` | **Lab F-7** — Use Amazon Titan Embeddings to compute and compare vector similarities with cosine similarity. |
| `bedrock/foundation/streamlit-intro.en.md` | **Lab F-8** — Build a minimal Streamlit app as an introduction to the UI framework used throughout the workshop. |
| `bedrock/foundation/model-selection.en.md` | Guidance on choosing Amazon Bedrock foundation models based on cost/performance tradeoffs and A/B testing. |

---

## Basic Patterns (`bedrock/basic/`)

Best for: users who want hands-on apps right away with no prior experience required.

| File | Summary |
|------|---------|
| `bedrock/basic/index.en.md` | Overview of the Basic Patterns Labs section. |
| `bedrock/basic/bedrock-text.en.md` | **Lab B-1** — Build a simple text-to-text generation app using Amazon Bedrock and Streamlit. |
| `bedrock/basic/bedrock-rag.en.md` | **Lab B-2** — Build a question-and-answer app using Retrieval-Augmented Generation (RAG) with Amazon Nova 2 Lite, Titan Embeddings, and a local Chroma vector database. |
| `bedrock/basic/bedrock-chatbot.en.md` | **Lab B-3** — Build a multi-turn chatbot with Amazon Bedrock and Streamlit, managing chat history manually. |

---

## Intermediate Text Patterns (`bedrock/intermediate/`)

Best for: users who have completed the basics and want to tackle more real-world use cases.

| File | Summary |
|------|---------|
| `bedrock/intermediate/index.en.md` | Overview of the Text Patterns Labs section (the intermediate section of the workshop). |
| `bedrock/intermediate/bedrock-rag-chatbot.en.md` | **Lab I-1** — Build a RAG-powered chatbot that uses tool use to retrieve context from a Chroma vector database on demand. |
| `bedrock/intermediate/bedrock-summarization.en.md` | **Lab I-2** — Build a document summarizer using Bedrock's document chat capability in the Converse API. |
| `bedrock/intermediate/bedrock-streaming.en.md` | **Lab I-3** — Build a streaming Streamlit app that displays model output incrementally as it arrives. |
| `bedrock/intermediate/bedrock-embeddings-search.en.md` | **Lab I-4** — Build an embeddings similarity search app that surfaces raw vector database matches without LLM post-processing. |
| `bedrock/intermediate/bedrock-personalized-recommendations.en.md` | **Lab I-5** — Build a personalized recommendations app that matches user queries to vector DB results and generates a tailored summary for each match. |
| `bedrock/intermediate/bedrock-json.en.md` | **Lab I-6** — Build a text-to-JSON extractor using tool use to pull structured fields from unstructured email content. |
| `bedrock/intermediate/bedrock-csv.en.md` | **Lab I-7** — Build a text-to-CSV extractor that generates JSON via tool use and converts it to a CSV displayed as a table and raw text using pandas. |

---

## Strands Agents — Fundamentals (`strands/fundamentals/`)

Best for: users moving from API-level Bedrock to building full agentic applications with Strands Agents.

| File | Summary |
|------|---------|
| `strands/index.en.md` | Introduction to the Strands Agents labs section, with workspace setup notes and screenshots of available labs. |
| `strands/fundamentals/index.en.md` | Overview of the Agentic Fundamentals chapter. |
| `strands/fundamentals/agents.en.md` | Understanding agents and agentic application architecture. |
| `strands/fundamentals/messages.en.md` | Messages and content blocks in agentic systems. |
| `strands/fundamentals/tool-schema.en.md` | JSON schema for Strands Agents tool definitions. |
| `strands/fundamentals/function-decorators.en.md` | Tool function decorators for Strands Agents. |
| `strands/fundamentals/structured-output.en.md` | Structured output with Pydantic and Strands Agents. |
| `strands/fundamentals/demo-apps.en.md` | Building agentic demo apps with Strands Agents. |

---

## Strands Agents — Intermediate Topics (`strands/intermediate-topics/`)

Best for: users comfortable with Strands Agents basics who want to explore advanced agentic patterns.

| File | Summary |
|------|---------|
| `strands/intermediate-topics/index.en.md` | Overview of the Intermediate Topics chapter. |
| `strands/intermediate-topics/multimodal.en.md` | Multimodal prompts and tools with Strands Agents. |
| `strands/intermediate-topics/context-engineering-basics.en.md` | Introduction to context engineering — no accompanying code. |
| `strands/intermediate-topics/sub-agents.en.md` | Orchestration and sub-agents using Strands Agents. |
| `strands/intermediate-topics/event-hooks.en.md` | Event hooks with Strands Agents. |
| `strands/intermediate-topics/compaction.en.md` | Message compaction strategies with Strands Agents. |
| `strands/intermediate-topics/mcp-local.en.md` | Introduction to MCP (Model Context Protocol) with Strands Agents. |

---

## Strands Agents — Use Cases (`strands/use-cases/`)

Best for: users who want end-to-end worked examples combining Strands Agents, tool use, and Streamlit UIs.

| File | Summary |
|------|---------|
| `strands/use-cases/index.en.md` | Overview of the use case labs available in this chapter. |
| `strands/use-cases/product-reviews.en.md` | Build a product review analyzer using Pydantic structured output for aspect-level sentiment extraction, with a Streamlit UI. |
| `strands/use-cases/quiz-assistant.en.md` | Build a quiz-generation chatbot using tool use with a custom JSON schema, Strands event hooks, and a Streamlit interface. |
| `strands/use-cases/data-storyteller.en.md` | Build a data storytelling agent that retrieves mock JSON data and uses tool-driven chart and commentary generation for a narrative Streamlit report. |

---

## AgentCore (`agentcore/agentcore-fundamentals/`)

Best for: users who want to deploy agents on AWS with managed runtime, tool gateways, and persistent memory. Requires an AWS-operated event.

| File | Summary |
|------|---------|
| `agentcore/index.en.md` | Top-level AgentCore lab index with event-only access notices and workspace setup instructions. |
| `agentcore/agentcore-fundamentals/index.en.md` | Introduction to Amazon Bedrock AgentCore — covers the Runtime, Gateway, and Memory components with descriptions of each. |
| `agentcore/agentcore-fundamentals/runtime-setup.en.md` | Set up and run an AgentCore Runtime agent locally using Python and the `agentcore` CLI dev server. |
| `agentcore/agentcore-fundamentals/runtime-deploy.en.md` | Deploy an agent to AWS AgentCore Runtime and demonstrate session-based conversation continuity. |
| `agentcore/agentcore-fundamentals/runtime-client.en.md` | Invoke a deployed AgentCore Runtime agent via a Python CLI client and Streamlit chatbot UI. |
| `agentcore/agentcore-fundamentals/memory.en.md` | Using Amazon Bedrock AgentCore Memory with Strands Agents for persistent storage. |
| `agentcore/agentcore-fundamentals/runtime-memory.en.md` | Add AgentCore Memory to a deployed Runtime so conversation preferences persist across sessions. |
| `agentcore/agentcore-fundamentals/gateway-setup.en.md` | Create an AgentCore Gateway backed by Lambda, generate tool specs from an MCP prototype, and enable semantic search. |
| `agentcore/agentcore-fundamentals/gateway-client.en.md` | Connect a Strands agent to the AgentCore Gateway via IAM-authenticated Streamable HTTP transport. |
| `agentcore/agentcore-fundamentals/gateway-search.en.md` | Use AgentCore Gateway's semantic search to let an agent dynamically discover and load only relevant tools per request. |
| `agentcore/agentcore-fundamentals/runtime-gateway.en.md` | Deploy an agent to AgentCore Runtime that connects via MCP to an AgentCore Gateway for Lambda-backed tool access. |
