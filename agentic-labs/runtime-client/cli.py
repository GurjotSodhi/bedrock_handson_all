"""Command line interface for the agent."""

import json
import uuid
import argparse

import math_client


def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", help="The prompt to send to the agent.", required=True)
    parser.add_argument("--session-id", "-s", help="The user session.", required=False)
    return parser.parse_args()


def main(prompt: str, session_id: str):
    """Main logic for command line interface"""

    if not session_id:
        session_id = str(uuid.uuid4())

    result = math_client.invoke_agentcore_runtime(prompt=prompt, session_id=session_id)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    args = parse_args()
    main(prompt=args.prompt, session_id=args.session_id)
