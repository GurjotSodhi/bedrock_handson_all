"""Deletes all long-term memories across all namespace prefixes."""

import os

from bedrock_agentcore.memory.session import MemorySessionManager

MEM_ID = os.getenv("DEMO_MEMORY_ID")


def delete_all_memories():
    """Delete all long-term memories across all namespace prefixes."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    namespaces = [
        "/preferences/",
        "/facts/",
        "/summaries/",
    ]

    for namespace in namespaces:
        print(f"Deleting memories in: {namespace}")
        session_manager.delete_all_long_term_memories_in_namespace(namespace=namespace)
        print("Done.")

    print("\nAll memories deleted.")


if __name__ == "__main__":
    delete_all_memories()
