"""A proactive conversation summarization manager"""

from typing import Optional, Any

from strands import Agent

from strands.agent.conversation_manager import SummarizingConversationManager


class ProactiveSummarizingConversationManager(SummarizingConversationManager):
    """Proactively summarizes messages after maximum_message_count_before_summarizing is reached"""

    def __init__(
        self,
        summary_ratio: float = 0.3,
        preserve_recent_messages: int = 10,
        summarization_agent: Optional["Agent"] = None,
        summarization_system_prompt: Optional[str] = None,
        maximum_message_count_before_summarizing: int = 20,
    ):
        if maximum_message_count_before_summarizing < preserve_recent_messages + 2:
            raise ValueError(
                "maximum_message_count_before_summarizing must be at least 2 greater than preserve_recent_messages."
            )

        super().__init__(
            summary_ratio=summary_ratio,
            preserve_recent_messages=preserve_recent_messages,
            summarization_agent=summarization_agent,
            summarization_system_prompt=summarization_system_prompt,
        )

        self.maximum_message_count_before_summarizing = maximum_message_count_before_summarizing

    def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
        """Proactively apply summarization after maximum_message_count_before_summarizing"""
        if len(agent.messages) > (self.maximum_message_count_before_summarizing):
            self.reduce_context(agent=agent)
