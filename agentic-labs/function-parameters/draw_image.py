"""Tool with basic types"""

import time
from typing import Annotated, List, Literal

from PIL import Image, ImageDraw, ImageColor
from strands import tool

import agent_testing_utils


@tool(description="Draws an image with a multi-segment line and text")
def draw_image_with_line_and_text(
    xy: Annotated[List[float], "List of x,y coordinates defining the line path"],
    line_width: Annotated[int, "Width of the line in pixels"],
    line_color: Annotated[Literal["red", "green", "blue", "yellow", "orange", "purple"], "Color of the line"],
    text: Annotated[str, "The text to draw in the image"],
    text_x: Annotated[float, "The x coordinate of the text"],
    text_y: Annotated[float, "The y coordinate of the text"],
    dark_mode: Annotated[bool, "Whether the image should have a dark background."],
):
    """The image drawing tool"""

    background_color = (0, 0, 0) if dark_mode else (255, 255, 255)

    im = Image.new("RGB", (200, 200), background_color)
    draw = ImageDraw.Draw(im)
    color = ImageColor.getrgb(line_color)

    draw.line(xy=xy, fill=color, width=line_width)

    text_color = (255, 255, 255) if dark_mode else 0

    draw.text(xy=(text_x, text_y), text=text, fill=text_color)

    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")

    im.save(f"line_drawing_{timestamp}.png", "PNG")


agent_testing_utils.display_and_test_decorated_function(
    draw_image_with_line_and_text,
    system_prompt="You are a drawing assistant. You have a 200x200 canvas to work with. You can only use the tool one time.",
    prompt="Draw a haunted castle.",
)
