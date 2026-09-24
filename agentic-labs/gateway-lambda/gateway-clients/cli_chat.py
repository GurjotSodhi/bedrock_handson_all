"""
A simple command-line interface for chatting with an agent.
"""

from gateway_agent import create_agent, create_mcp_client

BOT_PREFIX = "\033[1;36m\n🤖Bot:"
HUMAN_PREFIX = "\033[0;33m\n\n🙂Me:\n"


def main():
    """Runs a CLI-based chat with the agent"""

    mcp_client = create_mcp_client()

    with mcp_client:
        agent = create_agent(mcp_client=mcp_client)

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
                agent(prompt)
            except KeyboardInterrupt:
                print("\nBye!\n")
                break


if __name__ == "__main__":
    main()
