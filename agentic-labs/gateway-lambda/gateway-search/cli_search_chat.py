"""
A simple command-line interface for chatting with an agent.
"""

import os

from gateway_search_agent import GatewaySearchAgent

BOT_PREFIX = "\033[1;36m\n🤖Bot:"
HUMAN_PREFIX = "\033[0;33m\n\n🙂Me:\n"

GATEWAY_URL = os.environ.get("DEMO_GATEWAY_URL")


def main():
    """Runs a CLI-based chat with the agent"""

    if not GATEWAY_URL:
        print("Error: DEMO_GATEWAY_URL environment variable is not set.")
        return

    # Ensures the MCP gateway connection is properly opened and closed
    with GatewaySearchAgent(gateway_url=GATEWAY_URL) as agent:

        print(
            f"""{BOT_PREFIX}
    Welcome! Type your message below and hit return to send.
    Type "exit", "quit", "done", "bye" or press Ctrl-C to exit."""
        )

        while True:  # loop until exited
            try:
                prompt = input(f"{HUMAN_PREFIX}")

                if prompt.lower() in ["exit", "quit", "done", "bye"]:
                    print("EXITING!!!")
                    break

                print(f"{BOT_PREFIX}")
                agent.chat(prompt)  # Strands agents stream their response to stdout by default
            except KeyboardInterrupt:
                print("\nBye!\n")
                break


if __name__ == "__main__":
    main()
