"""Command line interface for the agent."""

import argparse
import line_drawing_agent


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", help="The prompt to send to the agent.", required=True)
    parser.add_argument("--model", "-m", help="The Amazon Bedrock model ID to use.", required=False)
    return parser.parse_args()


def main(prompt: str, model_id: str):
    """Main logic for command line interface"""

    line_drawing_agent.run_line_drawing_workflow(prompt, model_id=model_id)


if __name__ == "__main__":
    args = parse_args()
    main(args.prompt, args.model)
