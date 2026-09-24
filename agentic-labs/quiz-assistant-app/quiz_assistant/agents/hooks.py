"""Hook provider definitions for agents"""

from typing import Any
from threading import Lock

from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent, HookProvider, HookRegistry


class ToolCallRecorderHookProvider(HookProvider):
    """Conditionally records tool use requests and results and makes them available in AgentResult.state"""

    def __init__(self, record_requests: bool = False, record_results: bool = False):
        self.record_requests = record_requests
        self.record_results = record_results
        self._lock = Lock()

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        if self.record_requests:
            registry.add_callback(BeforeToolCallEvent, self.before_tool_hook)
        if self.record_results:
            registry.add_callback(AfterToolCallEvent, self.after_tool_hook)

    def before_tool_hook(self, event: BeforeToolCallEvent) -> None:
        """Records all tool use requests in "tool_requests" in the AgentResult's "state" property"""
        with self._lock:
            req_state = event.invocation_state.setdefault("request_state", {})  # this should already exist
            tool_requests = req_state.setdefault("tool_requests", [])
            tool_requests.append(event.tool_use)

    def after_tool_hook(self, event: AfterToolCallEvent) -> None:
        """Records all tool results in "tool_results" in the AgentResult's "state" property"""
        with self._lock:
            req_state = event.invocation_state.setdefault("request_state", {})  # this should already exist
            tool_results = req_state.setdefault("tool_results", [])
            tool_results.append(event.result)


class ToolCallLimiterHookProvider(HookProvider):
    """Limits the total number of tool calls made during one agent invocation.
    For an example of per-tool limits, please see:
        https://strandsagents.com/docs/user-guide/concepts/agents/hooks/#limit-tool-counts
    """

    def __init__(self, max_tool_calls_per_invocation: int):
        self.max_tool_calls_per_invocation = max_tool_calls_per_invocation
        self._lock = Lock()

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        if self.max_tool_calls_per_invocation >= 0:
            registry.add_callback(BeforeToolCallEvent, self.check_tool_call_count)

    def check_tool_call_count(self, event: BeforeToolCallEvent) -> None:
        """Records all tool use requests in "tool_requests" in the AgentResult's "state" property"""
        with self._lock:
            req_state = event.invocation_state.setdefault("request_state", {})  # this should already exist
            tool_call_count = req_state.get("tool_call_count", 0)

            if tool_call_count >= self.max_tool_calls_per_invocation:
                event.cancel_tool = (
                    f"Maximum limit of {self.max_tool_calls_per_invocation} calls reached for this "
                    f"user request. Wait until an additional user request to attempt to call a tool again."
                )
            else:
                req_state["tool_call_count"] = tool_call_count + 1
