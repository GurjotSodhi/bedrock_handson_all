"""Tools for the quiz assistant"""

from typing import Any

from strands import tool

# BEGIN CHALLENGE CONTENT: Create the question_schema JSON schema ------------------------------------------------

choice_schema = {
    "description": "A choice candidate for the question",
    "type": "object",
    "properties": {
        "choice_label": {
            "description": "The label for the choice - assume letter values like A, B, C, D, E unless told otherwise.",
            "type": "string",
        },
        "choice_text": {"description": "The text to be displayed for the choice", "type": "string"},
        "is_correct_answer": {
            "description": "Indicates whether this is the correct answer for the question",
            "type": "boolean",
        },
    },
    "required": ["choice_label", "choice_text", "is_correct_answer"],
}

question_schema = {
    "description": "A single choice question",
    "type": "object",
    "properties": {
        "question_text": {"description": "The main question text to be asked", "type": "string"},
        "explanation": {"description": "Explanation for why the correct answer is right", "type": "string"},
        "choices": {
            "description": "Array of possible answer choices. Only one can be correct.",
            "items": choice_schema,
            "maxItems": 5,
            "minItems": 3,
            "type": "array",
        },
    },
    "required": ["question_text", "explanation", "choices"],
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
