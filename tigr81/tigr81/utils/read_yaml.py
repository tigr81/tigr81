from typing import Dict

import yaml


def read_yaml(file_path: str) -> Dict:
    """Reads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file to be read.

    Returns:
        Dict: A dictionary containing the parsed YAML data. If the file is empty
        or an error occurs during reading, returns an empty dictionary.
    """
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)

    return config or {}
