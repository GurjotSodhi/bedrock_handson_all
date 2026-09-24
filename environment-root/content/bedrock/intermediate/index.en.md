---
title : "📚 Text patterns labs"
weight : 30001
---


::::alert
If running from an AWS event or AWS Builder Center, please be sure to have set up your [development environment using the instructions here.](/aws-hosted/launch-environment) If running from your own account, please complete the [Prerequisites](/prerequisites/) section before starting these labs.
::::

:::alert{header="Workspace setup" type="info"}
These labs use the `/environment` folder as the working directory. If your IDE has a different folder open, switch back using **☰ → File → Open Folder**

Alternatively, you can run :code[code /environment --reuse-window]{showCopyAction=true} from the web IDE's terminal.
:::

These labs assume no previous experience with Amazon Bedrock or Streamlit. That said, if you haven't used one of these before, you would benefit from doing the [Basic pattern labs](/bedrock/basic) in the workshop first.

In these intermediate labs, we expand on the techniques learned in the basic labs. We will start solving more real-world use cases. These labs do not require any additional supporting infrastructure or integrations beyond Amazon Bedrock API calls.



_Screenshots from some of the labs in this section:_

| | | |
| --- | --- | --- |
| ![RAG Chatbot app showing a multi-turn conversation where the user asks "what can you do with it?" and the model responds with a bulleted list of Amazon Bedrock capabilities](/static/labs/bedrock-rag-chatbot/app-in-use.png) | ![Document Summarization app displaying a user prompt asking for the three most important elements for an intern, followed by a structured Summary section with key points from an Amazon Leadership Principles document](/static/labs/bedrock-summarization/app-in-use.png) | ![Response Streaming app with a text area containing the prompt "Write a story about two cats that go on an adventure", a Go button, and a spinning loading indicator showing the response is being streamed](/static/labs/bedrock-streaming/streaming-ui.gif) |
| ![Personalized Recommendations app where the user entered "A cloud NoSQL database service for massive amounts of data" and the model recommended Amazon DynamoDB with a numbered list of supporting reasons](/static/labs/bedrock-personalized-recommendations/app-in-use.png) | ![Text to JSON app with a two-column layout: an input letter on the left complaining about an account manager named Roger Longbottom, and the extracted JSON result on the right containing fields like summary, escalate_complaint, overall_sentiment, and sentiment_towards_employees](/static/labs/bedrock-json/app-in-use.png) | ![Text to CSV app showing an input letter praising a customer service representative named Shirley Scarry, with the structured result displayed as a table and raw CSV below, containing fields like escalate_complaint, level_of_concern, overall_sentiment, and summary](/static/labs/bedrock-csv/app-in-use.png) |






Each lab is self-contained, and can be done in any order.

::children

