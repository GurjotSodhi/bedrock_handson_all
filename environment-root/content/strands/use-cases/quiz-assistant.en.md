---
title: "Quiz assistant"
weight: 2000
---





_Final product:_

![Screenshot of a Quiz Assistant application interface showing a dark-themed web application. On the left side is a chat panel with conversation history about creating a "Kitten Quiz" with 4 questions about kitten development stages and costs. On the right side is the quiz display showing "Kitten Quiz" with two multiple-choice questions: "At what age do kittens typically open their eyes?" and "When do kittens usually start eating solid food?" Each question has four answer options (A-D) with the correct answers marked. At the bottom is a chat input field for interacting with the bot.](/static/images/use-cases/quiz-assistant/quiz_assistant_1.png)

&nbsp;


## Prerequisites

Please make sure you are comfortable with the following topics before proceeding:

* [Messages and content blocks](/strands/fundamentals/messages/)
* [Tool schema](/strands/fundamentals/tool-schema/)
* [Building agentic demo apps](/strands/fundamentals/demo-apps/)
* [Event hooks](/strands/intermediate-topics/event-hooks/)

&nbsp;


## Purpose

In this exercise, we'll take the theory we've learned about [agents](/strands/fundamentals/agents) and [tool schema](/strands/fundamentals/tool-schema) and apply it to a real-world problem: generating quizzes from content.

We might want to generate quizzes for self-directed learners, to help them test reading comprehension after finding a story or article that interests them. This could also help test comprehension for foreign language learners. Or this could help an educator quickly create a quiz as part of a custom lesson plan.

&nbsp;

## Problem framing

We want to solve a few things here:

1. Make it easy to quickly generate a quiz based on a piece of content
2. Make it easy to iterate on the quiz to fix any problems
3. Use a data structure that could be imported into a learning management system, educational app, or printed out for students.


&nbsp;

## Potential solutions

We could keep this simple and just accept a single user prompt with the content and quiz request, but that assumes the LLM will generate a good quiz without any additional feedback.

We could use structured output to generate the quiz, but that could mean the quiz's structured output would be generated after each user message.

In this case, we're going to go with a chatbot and tool use. By using tool use with a chatbot, the LLM can choose whether or not to generate a quiz after receiving information from the user. This allows the user to brainstorm ideas with the chatbot, generate a quiz when ready, and then selectively edit portions of the quiz as needed.

Because an LLM can call a tool multiple times, in theory the LLM might generate multiple quizzes at once. This could clutter the user interface. So we'll need a way to limit the number of quizzes generated at a time. We mentioned in the [Event hooks](/strands/intermediate-topics/event-hooks) section that the **BeforeToolCallEvent** can be used to limit & cancel tool calls, so we'll implement that in this lab.

In a real world scenario, we might want to save the quiz to a database or file. For demo purposes, we'll just work with the quiz in memory. We'll also use the Tool call recorder implementation from the [Callback and hooks](/strands/intermediate-topics/event-hooks) section to present the generated quiz directly to the user.

&nbsp;




## Solution walkthrough 

The code for this solution can be found under **/environment/workshop/agentic-labs/quiz-assistant-app**

```bash
cd /environment/workshop/agentic-labs/quiz-assistant-app
```

&nbsp;


### Create the tool for quiz creation

Review the code in **quiz_assistant/tools/quiz_tools.py**. In this module, we create the `create_quiz` tool using the [inputSchema tool schema approach](/strands/fundamentals/tool-schema/). Note the stub for the `question_schema` variable. We'll revisit this during the challenge exercises.

&nbsp;


### Define hook providers to capture tool details and limit tool use calls

Review the code in **quiz_assistant/agents/hooks.py**. Here we have two hook providers:

* We'll use the `ToolCallRecorderHookProvider` class that we highlighted earlier in the [Event hooks](/strands/intermediate-topics/event-hooks/) section. This will allow us to capture the results of each tool call in a list.

* We also want this application to only support the editing of one quiz at a time. We'll use the `ToolCallLimiterHookProvider` class to restrict the number of tool calls per agent invocation. You can see the [Strands documentation on hooks](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/#limit-tool-counts) to see an alternative approach to limiting tool calls per tool.


&nbsp;


### Create an agent

Review the code in **quiz_assistant/agents/quiz_agent.py**. Here we define an agent that can collaborate with the user to create and modify a quiz. We reference both of the classes from **hooks.py**:

* The `ToolCallRecorderHookProvider` is configured to return all tool call results
* The `ToolCallLimiterHookProvider` is configured to limit tool calls to once per `agent()` invocation


&nbsp;

### Create a command-line app

Review the code in **quiz_assistant/cli.py**. Here we create a basic command line script to take a prompt and pass it to the agent.

&nbsp;






## Challenge #1: Complete the quiz schema

We currently have an empty dictionary for the `question_schema` variable in **quiz_assistant/tools/quiz_tools.py**. Recall from the [Tool schema](/strands/fundamentals/tool-schema/) section that this will be in the JSON schema format. Note that there is already a `quiz_schema` defined that assumes an array of `questions`. Will exist. `quiz_schema` then references `question_schema` that you will need to define.

