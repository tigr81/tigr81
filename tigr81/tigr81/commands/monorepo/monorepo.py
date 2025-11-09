import pathlib as pl
import shutil
from typing import Dict, List

import click
import typer
from pydantic import BaseModel

import tigr81.commands.core.scaffold as scaffold_core
import tigr81.utils as tigr81_utils
from tigr81.commands.core.poetry_pm import PoetryPM
from tigr81.commands.monorepo.constants import MANIFEST_FILE_NAME
from tigr81.commands.monorepo.manifest import Manifest
from tigr81.commands.scaffold.project_template import ProjectTemplate

app = typer.Typer()


@app.callback()
def callback():
    """Handle monorepo project."""


@app.command()
def add():
    """Add a component to the monorepo project."""
    typer.echo("Adding a component to the monorepo project")

    manifest_dct = tigr81_utils.read_yaml(MANIFEST_FILE_NAME)
    manifest = Manifest(**manifest_dct)

    component = ProjectTemplate.prompt(available_dependencies=manifest.components)

    manifest.components.append(component)

    manifest.to_yaml(MANIFEST_FILE_NAME)

    typer.echo(
        "In order to scaffold also the component you need to run 'tigr81 monorepo scaffold'"
    )


@app.command()
def draw():
    """Generate the .png representation of the monorepo pkd dependencies."""
    manifest_dct = tigr81_utils.read_yaml(MANIFEST_FILE_NAME)
    manifest = Manifest(**manifest_dct)
    mf_digraph = manifest.to_graphviz_digraph()
    typer.echo("Rendering the manifest...")
    mf_digraph.render()


@app.command()
def clean():
    """Delete all resources related to the current monorepo."""
    typer.echo("Cleaning monorepo project")
    manifest_dct = tigr81_utils.read_yaml(MANIFEST_FILE_NAME)
    manifest = Manifest(**manifest_dct)

    confirmed = typer.confirm(
        f"Are you sure you want to delete all the resources related to the monorepo: {manifest.name}"
    )

    if not confirmed:
        typer.echo("Cleaning stopped..")
        return

    typer.echo(
        f"Deleting all resources related to monorepo related to the monorepo: {manifest.name}.."
    )
    if manifest.relative_path.exists():
        typer.echo("Deleting source code..")
        shutil.rmtree(manifest.relative_path)

    manifest_png = pl.Path(f"{manifest.name}.png")
    if manifest_png.exists():
        typer.echo(f"Deleting {manifest_png}..")
        manifest_png.unlink()

    manifest = pl.Path(manifest.name)

    if manifest.exists():
        typer.echo(f"Deleting {manifest}..")
        manifest.unlink()

    typer.echo(
        f"Deleted all resources related to monorepo related to the monorepo: {manifest.name}.."
    )


@app.command()
def init():
    """Initialize a monorepo project."""
    typer.echo("Inizializing a monorepo project")

    manifest_path = pl.Path(MANIFEST_FILE_NAME)

    if manifest_path.exists():
        overwrite = typer.confirm(
            "The manifest file already exists, do you want to overwrite?"
        )
        if not overwrite:
            typer.echo("Manifest file not overwritten!!")
            return

    manifest = Manifest.prompt()
    typer.echo("Creating manifest file...")
    manifest.to_yaml()


@app.command()
def install():
    """Install every component inside the monorepo project."""
    typer.echo("Installing all the components of the monorepo project")

    pc = PoetryPM()

    manifest_dct = tigr81_utils.read_yaml(MANIFEST_FILE_NAME)

    manifest = Manifest(**manifest_dct)

    for component in manifest.components:
        pc.install(
            cwd=manifest.relative_path
            / component.relative_path
            / component.project_options.name
        )


@app.command()
def remove():
    """Remove a component from the monorepo project."""
    manifest_dct = tigr81_utils.read_yaml(MANIFEST_FILE_NAME)

    manifest = Manifest(**manifest_dct)

    names = [pt.project_options.name for pt in manifest.components]
    name = typer.prompt(
        "Enter the name of the component you want to delete", type=click.Choice(names)
    )

    typer.echo(f"Removing the component {name} to the monorepo project")
    manifest.remove(component_name=name)

    mf_digraph = manifest.to_graphviz_digraph()
    typer.echo("Rendering the manifest...")
    mf_digraph.render()
    manifest.to_yaml()


@app.command()
def scaffold():
    """Scaffold a monorepo project."""
    # TODO: check if the file exists and add a method from_yaml in Manifest
    try:
        manifest_dct = tigr81_utils.read_yaml(MANIFEST_FILE_NAME)
    except FileNotFoundError:
        typer.echo(
            "Manifest not found.. make sure you are in the correct folder or if you want to create a new one run: tigr81 monorepo init"
        )
        raise typer.Exit() from None

    manifest = Manifest(**manifest_dct)

    typer.echo(
        f"Scaffolding a monorepo project from manifest located at {pl.Path.cwd() / MANIFEST_FILE_NAME}"
    )

    for component in manifest.components:
        component_location = (
            manifest.relative_path
            / component.relative_path
            / component.project_options.name
        )
        typer.echo(f"Scaffolding {component_location} component...")
        if not component_location.exists():
            scaffold_core.scaffold_project_template(
                project_template=component,
                default=True,
                output_dir=manifest.relative_path / component.relative_path,
            )
            typer.echo(f"Component {component_location} scaffolded successfully")
        else:
            typer.echo(f"Component {component.project_options.name} already exists..")

    typer.echo("Monorepo scaffolding completed successfully")

    # FIX: fix monorepo graph visualization
    # mf_digraph = manifest.to_graphviz_digraph()

    # typer.echo("Rendering the manifest...")
    # mf_digraph.render()


# Define a function to interactively prompt the user for input for a Pydantic BaseModel
def prompt_for_model(model_type: BaseModel) -> BaseModel:
    """Interactively prompt the user for input to create a Pydantic BaseModel instance.

    Args:
        model_type: The BaseModel class to instantiate.

    Returns:
        A new instance of the model_type created from user input.
    """
    input_data = {}
    for field_name, field_info in model_type.model_fields.items():
        if issubclass(field_info, BaseModel):
            input_data[field_name] = prompt_for_model(field_info)
        elif issubclass(field_info, List):
            inner_type = field_info.__args__[0]
            input_data[field_name] = []
            while True:
                item = prompt_for_model(inner_type)
                input_data[field_name].append(item)
                if typer.confirm("Add another item? (y/n)", default=True):
                    continue
                break
        elif issubclass(field_info, Dict):
            key_type, value_type = field_info.__args__
            input_data[field_name] = {}
            while True:
                key = prompt_for_model(key_type)
                value = prompt_for_model(value_type)
                input_data[field_name][key] = value
                if typer.confirm("Add another item? (y/n)", default=True):
                    continue
                break
        else:
            default_value = (
                field_info.default if hasattr(field_info, "default") else None
            )
            user_input = typer.prompt(
                f"Enter value for {field_name} (default is {default_value}): ",
                default=default_value,
            )
            input_data[field_name] = user_input
    return model_type(**input_data)
