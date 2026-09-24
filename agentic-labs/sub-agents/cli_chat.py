"""
A simple command-line interface for chatting with an agent.
"""

import orchestrator_agent

BOT_PREFIX = "\033[1;36m\n🤖Bot:"
HUMAN_PREFIX = "\033[0;33m\n\n🙂Me:\n"


def main():
    """Runs a CLI-based chat with the agent"""
    agent = orchestrator_agent.create_orchestrator_agent()

    print(
        f"""{BOT_PREFIX}
Welcome! Type your message below and hit return to send.
Type "exit", "quit", "done", "bye" or press Ctrl-C to exit."""
    )

    while True:  # loop until exited
        try:
            prompt = input(f"{HUMAN_PREFIX}")

            if prompt.lower() in ["exit", "quit", "done", "bye"]:
                break

            print(f"{BOT_PREFIX}")
            agent(prompt)
        except KeyboardInterrupt:
            print("\nBye!\n")
            break


if __name__ == "__main__":
    main()
