"""The supporting logic for the streamlit app"""

from data_storyteller.agents import storyteller_agent


def generate_report(topic: str):
    """Requests and returns a report generation"""
    result = storyteller_agent.run_storyteller_agent_workflow(topic)

    return result
