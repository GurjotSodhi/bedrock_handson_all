"""Script to list memories"""

import os

from bedrock_agentcore.memory.session import MemorySessionManager

ACTOR_ID = os.getenv("DEMO_ACTOR_ID")
MEM_ID = os.getenv("DEMO_MEMORY_ID")


def print_sessions(actor_id: str):
    """Print all sessions for a given actor."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    actor_sessions = session_manager.list_actor_sessions(actor_id=actor_id)
    print("#" * 40)
    print("SESSIONS")

    for actor_session in actor_sessions:
        print(actor_session)


def print_memories_by_prefix(actor_id: str):
    """Print long-term memory records grouped by namespace prefix."""
    session_manager = MemorySessionManager(memory_id=MEM_ID, region_name="us-west-2")

    print("#" * 40)
    print("MEMORIES")
    for prefix in [f"/preferences/{actor_id}/", f"/facts/{actor_id}/", f"/summaries/{actor_id}/"]:

        print()
        print("-" * 40)
        print(prefix)
        print()

        memory_records = session_manager.list_long_term_memory_records(namespace_prefix=prefix)

        for record in memory_records:
            memory = record.get("content", {}).get("text", "")

            print(memory)
            print()


if __name__ == "__main__":
    print_sessions(actor_id=ACTOR_ID)
    print_memories_by_prefix(actor_id=ACTOR_ID)
