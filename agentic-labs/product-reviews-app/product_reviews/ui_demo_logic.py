"""The supporting logic for the streamlit app"""

from product_reviews.agents import product_reviews_agent

MAX_DEPTH = 10


def process_content(review_title: str, review_content: str, stars_rating: int):
    """Handle the client-side request"""

    result = product_reviews_agent.run_agent_workflow(review_content=review_content)

    # eventually do something with this data, like save to a database,
    # or validate if the stars and the review text are in alignment.
    _ = (review_title, review_content, stars_rating)

    return result.model_dump()


def get_presentable_key(key: str):
    if key and isinstance(key, str):
        return key.replace("_", " ").title()
    return ""


def format_as_markdown(content, depth: int = 0) -> str:
    """Renders an object as markdown"""

    if depth > MAX_DEPTH:
        return ""

    sb = []

    indented_prefix = "    " * depth

    if isinstance(content, dict):
        sb.append("")  # break dictionaries as values onto a new line
        for key, value in content.items():
            if isinstance(value, dict | list):
                val_rendered = format_as_markdown(value, depth + 1)
            else:
                val_rendered = str(value)
            sb.append(f"{indented_prefix}* **{get_presentable_key(key)}**: {val_rendered}")
    elif isinstance(content, list):
        sb.append("")  # break lists as values onto a new line
        for i, item in enumerate(content):
            if isinstance(item, dict | list):
                val_rendered = format_as_markdown(item, depth + 1)
            else:
                val_rendered = str(item)

            sb.append(f"{indented_prefix}* **Item {(i + 1)}**: {val_rendered}")
    else:
        return str(content)

    return "\n".join(sb)
