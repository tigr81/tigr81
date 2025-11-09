import pathlib as pl
from typing import Dict, List

import typer

from tigr81 import AVAILABLE_HUBS
from tigr81.commands.hub.models import Hub, HubTemplate


def load_hubs(hub_folders: List[pl.Path] = AVAILABLE_HUBS) -> Dict[str, Hub]:
    """Load hub configurations from specified YAML files in given folders.

    Args:
        hub_folders (List[pl.Path]): A list of paths to directories containing hub YAML files.
                                       Defaults to AVAILABLE_HUBS.

    Returns:
        Dict[str, Hub]: A dictionary mapping hub names to Hub objects.
    """
    hubs = {}
    for hub_folder in hub_folders:
        for hub_path in hub_folder.glob("*.yml"):
            hub = Hub.from_yaml(hub_path)
            hubs[hub.name] = hub
    return hubs


def is_hub_name_valid(
    hub_name: str, hub_folders: List[pl.Path] = AVAILABLE_HUBS
) -> bool:
    """Check if a hub name is valid by determining if it exists in the loaded hubs.

    Args:
        hub_name (str): The name of the hub to check.
        hub_folders (List[pl.Path]): A list of paths to directories containing hub YAML files.
                                       Defaults to AVAILABLE_HUBS.

    Returns:
        bool: True if the hub name is not found in the loaded hubs, False otherwise.
    """
    hubs = load_hubs(hub_folders)
    return hub_name not in hubs


def get_template_from_hubs(
    hub_name: str, template_name: str, hubs: Dict[str, Hub]
) -> HubTemplate:
    """Retrieve a hub template by name from a specified hub.

    Args:
        hub_name (str): The name of the hub from which to retrieve the template.
        template_name (str): The name of the template to retrieve.
        hubs (Dict[str, Hub]): A dictionary of loaded hubs.

    Returns:
        HubTemplate: The requested HubTemplate object.

    Raises:
        typer.Exit: If the hub name or template name is not found, an error message is printed
                     and the program exits.
    """
    hub = hubs.get(hub_name)
    if not hub:
        typer.echo(f"Hub name not found: {hub_name}")
        raise typer.Exit()

    template = hub.hub_templates.get(template_name)

    if not template:
        typer.echo(f"Hub template {template_name} not found in hub {hub_name}")
        raise typer.Exit()

    return template
