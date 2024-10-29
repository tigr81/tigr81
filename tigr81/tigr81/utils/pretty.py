from typing import List


def pretty_list(lst: List[str]) -> str:
    """Convert a list of strings into a human-readable format.

    This function takes a list of strings and formats it in a way that 
    is easy to read. The output will vary depending on the number of 
    items in the list:
    
    - If the list is empty, it returns "Empty".
    - If the list contains one item, it returns that item as a string.
    - If the list contains two or more items, it joins all items 
      with a comma, using "and" before the last item.

    Args:
        lst (List[str]): A list of strings to be formatted.

    Returns:
        str: A formatted string representation of the list. If the 
        list is empty, returns "Empty".
    """
    if not lst:
        return "Empty"

    if len(lst) == 1:
        return lst[0]

    return f'{", ".join(lst[:-1])} and {lst[-1]}'
