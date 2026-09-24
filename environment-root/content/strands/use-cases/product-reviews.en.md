---
title: "Product review analyzer"
weight: 1000
---


_Final product:_

![Review Analyzer web application interface showing a product review input form on the left and structured sentiment analysis results with aspect extraction and star rating on the right.](/static/images/use-cases/product-reviews/review_streamlit_app.png)

&nbsp;

## Prerequisites

Please make sure you are comfortable with the following topics before proceeding:

* [Structured output](/strands/fundamentals/structured-output)
* [Building agentic demo apps](/strands/fundamentals/demo-apps)

&nbsp;




## Purpose

In this exercise, we'll take the theory we've learned about [agents](/strands/fundamentals/agents) and [structured outputs](/strands/fundamentals/structured-output) and apply it to a real-world problem: extracting insights from product review text.

Most product reviews give you basic info - a star rating, some text, maybe a title. But what if you want to dig deeper? What if you need to understand how customers feel about specific product attributes like taste, value, or quality?

This walkthrough shows you how to build an agent that can analyze a product review's text and extract structured data about how the consumer feels about specific product aspects. Instead of manually reading through hundreds of reviews to understand more targeted customer sentiment, you'll have a tool that does the heavy lifting for you.


&nbsp;

## Problem framing

Traditional product reviews are pretty basic - some text and a rating between 1 and 5. That's fine for calculating an overall average sentiment, but it doesn't tell you much about the specific strengths and weaknesses of a product.

Say you're selling protein bars and you want to understand customer feedback. One review might say "Great taste but too expensive" while another says "Bland flavor but good value." Both might give 3 stars, but they're talking about completely different aspects of your product.

What if you could automatically extract specific insights like:

* How do customers feel about taste vs. price vs. nutrition?
* Which product attributes get mentioned most often?
* What quotes from reviews support each sentiment?

Instead of manually reading through hundreds of reviews to spot patterns, you could have structured data that tells you exactly where your product succeeds and where it needs work. And in the case of an e-commerce site, this data provides helpful additional context to consumers making product choices.

&nbsp;

## Potential solutions

You could approach this problem in a couple of ways. One option would be to give your agent tools - maybe a "sentiment analyzer" tool and a "quote extractor" tool that it could call as needed. That would work, but it adds complexity and cost since each tool call is a separate API request.

A simpler approach is to use structured output. With structured output, you can get all the analysis you need in a single step - the agent processes the review text and returns organized data about sentiment, quotes, and ratings all at once. It's faster, cheaper, and easier to work with.

For this walkthrough, we'll use structured output since it's the most efficient solution for this type of data extraction task.




&nbsp;

## Solution walkthrough 

The code for this solution can be found under **/environment/workshop/agentic-labs/product-reviews-app**

```bash
cd /environment/workshop/agentic-labs/product-reviews-app
```

&nbsp;


### Create the structured output classes

Review the code in **product_reviews/types/structures.py**. In this module, we have a placeholder `ReviewAnalysis` class that we'll use to generate the structured output.

&nbsp;

## Challenge #1: Complete the review analysis class definition

We currently have an empty definition for the `ReviewAnalysis` class in **product_reviews/types/structures.py**.

Come up with a definition for the `ReviewAnalysis` class. Here are some requirements:

1. The analysis should include an estimate for the user's star rating, based on the review text
2. The analysis should capture the sentiment for up to five different aspects of food products: Taste, Appearance, Smell, Nutrition, and Value
3. The analysis doesn't need to include an aspect if the user is neutral about it or doesn't mention it.
4. The analysis should include a relevant quote from the user's review for each aspect with positive or negative sentiment.

&nbsp;

::::expand{header="Challenge #1: tips" variant="container"}
* Recall from the [Structured output](/strands/fundamentals/structured-output/) section that this should use Pydantic Field() constructors to define the class's attributes.
* You'll probably need another class for aspect-specific sentiments.
::::




### Create an agent

Review the code in **product_reviews/agents/product_reviews_agent.py**. Now we'll define an agent that can analyze a product review. For this use case, we just need the agent to extract the structured output in a single step.
So we create a `run_agent_workflow` method that both creates and invokes the agent with the `structured_output_model` parameter.

&nbsp;

### Create a command-line app

Review the code in **product_reviews/cli.py**. Here we create a basic command line script to take a prompt and pass it to the agent.

&nbsp;





### Test the agent from the command line

From the **product-reviews-app** directory, install the local project:

```bash
pip install -e .
```

Then cd into the code folder:

```bash
cd product_reviews
```


Run the following command to test the CLI app:

