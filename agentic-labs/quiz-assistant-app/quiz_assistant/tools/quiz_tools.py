"""Tools for the quiz assistant"""

from typing import Any

from strands import tool

# BEGIN CHALLENGE CONTENT: Create the question_schema JSON schema ------------------------------------------------

question_schema = {
    # define values for "description", "type", "properties", and "required" here.
}

# END CHALLENGE CONTENT --------------------------------------------------------------------------------

quiz_schema = {
    "description": "Represents the contents of a quiz",
    "type": "object",
    "properties": {
        "quiz_title": {"description": "The title of the quiz", "type": "string"},
        "questions": {
            "description": "A collection of single choice questions in the quiz",
            "items": question_schema,
            "type": "array",
        },
    },
    "required": ["quiz_title", "questions"],
}


@tool(description="Creates a quiz", inputSchema={"json": quiz_schema})
def create_quiz(quiz_title: str, questions: Any) -> dict:
    """Tool for capturing the generated quiz"""

    _ = (quiz_title, questions)
    # You could choose to save this working quiz record somewhere

    return {
        "status": "success",
        "content": [{"json": {"quiz_title": quiz_title, "questions": questions}}],
    }
