import pathlib as pl
from typing import Dict, Optional, Union

import typer
import yaml
from pydantic import BaseModel

import tigr81.utils as tigr81_utils


class TemplateTypeEnum(tigr81_utils.StrEnum):
    """Enumeration for different types of templates."""
    COOKIECUTTER = "cookiecutter"
    COPIER = "copier"
    RAW_GIT = "raw_git"


class HubTemplate(BaseModel):
    """Represents a template in the hub, with details about its name, location, version control, and type.

    Attributes:
        name (str): The name of the template.
        template (Union[str, pl.Path]): Path or URL location of the template.
        checkout (Optional[str]): Specific version or branch if it's a remote template.
        directory (Optional[str]): Path within the repository if it's a remote template.
        template_type (TemplateTypeEnum): The type of the template, such as cookiecutter or copier.
    """

    name: str
    template: Union[str, pl.Path]
    checkout: Optional[str] = None
    directory: Optional[str] = None
    template_type: TemplateTypeEnum

    def __str__(self):
        """String representation of the HubTemplate instance, listing the template type, name, location, and optional checkout and directory details.

        Returns:
            str: Formatted string detailing the template information.
        """
        components = [
            f"\tTemplate type: {self.template_type}",
            f"\tTemplate name: {self.name}",
            f"\tTemplate location: {self.template}",
        ]
        if self.checkout:
            components.append(f"\tCheckout: {self.checkout}")
        if self.directory:
            components.append(f"\tDirectory: {self.directory}\n")
        return "\n".join(components)

    @staticmethod
    def prompt() -> "HubTemplate":
        """Interactive prompt to gather details for creating a new HubTemplate instance.

        Returns:
            HubTemplate: A HubTemplate instance based on user input.
        """
        template_type = tigr81_utils.create_interactive_prompt(
            values=list(TemplateTypeEnum),
            message="Select a template type",
        )
        template = typer.prompt("Enter the template location (git repo, local)")

        hub_template_name = tigr81_utils.extract_template_name(template)
        hub_template_name = typer.prompt(
            "Enter the template name", default=hub_template_name
        )

        template_pl = pl.Path(template)
        checkout = None
        directory = None
        if not template_pl.exists() or not template_pl.is_dir():
            checkout = typer.prompt(
                "Enter the checkout (only needed for remote template)",
                default="main",
            )
            directory = typer.prompt(
                "Enter the relative path to a template in a repository (only needed for remote template)",
                default=pl.Path("."),
            )

        return HubTemplate(
            name=hub_template_name,
            template=template,
            checkout=checkout,
            directory=directory,
            template_type=template_type,
        )


class Hub(BaseModel):
    """Represents a hub, which is a collection of templates, and includes functionality to serialize and deserialize from YAML format.

    Attributes:
        name (str): The name of the hub.
        hub_templates (Dict[str, HubTemplate]): A dictionary of templates within the hub,
            where keys are template names.
    """

    name: str
    hub_templates: Dict[str, HubTemplate]

    def to_yaml(self, folder_path: pl.Path) -> None:
        """Serializes the Hub instance to a YAML file at the specified folder path.

        Args:
            folder_path (pl.Path): The directory where the YAML file should be saved.
        """
        path = folder_path / f"{self.name}.yml"
        with open(path, "w") as f:
            yaml.dump(
                data=self.model_dump(mode="json"),
                stream=f,
            )

    @staticmethod
    def from_yaml(path: pl.Path) -> "Hub":
        """Loads a Hub instance from a YAML file.

        Args:
            path (pl.Path): Path to the YAML file.

        Returns:
            Hub: A Hub instance with data loaded from the file.
        """
        hub_dct = tigr81_utils.read_yaml(path)
        return Hub(**hub_dct)

    @staticmethod
    def prompt() -> "Hub":
        """Interactive prompt to create a new Hub instance, allowing the user to add templates.

        Returns:
            Hub: A Hub instance based on user input.
        """
        hub_name = typer.prompt("Enter the hub name", default="my-hub")

        hub_templates = {}

        while typer.confirm("Do you want to add a template? (y/n)", default=True):
            hub_template = HubTemplate.prompt()
            hub_templates[hub_template.name] = hub_template

        return Hub(name=hub_name, hub_templates=hub_templates)
    
    def __str__(self):
        """String representation of the Hub instance, listing hub name and templates.

        Returns:
            str: Formatted string detailing hub information.
        """
        hub_templates_str = "".join([f"{ht}" for ht in self.hub_templates.values()])
        return f"""Hub info
hub name: {self.name}
hub templates:\n\n{hub_templates_str}
"""
