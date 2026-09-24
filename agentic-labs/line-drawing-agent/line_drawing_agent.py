"""The line drawer agent module"""

import time
import json
from typing import Annotated, Literal

from PIL import Image, ImageDraw, ImageColor
from strands import Agent, tool
from strands.tools.executors import SequentialToolExecutor


class LineDrawer:
    """Class with line drawing methods"""

    LINE_COLORS = Literal["red", "green", "blue", "yellow", "orange", "purple"]

    def __init__(self):
        self.im = Image.new("RGB", (200, 200), (255, 255, 255))
        self.images = [self.im]

    def _get_draw(self):
        im_to_copy = self.images[-1]
        im = im_to_copy.copy()
        self.images.append(im)
        draw = ImageDraw.Draw(im)
        return draw

    @tool(description="Draw a straight line between two points on the canvas")
    def draw_line(
        self,
        x0: Annotated[float, "Starting X coordinate (0-200)"],
        y0: Annotated[float, "Starting Y coordinate (0-200)"],
        x1: Annotated[float, "Ending X coordinate (0-200)"],
        y1: Annotated[float, "Ending Y coordinate (0-200)"],
        color: Annotated[LINE_COLORS, "Color of the line"],
    ):
        """Line tool."""
        draw = self._get_draw()
        rgb_color = ImageColor.getrgb(color)

        draw.line((x0, y0, x1, y1), fill=rgb_color, width=5)

    @tool(description="Draw an arc (curved line) within a bounding box")
    def draw_arc(
        self,
        x0: Annotated[float, "Top-left X coordinate of bounding box (0-200)"],
        y0: Annotated[float, "Top-left Y coordinate of bounding box (0-200)"],
        x1: Annotated[float, "Bottom-right X coordinate of bounding box (0-200)"],
        y1: Annotated[float, "Bottom-right Y coordinate of bounding box (0-200)"],
        start_angle: Annotated[float, "Starting angle in degrees (0-360)"],
        end_angle: Annotated[float, "Ending angle in degrees (0-360)"],
        color: Annotated[LINE_COLORS, "Line color of the arc"],
    ):
        """Arc tool."""
        draw = self._get_draw()
        rgb_color = ImageColor.getrgb(color)
        draw.arc([(x0, y0), (x1, y1)], start=start_angle, end=end_angle, fill=rgb_color, width=5)

    @tool(description="Draw an ellipse (oval shape) outline within a bounding box")
    def draw_ellipse(
        self,
        x0: Annotated[float, "Top-left X coordinate of bounding box (0-200)"],
        y0: Annotated[float, "Top-left Y coordinate of bounding box (0-200)"],
        x1: Annotated[float, "Bottom-right X coordinate of bounding box (0-200)"],
        y1: Annotated[float, "Bottom-right Y coordinate of bounding box (0-200)"],
        color: Annotated[LINE_COLORS, "Line color of the ellipse"],
    ):
        """Ellipse tool."""
        draw = self._get_draw()
        rgb_color = ImageColor.getrgb(color)
        draw.ellipse([(x0, y0), (x1, y1)], outline=rgb_color, width=5)

    @tool(description="Draw a rectangle outline with specified corners")
    def draw_rectangle(
        self,
        x0: Annotated[float, "Top-left X coordinate (0-200)"],
        y0: Annotated[float, "Top-left Y coordinate (0-200)"],
        x1: Annotated[float, "Bottom-right X coordinate (0-200)"],
        y1: Annotated[float, "Bottom-right Y coordinate (0-200)"],
        color: Annotated[LINE_COLORS, "Line color of the rectangle"],
    ):
        """Rectangle tool."""
        draw = self._get_draw()
        rgb_color = ImageColor.getrgb(color)
        draw.rectangle([(x0, y0), (x1, y1)], outline=rgb_color, width=5)

    @tool(description="Draw a triangle outline using three vertex points")
    def draw_triangle(
        self,
        x0: Annotated[float, "First vertex X coordinate (0-200)"],
        y0: Annotated[float, "First vertex Y coordinate (0-200)"],
        x1: Annotated[float, "Second vertex X coordinate (0-200)"],
        y1: Annotated[float, "Second vertex Y coordinate (0-200)"],
        x2: Annotated[float, "Third vertex X coordinate (0-200)"],
        y2: Annotated[float, "Third vertex Y coordinate (0-200)"],
        color: Annotated[LINE_COLORS, "Line color of the triangle"],
    ):
        """Triangle tool."""
        draw = self._get_draw()
        rgb_color = ImageColor.getrgb(color)
        draw.polygon([(x0, y0), (x1, y1), (x2, y2)], outline=rgb_color, width=5)

    @tool(description="Draw text at a specified position on the canvas")
    def draw_text(
        self,
        x: Annotated[float, "X coordinate for text position (0-200)"],
        y: Annotated[float, "Y coordinate for text position (0-200)"],
        text: Annotated[str, "Text content to draw"],
        color: Annotated[LINE_COLORS, "Line color of the text"],
    ):
        """Draw text at the specified position with the given color."""
        draw = self._get_draw()
        rgb_color = ImageColor.getrgb(color)
        draw.text(xy=(x, y), text=text, fill=rgb_color)

    def save_images(self):
        """Saves the completed PNG and animated GIF images."""
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.im.save(
            f"line_drawer_{timestamp}.gif",
            save_all=True,
            append_images=self.images[1:],
            optimize=False,
            duration=200,
            loop=0,
        )

        self.images[-1].save(f"line_drawer_{timestamp}.png", "PNG")


def run_line_drawing_workflow(line_drawing_request: str, model_id: str = None):
    """Creates and runs the line drawing agent, and saves the result."""

    if model_id is None:
        model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

    print(f"Using model {model_id}")

    line_drawer = LineDrawer()

    agent = Agent(
        model=model_id,
        tools=[
            line_drawer.draw_arc,
            line_drawer.draw_line,
            line_drawer.draw_rectangle,
            line_drawer.draw_ellipse,
            line_drawer.draw_triangle,
            line_drawer.draw_text,
        ],
        system_prompt=(
            "You are a drawing assistant. You have a 200x200 canvas to work with. Your line width is 5. "
            "You must complete the drawing in 30 steps or less. "
            "You do not draw offensive images. "
            "You cannot fix mistakes."
        ),
        tool_executor=SequentialToolExecutor(),  # we want to be sure we draw each step one at a time.
    )

    agent(line_drawing_request)

    line_drawer.save_images()

    print(json.dumps(agent.messages, indent=4))
