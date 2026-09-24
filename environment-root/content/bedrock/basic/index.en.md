---
title : "📙 Basic patterns labs"
weight : 20001
---

::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting these labs.
::::

:::alert{header="Workspace setup" type="info"}
These labs use the `/environment` folder as the working directory. If your IDE has a different folder open, switch back using **☰ → File → Open Folder**

Alternatively, you can run :code[code /environment --reuse-window]{showCopyAction=true} from the web IDE's terminal.
:::


These labs assume no previous experience with Amazon Bedrock or Streamlit. They will introduce you to the core patterns for working with foundation models. All the other labs in the workshop build on these patterns.

These patterns can be used to solve some basic real-world use cases. These labs do not require any additional supporting infrastructure or integrations beyond Amazon Bedrock API calls.

_Screenshots from some of the labs in this section:_

| | | |
| --- | --- | --- |
| ![Streamlit Text to Text app showing a text area with the prompt "What is a good name for a product that provides large language models?" and the model's response suggesting the name "Gigaton AI"](/static/labs/bedrock-text/app-in-use.png) | ![Streamlit Retrieval-Augmented Generation app showing the question "What can you do with Guardrails for Amazon Bedrock?" with a detailed bulleted answer from the model describing features such as defining denied topics](/static/labs/bedrock-rag/app-in-use.png) | ![Streamlit Chatbot app showing a multi-turn conversation with alternating user and assistant message bubbles, asking about rainbow colors and guitar strings, with a text input field at the bottom](/static/labs/bedrock-chatbot/app-in-use.png) |




Each lab is self-contained, and can be done in any order.

::children

