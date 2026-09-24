"""Command line interface for the agent."""

import argparse
import json

from product_reviews.agents import product_reviews_agent


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--review_content", "-r", help="The review content to send to the agent.", required=True)
    return parser.parse_args()


def main(review_content: str):
    """Main logic for command line interface"""

    try:
        result = product_reviews_agent.run_agent_workflow(review_content=review_content)

        print(result)
        print(result.model_dump_json(indent=4))

    except KeyboardInterrupt:
        print("\nBye!\n")


if __name__ == "__main__":
    args = parse_args()
    main(args.review_content)
