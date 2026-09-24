"""To-do tool schema example"""

from strands import tool

import agent_testing_utils


@tool(
    description="Adds, updates, or deletes a to-do list",
    inputSchema={
        "json": {
            "properties": {
                "to_do_list_attributes": {  # Nested object
                    "type": "object",
                    "description": "Attributes about the to-do list and what kind of action to take",
                    "properties": {
                        "to_do_list_name": {"type": "string", "description": "The name of the to-do list"},
                        "to_do_list_action": {
                            "type": "string",
                            "description": "The action to take on the to-do list",
                            "enum": ["create", "update", "delete"],
                        },
                    },
                },
                "to_do_list_items": {
                    "type": "array",
                    "description": "The list of to-do items",
                    "items": {
                        "type": "object",
                        "description": "The to-do list item",
                        "properties": {
                            "to_do_item_title": {
                                "type": "string",
                                "description": "The title of the to-do item",
                            },
                            "to_do_item_details": {
                                "type": "string",
                                "description": "Details about the to-do item",
                            },
                        },
                        "required": ["to_do_item_title"],
                    },
                },
            },
            "required": ["to_do_list_attributes"],
        }
    },
)
def to_do_list_editor(to_do_list_attributes, to_do_list_items) -> str:
    """To-do list editor tool"""

    # Some logic here to retrieve or create a list, and save changes to a database.
    _ = (to_do_list_attributes, to_do_list_items)  # do something with these later

    return "List modified successfully!"


agent_testing_utils.display_and_test_decorated_function(
    to_do_list_editor,
    prompt="Create a new to-do list called 'Winter prep'. Add items for calling the plow service and buying a shovel",
)
