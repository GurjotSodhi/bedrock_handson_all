"""Command line interface for the agent."""

import argparse
from basic_agent import create_agent


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", help="The prompt to send to the agent.", required=True)
    return parser.parse_args()


def main(prompt: str):
    """Main logic for command line interface"""
    agent = create_agent()

    agent(prompt)


if __name__ == "__main__":
    args = parse_args()
    main(args.prompt)
