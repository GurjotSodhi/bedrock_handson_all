"""Tools for creating content including charts, tables, and commentary."""

import time
from typing import Annotated, List

import matplotlib.pyplot as plt
import matplotlib

from strands import tool


def get_timestamp_file_name(prefix: str, extension: str) -> str:
    """Generate a timestamped filename with the given prefix and extension."""
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")

    return f"generated_images/{prefix}_{timestamp}.{extension}"


@tool(description="Create a pie chart and save it as a PNG file.")
def create_pie_chart(
    labels: Annotated[List[str], "List of labels for each pie slice"],
    values: Annotated[List[float], "List of numeric values for each pie slice"],
    title: Annotated[str, "Title for the pie chart"],
    accessible_caption: Annotated[str, "Accessible caption describing the chart for screen readers"],
) -> dict:
    """Pie chart tool."""

    try:
        matplotlib.use("agg")
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title(title)
        file_name = get_timestamp_file_name("chartmaker_pie", "png")
        fig.savefig(file_name)
        plt.close(fig)

        return {
            "status": "success",
            "content": [
                {
                    "json": {
                        "content_type": "chart",
                        "image_file_name": file_name,
                        "chart_type": "pie",
                        "accessible_caption": accessible_caption,
                    }
                }
            ],
        }
    except Exception as e:
        return {"status": "error", "content": [{"text": f"Failed to create pie chart: {str(e)}"}]}


# BEGIN CHALLENGE CONTENT: Define the bar chart tool ----------------------------------------------


@tool(description="Create a bar chart and save it as a PNG file.")
def create_bar_chart(
    labels: Annotated[List[str], "List of labels for each bar"],
    values: Annotated[List[float], "List of numeric values for each bar"],
    title: Annotated[str, "Title for the bar chart"],
    xlabel: Annotated[str, "Label for the x-axis"],
    ylabel: Annotated[str, "Label for the y-axis"],
    accessible_caption: Annotated[str, "Accessible caption describing the chart for screen readers"],
    horizontal: Annotated[bool, "Whether to display a horizontal bar chart"] = False,
) -> dict:
    """Bar chart tool."""
    matplotlib.use("agg")
    fig, ax = plt.subplots()
    if horizontal:
        ax.barh(labels, values)
    else:
        ax.bar(labels, values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    file_name = get_timestamp_file_name("chartmaker_bar", "png")
    fig.savefig(file_name)
    plt.close(fig)
    return {
        "status": "success",
        "content": [
            {
                "json": {
                    "content_type": "chart",
                    "image_file_name": file_name,
                    "chart_type": "bar",
                    "accessible_caption": accessible_caption,
                }
            }
        ],
    }


# END CHALLENGE CONTENT ---------------------------------------------------------------------------


@tool(description="Create a line chart and save it as a PNG file.")
def create_line_chart(
    xvalues: Annotated[List[float], "List of x-axis values for the line chart"],
    yvalues: Annotated[List[float], "List of y-axis values for the line chart"],
    title: Annotated[str, "Title for the line chart"],
    xlabel: Annotated[str, "Label for the x-axis"],
    ylabel: Annotated[str, "Label for the y-axis"],
    accessible_caption: Annotated[str, "Accessible caption describing the chart for screen readers"],
) -> dict:
    """Line chart tool."""
    matplotlib.use("agg")
    fig, ax = plt.subplots()
    ax.plot(xvalues, yvalues)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    file_name = get_timestamp_file_name("chartmaker_line", "png")
    fig.savefig(file_name)
    plt.close(fig)
    return {
        "status": "success",
        "content": [
            {
                "json": {
                    "content_type": "chart",
                    "image_file_name": file_name,
                    "chart_type": "line",
                    "accessible_caption": accessible_caption,
                }
            }
        ],
    }


@tool(description="Add a table to the document.")
def create_table(
    table: Annotated[List[dict], "A list of JSON objects that will be displayed as a table in the document"],
    table_heading: Annotated[str, "Heading for this table."],
    table_caption: Annotated[str, "A caption for this table."],
) -> dict:
    """Add a table to the document with the provided data, heading, and caption."""

    return {
        "status": "success",
        "content": [
            {
                "json": {
                    "content_type": "table",
                    "table": table,
                    "table_heading": table_heading,
                    "table_caption": table_caption,
                }
            }
        ],
    }


@tool(description="Add commentary to the document.")
def create_commentary(
    commentary: Annotated[str, "Commentary to be added to the document."],
    section_heading: Annotated[str, "Heading for this section of commentary."],
) -> dict:
    """Basic passthrough tool to capture commentary in isolation"""

    return {
        "status": "success",
        "content": [
            {"json": {"content_type": "commentary", "commentary": commentary, "section_heading": section_heading}}
        ],
    }
