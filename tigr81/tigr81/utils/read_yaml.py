from typing import Dict

import yaml


def read_yaml(file_path: str) -> Dict:
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)

    return config or {}
