from typing import List


def pretty_list(lst: List[str]) -> str:
    if not lst:
        return "Empty"

    if len(lst) == 1:
        return lst[0]

    return f'{", ".join(lst[:-1])} and {lst[-1]}'
