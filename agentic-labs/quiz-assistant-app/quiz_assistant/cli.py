"""Command line interface for the agent."""

import json
import argparse
from quiz_assistant.agents import quiz_agent


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", help="The prompt to send to the agent.", required=True)
    return parser.parse_args()


def main(prompt: str):
    """Main logic for command line interface"""

    try:
        agent = quiz_agent.create_quiz_agent()

        result = agent(prompt)

        print("-" * 40)
        print("result.state as JSON:")
        print("-" * 40)
        print(json.dumps(result.state, indent=4))

    except KeyboardInterrupt:
        print("\nBye!\n")


if __name__ == "__main__":
    args = parse_args()
    main(args.prompt)
