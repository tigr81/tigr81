"""
Handle hub templates.
    - Configure you hub template (also private hub templates)
    - Scaffold a project template from hub templates
    - Add hub templates (public, private, local)
    - Update hub templates properties
    - Delete hub templates
"""

import pathlib as pl

import typer
from cookiecutter.main import cookiecutter
from cookiecutter.repository import repository_has_cookiecutter_json
from typing_extensions import Annotated

import tigr81.commands.core.gitw as gitw
import tigr81.utils as tigr81_utils
from tigr81 import DEFAULT_HUB_LOCATION, USER_HUB_LOCATION
from tigr81.commands.hub.helpers import (
    get_template_from_hubs,
    is_hub_name_valid,
    load_hubs,
)
from tigr81.commands.hub.models import Hub

app = typer.Typer()

default_hub = Hub.from_yaml(path=DEFAULT_HUB_LOCATION)


@app.callback()
def callback():
    """Handle hub templates."""


@app.command()
def add():
    """Add a new hub templates"""
    hub = Hub.prompt()

    if not is_hub_name_valid(hub.name):
        typer.echo(
            f"The hub name {hub.name} is not valid. Already present hub with this name."
        )
        raise typer.Exit()
    hub.to_yaml(USER_HUB_LOCATION)


@app.command()
def list(
    hub_name: Annotated[
        str, typer.Argument(help="The name of the hub to list")
    ] = "all",
):
    """List all hub templates"""
    hubs = load_hubs()
    if hub_name == "all":
        typer.echo("Your hub templates are:")
        for hub_name in hubs:
            typer.echo(hub_name)
        return

    if hub_name not in hubs:
        typer.echo(f"The hub name {hub_name} does not exist")
        raise typer.Exit()

    typer.echo(f"Info about hub {hub_name}")
    typer.echo(hubs[hub_name])


@app.command()
def remove(
    hub_name: Annotated[str, typer.Argument(help="The name of the hub to delete")],
):
    """Remove a hub templates"""
    hubs = load_hubs([USER_HUB_LOCATION])

    if hub_name not in hubs:
        typer.echo(f"The hub name {hub_name} does not exist")
        raise typer.Exit()

    hub_path = USER_HUB_LOCATION / f"{hub_name}.yml"
    typer.echo(f"Deleting hub {hub_name}...")
    hub_path.unlink()
    typer.echo(f"Hub {hub_name} deleted successfully")


@app.command()
def update():
    """Update a hub templates"""
    pass


@app.command()
def scaffold(
    hub_name: Annotated[
        str,
        typer.Argument(
            help="The name of the hub in which there is the template to scaffold."
        ),
    ] = None,
    template_name: Annotated[
        str, typer.Argument(help="The name of the template to scaffold.")
    ] = None,
    output_dir: pl.Path = typer.Option(
        pl.Path("."),
        help="Set if you want to scaffold the project template in a specific directory",
    ),
):
    """Scaffold a template from an existing hub templates"""
    hubs = load_hubs()

    if not hub_name:
        hub_name = tigr81_utils.create_interactive_prompt(
            values=[_name for _name in hubs.keys()],
            message="Select the hub from which to scaffold the template",
            display_transform=lambda hub: hub.replace("_", " ")
            .replace("-", " ")
            .title(),
        )

    selected_hub = hubs.get(hub_name)
    if not selected_hub:
        typer.echo(f"Hub '{hub_name}' not found.")
        raise typer.Exit(code=1)

    if not template_name:
        template_name = tigr81_utils.create_interactive_prompt(
            values=[_name for _name in selected_hub.hub_templates.keys()],
            message=f"Select a template from the hub '{hub_name}'",
            display_transform=lambda template: template.replace("_", " ")
            .replace("-", " ")
            .title(),
        )

    hub_template = selected_hub.hub_templates.get(template_name)
    if not hub_template:
        typer.echo(f"Template '{template_name}' not found in hub '{hub_name}'.")
        raise typer.Exit(code=1)

    hub_template = get_template_from_hubs(
        hub_name=hub_name, template_name=template_name, hubs=hubs
    )

    if repository_has_cookiecutter_json(hub_template.template):
        cookiecutter(
            template=hub_template.template,
            output_dir=output_dir,
            no_input=False,
            checkout=hub_template.checkout,
            directory=hub_template.directory,
        )
    else:
        gitw.scaffold_git_repo(
            repo_url=hub_template.template,
            dest_folder=output_dir,
            folder_path=hub_template.directory,
            checkout=hub_template.checkout,
        )