Come up with a JSON schema for the quiz questions. Here are some requirements:

1. Each question should have the question text
2. Each question should have 3-5 potential answers
3. Each question should indicate which answer is correct
4. OPTIONAL: Include an explanation of why the answer is correct


&nbsp;

::::expand{header="Challenge #1: tips" variant="container"}
* See the [Tool schema](/strands/fundamentals/tool-schema/) section if you need a refresher on defining tool schema.
* `question_schema` is a dictionary that should include values for "description", "type", "properties", and "required".
* Just like questions are a nested list under a quiz, answer choices could also be a nested list under a question.
::::



### Test the command line app.

From the **quiz-assistant-app** directory, install the local project:

```bash
pip install -e .
```

Then cd into the code folder:

```bash
cd quiz_assistant
```


Run the following command to test the CLI app:

```bash
python cli.py --prompt "Create a two-question quiz about kittens"
```

&nbsp;

::::expand{header="Challenge #1: potential solution" variant="container"}

Here's one example that works reasonably well.

1. To keep things readable, we use both `question_schema` and `choice_schema`.
2. We implemented `choices` as a list of nested choice objects.
3. We chose to indicate the correct choice directly on the choice object. Alternatively, we could have indicated the correct answer on the question object directly.
4. We use maxItems and minItems to limit each question to 3-5 choices.

```python
choice_schema = {
    "description": "A choice candidate for the question",
    "type": "object",
    "properties": {
        "choice_label": {
            "description": "The label for the choice - assume letter values like A, B, C, D, E unless told otherwise.",
            "type": "string",
        },
        "choice_text": {"description": "The text to be displayed for the choice", "type": "string"},
        "is_correct_answer": {
            "description": "Indicates whether this is the correct answer for the question",
            "type": "boolean",
        },
    },
    "required": ["choice_label", "choice_text", "is_correct_answer"],
}

question_schema = {
    "description": "A single choice question",
    "type": "object",
    "properties": {
        "question_text": {"description": "The main question text to be asked", "type": "string"},
        "explanation": {"description": "Explanation for why the correct answer is right", "type": "string"},
        "choices": {
            "description": "Array of possible answer choices. Only one can be correct.",
            "items": choice_schema,
            "maxItems": 5,
            "minItems": 3,
            "type": "array",
        },
    },
    "required": ["question_text", "explanation", "choices"],
}
```

::::

&nbsp;



The CLI app will just display the JSON of the tool results. To make this demo more compelling, we'll now implement a simple Streamlit app to demonstrate the functionality.




## Create the Streamlit app

### Create the supporting logic

Review the code in **quiz_assistant/ui_demo_logic.py**. Here we create the following:

1. A `ChatMessage` class to store messages for the user interface
2. A `chat_with_agent` function to bridge between the user interface and the agent object
3. A `create_download_content` function to allow the user to download the JSON of the quiz.

&nbsp;

### Create the presentation layer

Review the code in **quiz_assistant/ui_demo_app.py**. Here we have a chat interface that the user can brainstorm, generate, and modify the quiz in collaboration with the LLM.

Once the quiz is generated, it will be displayed in a user-friendly way in the interface.

### Challenge #2: Display your custom question object

If you completed Challenge #1, you should now adapt the code under `with quiz_container:` in **quiz_assistant/ui_demo_app.py** to work with your question object. Alternatively, you can just use the solution for Challenge #1 in order to work with the existing display format in the Streamlit app.

&nbsp;

### Run the streamlit app

```bash
streamlit run ui_demo_app.py
```

You should see an app that looks something like this:

![A screenshot of a Quiz Assistant application interface showing a conversation about creating quizzes. On the left side, there's a chat conversation where the user requests creating quizzes about kittens and puppies, and the assistant responds that it successfully created a Kittens Quiz with 5 questions but can only create one quiz at a time. On the right side, there's an active "Kittens Quiz" displaying multiple choice questions about kitten facts, including questions about when kittens open their eyes and their sleep patterns, with answer options and an explanation section visible.](/static/images/use-cases/quiz-assistant/quiz_assistant_2.png)


Try brainstorming with the agent first, then generating a quiz based on that brainstorming. Ask the LLM to make changes to the quiz in different ways.

&nbsp;

## Commentary

This example demonstrates a tool with a moderately complex structure of nested objects (quiz -> questions -> choices). It also shows the usefulness of extending Strands through custom hooks to support a user interface and enforce business rules. 

&nbsp;

## Challenge yourself

* Try altering the tool schema to number the questions.
* Add the ability to generate a quiz from an uploaded document (See the [multimodal section](/strands/intermediate-topics/multimodal) and the [Streamlit file_uploader control](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader))
* _ADVANCED:_ Create a tool that allows another agent to take the test, then grades the result.


&nbsp;

---

&nbsp;

::alert[You have successfully built a quiz assistant demo!]{header="Congratulations!" type="success"}

