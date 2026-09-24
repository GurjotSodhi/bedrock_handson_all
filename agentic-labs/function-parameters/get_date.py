"""A tool with no parameters"""

from datetime import datetime, timezone

from strands import tool

import agent_testing_utils


@tool(description="Returns the current UTC date in ISO 8601 format")
def get_current_utc_date() -> str:
    """Tool to return current UTC date in "2025-01-30" format."""
    return datetime.now(timezone.utc).date().isoformat()


agent_testing_utils.display_and_test_decorated_function(get_current_utc_date, prompt="What UTC date is it?")
