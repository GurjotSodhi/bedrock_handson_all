---
title: "Data storyteller"
weight: 3000
---


_Final product:_

![The Data Storyteller application interface showing an AI-generated EU sales report with a pie chart displaying unit sales distribution across five European countries and accompanying executive summary and market analysis sections.](/static/images/use-cases/data-storyteller/data_storyteller_1.png)

&nbsp;


## Prerequisites

Please make sure you are comfortable with the following topics before proceeding:

* [Messages and content blocks](/strands/fundamentals/messages/)
* [Tool function parameters](/strands/fundamentals/function-decorators/)
* [Building agentic demo apps](/strands/fundamentals/demo-apps/)
* [Event hooks](/strands/intermediate-topics/event-hooks/)

&nbsp;


## Purpose

In this exercise, we'll take the theory we've learned about [tool function parameters](/strands/fundamentals/function-decorators/) and [hooks](/strands/intermediate-topics/event-hooks/) and apply it to a real-world problem: creating a report based on a set of data.

This can be helpful when we want to generate insights based on an arbitrary dataset, have limited time to create reports, or have limited access to reporting tools.

&nbsp;

## Problem framing

We want to solve the following:

1. Retrieve an arbitrary dataset in JSON form. For this demo, we'll keep its size small so we don't need to add data query capabilities.
2. Generate commentary about the data.
3. Generate visualizations of the data, including tables, pie charts, line charts, and bar charts.

&nbsp;

## Potential solutions

We could build this as a chatbot. This would allow us to interactively shape the report, but could be time consuming.

We could also allow the agent to pull in multiple datasets to feed into the report.

In this demo, we'll just focus on generating a report based on a single prompt and fixed dataset. That way the user can multi-task while waiting for the agent to come back with a report. A future version could include interactive editing and multiple datasets, but for now, we'll just prove out the basic report generation capability.

&nbsp;




## Solution walkthrough 

The code for this solution can be found under **/environment/workshop/agentic-labs/data-storyteller-app**

```bash
cd /environment/workshop/agentic-labs/data-storyteller-app
```

&nbsp;


### Creating a tool to retrieve mock data

Review the code in **data_storyteller/tools/data_retrieval_tools.py**. In this module, we declare a single tool called `retrieve_data` that takes no parameters, and returns a JSON content block. We're creating our own proprietary dictionary structure that will use the `content_type` attribute to determine how content will be rendered in the final data story.

For now, we'll just use mock data and pass no parameters to the tool. After this code is working, you can start thinking about how to retrieve the necessary data, and which parameters you would want to pass to select and filter that data for your data story.

&nbsp;


### Create tools for content creation

Review the code in **data_storyteller/tools/content_creation_tools.py**. This module contains the tools for content creation, including tools for pie charts, line charts, tabular data, and written commentary. In a real data story, you may want additional visualizations and content types. Note the stub implementation for the bar chart tool. We'll revisit this during the challenge exercises.

&nbsp;





### Define a hook provider to capture tool details 

Review the code in **data_storyteller/agents/hooks.py**. Here we use the `ToolCallRecorderHookProvider` class that we highlighted earlier in the [Event hooks](/strands/intermediate-topics/event-hooks/) section. This will allow us to capture the results of each tool call in a list.


&nbsp;


### Create an agent

Review the code in **data_storyteller/agents/storyteller_agent.py**. Here we define an agent that can generate the data story using the provided data and tools. This can be considered a "proper" agent, since it is given discretion to solve the problem as it sees fit, without a fixed process.

We've also included an `_extract_result_json` function, which we use to transform the raw tool results into a flattened format that we will use to render the data story. It also will make any errors visible in the generated story.

&nbsp;


### Create a command-line app

Review the code in **data_storyteller/cli.py**. Here we create a basic command line script to take a prompt and pass it to the agent.

&nbsp;


## Challenge #1: Define the agent's system prompt

We currently have an empty system prompt in **data_storyteller/agents/storyteller_agent.py**. Recall from [Messages and content blocks](/strands/fundamentals/messages/) that the system prompt is used to guide the behavior of the LLM.

Come up with a system prompt that explains its role, objective, and available tools. You may start small, then increase the system prompt as needed, depending on any issues you may see. The example solution consists of four short sentences. 

