from typing import Any, Dict, List, Optional

from InquirerPy import prompt


def create_interactive_prompt(
    values: List[Any],
    icon_mapping: Optional[Dict[Any, str]] = None,
    message: str = "Select an option",
    display_transform: callable = lambda x: x,
) -> Any:
    """Utility function to prompt the user to select a value interactively.

    Parameters:
        values (List[Any]): List of values to present as options.
        icon_mapping (Optional[Dict[Any, str]]): Mapping of values to their icons. If None, no icons are displayed.
        message (str): The message to display in the prompt.
        display_transform (callable): A function to transform the display of values.

    Returns:
        Any: The selected value from the list.
    """
    # Build choices with icons (if provided) or just names
    choices = [
        {
            "name": f"{icon_mapping.get(value, '') + ' ' if icon_mapping and value in icon_mapping else ''}{display_transform(value)}",
            "value": value,
        }
        for value in values
    ]

    # Define the question structure for InquirerPy
    questions = [
        {
            "type": "list",
            "name": "selection",
            "message": message,
            "choices": choices,
        }
    ]

    # Prompt the user and return their choice
    answers = prompt(questions)
    return answers["selection"]
