"""Product reviews agent"""

from strands import Agent
from product_reviews.types.structures import ReviewAnalysis


def run_agent_workflow(review_content: str) -> ReviewAnalysis:
    """Create and run the agent workflow"""

    agent = Agent(
        system_prompt="Analyze the provided product review.",
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    prompt = f"Review Content: {review_content}"

    analysis_response = agent(prompt=prompt, structured_output_model=ReviewAnalysis)

    return analysis_response.structured_output