Assign your system prompt to the `STORYTELLER_SYSTEM_PROMPT` variable.

&nbsp;

### Test the command line app.

From the **data-storyteller-app** directory, install the local project:

```bash
pip install -e .
```

Then cd into the code folder:

```bash
cd data_storyteller
```


Run the following command to test the CLI app:

```bash
python cli.py --prompt "Create a brief data story about our German performance"
```

&nbsp;

::::expand{header="Challenge #1: potential solution" variant="container"}

Here's one example that works reasonably well.

1. Initial tests showed the LLM repeating the same chart type several times, so we encourage the LLM to use a mix of tools to avoid repetition.
2. Follow-up tests also showed the LLM clustering visualizations together, so we ask the LLM to alternate between text and visualization.
3. We also request an executive summary to help set the tone and consistency of the data story.

```python
STORYTELLER_SYSTEM_PROMPT = """You are a data storyteller.
Use a mix of commentary, charts, and tables to explain the data.
Be sure to alternate between text commentary and visualizations.
Always start with an executive summary.
"""
```

::::

&nbsp;

With the command line tool, we end up with a not-too-friendly JSON dump, Let's create a Streamlit app to display the data story in a web app.

&nbsp;

## Create the Streamlit app

### Create the supporting logic

Review the code in **data_storyteller/ui_demo_logic.py**. Here we create a simple function to invoke the agent.

&nbsp;

### Create the presentation layer

Review the code in **data_storyteller/ui_demo_app.py**. Here we have a basic application that accepts the user's guidance for the report to generate.

Once the report is generated, the application loops through the report elements and displays them with the various render functions for each `content_type`. Note that any attempts to generate a bar chart will be displayed as an error.

&nbsp;

### Run the streamlit app

```bash
streamlit run ui_demo_app.py
```

You should see an app that looks something like this:

![The Data Storyteller application interface showing an AI-generated EU sales report with a pie chart displaying unit sales distribution across five European countries and accompanying executive summary and market analysis sections.](/static/images/use-cases/data-storyteller/data_storyteller_1.png)

Additional detail:

![A business dashboard showing country performance metrics with a data table displaying units sold, profits, employees, and year-over-year growth for five European countries (Netherlands, Germany, Italy, Spain, France), followed by an analysis section highlighting growth trends and performance concerns across these markets.](/static/images/use-cases/data-storyteller/data_storyteller_detail.png)

&nbsp;

## Challenge #2: Define the bar chart tool

Implement the `create_bar_chart` tool in **data_storyteller/tools/content_creation_tools.py**.

BONUS challenge: Allow the LLM to specify either a vertical or horizontal bar chart.

::::expand{header="Challenge #2: tips" variant="container"}
* See the [Tool function parameters](/strands/fundamentals/function-decorators/) section if you need a refresher on defining tools. 
* Review the `create_pie_chart` and `create_line_chart` tools for patterns you can reuse.
* See the [Matplotlib documentation](https://matplotlib.org/stable/api/pyplot_summary.html) to understand the options for creating a bar chart.
::::


Use the following prompt to test the bar chart tool in relative isolation:
```text
Create only one bar chart about our German performance
```


::::expand{header="Challenge #2: potential solution" variant="container"}

Review the code in **data_storyteller/tools/content_creation_tools_solution.py**.

This solution is effectively a halfway point between the pie chart and the line chart. It uses both x and y labels like the line chart, but requires a series of values and labels like the pie chart.

To solve the bonus challenge, we also added a `horizontal` boolean argument that toggles whether the `bar` or `barh` Matplotlib functions are called.

::::


&nbsp;


## Commentary

This example demonstrates how powerful a simple agent loop and tools created only with function decorators and parameter annotations can be. It also shows the usefulness of extending Strands through custom hooks to support a user interface.

&nbsp;

## Challenge yourself

* Review the [list of plot types from Matplotlib](https://matplotlib.org/stable/plot_types/index.html). Try creating a tool to generate an additional plot type.
* Try creating some mock data in your area of interest. Does this require changes to your prompts or tools?
* Try creating several different data sources that the agent can choose from, based on your prompt. How does the agent incorporate these data sources into the report?


&nbsp;

---

&nbsp;

::alert[You have successfully built a data storyteller demo!]{header="Congratulations!" type="success"}

