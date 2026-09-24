---
title: "Context engineering basics"
weight: 200
---


::::alert
This lab is based on the following article: [Introduction to context engineering](https://builder.aws.com/content/38oLzpDYZJKUwbbKw3XyKD4Qjdd/introduction-to-context-engineering)
::::




## The context window

Before we can talk about context engineering, we need to talk about an LLM's **context window**.

The **context window** is the amount of input content an LLM can receive as part of a request. Model providers have been rapidly increasing their models' context windows, starting from hundreds of tokens a few years ago, to hundreds of thousands of tokens today. So great! Problem solved, right? Sorry, no.

Filling the larger context window has several important downsides:

* More input tokens = higher cost per request
* Greater latency per request
* The LLM can get confused when processing lots of content, leading to it returning low-quality responses or forgetting its objective entirely

## Context engineering

**Context engineering** is the effective management of the LLM's context window, in order for it to complete its objective in a cost-efficient and performant way.

Some key aspects of context engineering include:

* **Prompt engineering**: Efficiently and effectively communicating requirements and information to an agent.
* **Tool curation**: Limiting the number of tools available to an agent.
* [**Division of labor across agents**](https://builder.aws.com/content/38oNsaQfOSbawDMpHdZIUdWRy99/orchestration-and-sub-agents-using-strands-agents): Delegating tasks to other agents, in order to minimize tools, message history, and total context size needed for each agent.
* [**Conversation history management**](https://builder.aws.com/content/38oNwLRwQIiQEsuy2eG1KGZ0HR8/message-compaction-with-strands-agents): Limiting conversation history to more recent messages, along with summaries of past messages.
* **Memory storage & retrieval**: Selectively storing user preferences, important facts, and intermediate results, to be retrieved as needed later.
* **Information retrieval**: The ability to retrieve relevant information from knowledge bases, the Internet, or other sources (AKA Retrieval-Augmented Generation).

## Context engineering examples

1. Using one agent to summarize a large document and return the summary to another agent
2. Summarizing or deleting older messages whenever the message history gets too large
3. Passing requests to a specialized agent with a distinct set of tools and instructions
4. Selectively storing key facts for later retrieval
5. Selectively retrieving information from knowledge bases (retrieval-augmented generation)

We will gradually introduce these concepts throughout this series.

## Learn more

* [Phil Schmid: The New Skill in AI is Not Prompting, It's Context Engineering](https://www.philschmid.de/context-engineering)
* [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
* [AWS: Key components of a data-driven agentic AI application](https://aws.amazon.com/blogs/database/key-components-of-a-data-driven-agentic-ai-application/)






Please check out the [series overview for more articles on agentic topics.](https://builder.aws.com/content/38ooxopwKSyth7Wa9dVTdrmnGL7/series-overview-agentic-applications-with-amazon-bedrock)