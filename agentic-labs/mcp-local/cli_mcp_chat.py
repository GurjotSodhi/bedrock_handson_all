"""
A simple command-line interface for chatting with an agent.
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

BOT_PREFIX = "\033[1;36m\n🤖Bot:"
HUMAN_PREFIX = "\033[0;33m\n\n🙂Me:\n"


def main():
    """Runs a CLI-based chat with the agent"""

    mcp_client = MCPClient(
        lambda: stdio_client(StdioServerParameters(command="python", args=["math_fastmcp_server.py"]))
    )

    with mcp_client:
        tools = mcp_client.list_tools_sync()
        agent = Agent(tools=tools, model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

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
