"""Pie chart tool schema example"""

from typing import List

import matplotlib
import matplotlib.pyplot as plt
from strands import tool

import agent_testing_utils


@tool(
    description="Create a pie chart and save it as a PNG file.",
    inputSchema={
        "json": {
            "properties": {
                "title": {"description": "Title for the pie chart", "type": "string", "minLength": 2, "maxLength": 50},
                "labels": {
                    "description": "List of labels for each pie slice",
                    "items": {"type": "string", "minLength": 1},
                    "type": "array",
                    "minItems": 1,
                },
                "values": {
                    "description": "List of numeric values for each pie slice",
                    "items": {"type": "number", "minimum": 0},
                    "type": "array",
                    "minItems": 1,
                },
                "shadow": {
                    "default": False,
                    "description": "Whether to draw a shadow beneath the pie chart",
                    "type": "boolean",
                },
                "startangle": {"default": 0, "description": "The starting angle for the pie chart.", "type": "integer"},
                "color_sequence": {
                    "description": "The matplotlib color sequence for the chart",
                    "enum": ["tab10", "Pastel1", "Accent"],
                    "type": "string",
                    "default": "tab10",
                },
            },
            "required": ["title", "labels", "values"],
            "type": "object",
        }
    },
)
def create_pie_chart(
    title: str,
    labels: List[str],
    values: List[float],
    shadow: bool = False,
    startangle: int = 0,
    color_sequence: str = "tab10",
) -> str:
    """Pie chart tool"""

    matplotlib.use("agg")
    fig, ax = plt.subplots()

    colors = matplotlib.color_sequences.get(color_sequence, matplotlib.color_sequences["Pastel1"])

    ax.pie(values, labels=labels, autopct="%1.1f%%", shadow=shadow, startangle=startangle, colors=colors)
    ax.set_title(title)
    file_name = "pie_chart.png"
    fig.savefig(file_name)
    plt.close(fig)

    return f"Successfully created {file_name}!"


agent_testing_utils.display_and_test_decorated_function(
    create_pie_chart, prompt="Create a pastel pie with some made-up data."
)
