"""CLI tool to search long-term memories using semantic search."""

import os
import argparse

from bedrock_agentcore.memory.session import MemorySessionManager


def search_actor_memory_records(
    actor_id: str, query: str, top_k: int = 3, namespace: str = "/facts/{actorId}/"
) -> list:
    """Search long-term memories based on a query."""
    # Read memory ID from file
    mem_id = os.getenv("DEMO_MEMORY_ID")

    region_name = "us-west-2"

    session_manager = MemorySessionManager(memory_id=mem_id, region_name=region_name)

    namespace_prefix = namespace.format(actorId=actor_id)

    # Search memories
    memory_records = session_manager.search_long_term_memories(
        query=query, namespace_prefix=namespace_prefix, top_k=top_k
    )

    return memory_records


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Search long-term memories using semantic search")
    parser.add_argument("--query", "-q", type=str, required=True, help="The search query to find relevant memories")
    parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of top results to return (default: 3)")
    parser.add_argument(
        "--namespace",
        "-n",
        type=str,
        default="/facts/{actorId}/",
        help="Namespace prefix to search within (default: '/facts/{actorId}/')",
    )

    return parser.parse_args()


def main():
    """Command-line interface entry point."""
    args = parse_args()

    print(f"Searching for: {args.query}")
    print(f"Top K: {args.top_k}")
    print(f"Namespace: {args.namespace}")

    actor_id = os.getenv("DEMO_ACTOR_ID")

    memory_records = search_actor_memory_records(
        actor_id=actor_id, query=args.query, top_k=args.top_k, namespace=args.namespace
    )

    # Display results
    if not memory_records:
        print("No memories found.")
    else:
        print(f"Found {len(memory_records)} result(s):\n")
        for record in memory_records:

            memory = record.get("content", {}).get("text", "")
            print(memory)
            print()


if __name__ == "__main__":
    main()