```bash
python cli.py --review_content "Love these protein bars! The chocolate flavor is incredible - tastes like a real dessert. At $2.50 each they're a great deal compared to other premium bars. Will definitely buy again! "
```


If there were no errors in your implementation of the `ReviewAnalysis` class, this will print the structured output as a Python object and as JSON.

Did it work like you expected? You should see structured output that identifies different product aspects (taste, value) along with relevant quotes and sentiment analysis.

If something seems off, try tweaking your ReviewAnalysis model - maybe adjust the field descriptions or add constraints to guide the LLM toward better results.



&nbsp;

::::expand{header="Challenge #1: potential solution" variant="container"}

Here's one example that works reasonably well.

1. We use an integer field for `estimated_star_rating`, and restrict it to values between 1 and 5.
2. We create an additional Pydantic class, `ProductAspectSentiment` to capture the sentiment per aspect.
3. We use a Literal, `aspect_name`, to limit the available aspects to capture.
4. We use another Literal for sentiment, and limit it to "positive" or "negative" (in this case, we don't care about neutral sentiment)
5. We use a str field for `relevant_quote` with a brief description linking the quote to the aspect.

```python
class ProductAspectSentiment(BaseModel):
    """Captures the consumer's sentiment towards an aspect of the product."""

    aspect_name: Literal["Taste", "Appearance", "Smell", "Nutrition", "Value"] = Field(
        description="The aspect of the product"
    )

    relevant_quote: str = Field(description="A relevant quote from the review towards this aspect")

    sentiment: Literal["positive", "negative"] = Field(description="The consumer's sentiment towards this aspect")


class ReviewAnalysis(BaseModel):
    """Analysis results for a product review, including sentiment for different aspects."""

    aspect_sentiments: List[ProductAspectSentiment] = Field(
        description="A list of the aspects of the product towards which the consumer has an identifiable sentiment"
    )

    estimated_star_rating: int = Field(
        description="The estimated star rating based on the review content, between 1 and 5", ge=1, le=5
    )


```

::::

&nbsp;



To make this proof-of-concept more compelling, next we'll implement a simple Streamlit app to demonstrate the functionality.




## Create the Streamlit app

### Create the supporting logic

Review the code in **product_reviews/ui_demo_logic.py**. Here we create the following:


1. A `process_content` function to bridge between the user interface and the agent object
2. `format_as_markdown` and `get_presentable_key` functions to render the structured output in a friendlier format than a JSON dump



&nbsp;

### Create the presentation layer

Review the code in **product_reviews/ui_demo_app.py**. Here we have a simple form where the user can submit a product review.

Once the review is submitted, the analysis can be viewed in either "friendly" or "JSON" modes.

&nbsp;

### Run the streamlit app

```bash
streamlit run ui_demo_app.py
```

You should see an app that looks something like this:


![Review Analyzer web application interface showing a product review input form on the left and structured sentiment analysis results with aspect extraction and star rating on the right.](/static/images/use-cases/product-reviews/review_streamlit_app.png)


This interface on the left mimics what you might see on an e-commerce site where customers submit reviews. We display the results on the right, in "Friendly" mode for less technical viewers, and in "JSON" mode for diagnostic purposes.

Try a few reviews:

```text
Love these protein bars! The chocolate flavor is incredible - tastes like 
a real dessert. At $2.50 each they're a great deal compared to other 
premium bars. Will definitely buy again!
```

```text
The packaging looks really professional and sleek. When I opened the 
container, there was a pleasant vanilla aroma that made me excited to try it. 
Definitely impressed with the presentation.
```

```text
Tastes terrible - way too sweet and artificial. However, the nutrition 
label is solid with 25g protein and no junk ingredients. Unfortunately 
it's overpriced at $45 for such a small container.
```

One interesting feature would be to compare the user's star rating with the agent's estimated rating - if they differ by more than one star, you could flag it as a potential data quality issue or confirm if the user mistakenly selected the wrong rating.

&nbsp;

## Commentary

This example demonstrates how structured output can solve real business problems with minimal code. Instead of building complex parsing logic or multiple tool calls, we defined a Pydantic model and let the LLM do the heavy lifting.

&nbsp;

## Challenge yourself

1. **Custom aspects** - Make the product aspects configurable so the same system can work for different product categories (electronics, food, clothing).

2. **Translation support** - Modify the agent to handle reviews in different languages and return results in your preferred language.

3. **Image analysis** - Add support for user-provided images in reviews. Match the image to the most relevant product aspects (ex: a tear in the fabric could match a shirt's `quality` aspect).



&nbsp;

---

&nbsp;

::alert[You have successfully built a product review analyzer demo!]{header="Congratulations!" type="success"}

