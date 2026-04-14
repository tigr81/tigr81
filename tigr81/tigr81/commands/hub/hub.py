"""Handle hub templates.

- Configure you hub template (also private hub templates)
- Scaffold a project template from hub templates
- Add hub templates (public, private, local) or a template to an existing hub
- Update hub templates properties
- Delete hub templates
"""

import pathlib as pl
from typing import Optional, Tuple

import copier
import typer
from cookiecutter.main import cookiecutter
from typing_extensions import Annotated

import tigr81.commands.core.gitw as gitw
import tigr81.utils as tigr81_utils
from tigr81 import DEFAULT_HUB_LOCATION, USER_HUB_LOCATION
from tigr81.commands.hub.helpers import (
    get_template_from_hubs,
    is_hub_name_valid,
    load_hubs,
)
from tigr81.commands.hub.models import Hub, HubTemplate, TemplateTypeEnum

app = typer.Typer()

default_hub = Hub.from_yaml(path=DEFAULT_HUB_LOCATION)


def _resolve_checkout_directory(
    template: str,
    checkout: Optional[str],
    directory: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    """Match HubTemplate.prompt defaults: local dirs skip checkout/directory."""
    template_pl = pl.Path(template)
    if template_pl.exists() and template_pl.is_dir():
        return None, None
    resolved_checkout = checkout if checkout is not None else "main"
    resolved_directory = directory if directory is not None else "."
    return resolved_checkout, resolved_directory


def _add_template_cli(
    hub_name: str,
    template_name: str,
    template: str,
    template_type: TemplateTypeEnum,
    checkout: Optional[str],
    directory: Optional[str],
) -> None:
    """Add one template from CLI flags; create the hub YAML under ~/.tigr81rc if needed."""
    hubs = load_hubs()
    selected_hub = hubs.get(hub_name)
    if selected_hub is None:
        selected_hub = Hub(name=hub_name, hub_templates={})
    elif template_name in selected_hub.hub_templates:
        typer.echo(
            f"Template '{template_name}' already exists in hub '{hub_name}'."
        )
        raise typer.Exit(1)

    co, di = _resolve_checkout_directory(template, checkout, directory)
    hub_template = HubTemplate(
        name=template_name,
        template=template,
        checkout=co,
        directory=di,
        template_type=template_type,
    )
    selected_hub.hub_templates[template_name] = hub_template
    selected_hub.to_yaml(USER_HUB_LOCATION)
    typer.echo(
        f"Template '{template_name}' added to hub '{hub_name}' (saved under {USER_HUB_LOCATION})."
    )


def _interactive_add_to_hub(hub_name: str) -> None:
    """Prompt-driven: append templates to a hub that already exists in config."""
    hubs = load_hubs()
    if len(hubs) == 0:
        typer.echo(
            "No hubs were found. To create a hub with a template in one step, use:\n"
            "  tigr81 hub add HUB_NAME TEMPLATE_NAME --template URL --type cookiecutter|copier|raw_git"
        )
        raise typer.Exit(1)

    selected_hub = hubs.get(hub_name)
    if not selected_hub:
        typer.echo(f"The hub name '{hub_name}' does not exist.")
        raise typer.Exit(1)

    typer.echo(f"Adding templates to hub '{hub_name}'...")
    added_any = False
    while typer.confirm("Do you want to add a template?", default=True):
        hub_template = HubTemplate.prompt()
        if hub_template.name in selected_hub.hub_templates:
            typer.echo(
                f"Template '{hub_template.name}' already exists in hub '{hub_name}'."
            )
            raise typer.Exit(1)
        selected_hub.hub_templates[hub_template.name] = hub_template
        added_any = True
        typer.echo(f"Template '{hub_template.name}' added to hub '{hub_name}'.")

    if not added_any:
        typer.echo("No templates added.")
        return

    selected_hub.to_yaml(USER_HUB_LOCATION)
    typer.echo(f"Hub '{hub_name}' saved successfully.")


@app.callback()
def callback():
    """Handle hub templates."""


@app.command()
def add(
    hub_name: Annotated[
        Optional[str],
        typer.Argument(
            help="Hub to add the template to (created under user config if it does not exist)"
        ),
    ] = None,
    template_name: Annotated[
        Optional[str],
        typer.Argument(
            help="Name for the template entry (required with --template and --type)"
        ),
    ] = None,
    template: Annotated[
        Optional[str],
        typer.Option(
            "--template",
            "-t",
            help="Git URL or local path to the template",
        ),
    ] = None,
    template_type: Annotated[
        Optional[TemplateTypeEnum],
        typer.Option(
            "--type",
            help="Template backend: cookiecutter, copier, or raw_git",
            case_sensitive=False,
        ),
    ] = None,
    checkout: Annotated[
        Optional[str],
        typer.Option(
            "--checkout",
            "-c",
            help="Branch, tag, or commit for remote templates (default: main)",
        ),
    ] = None,
    directory: Annotated[
        Optional[str],
        typer.Option(
            "--directory",
            "-d",
            help="Path inside the repo for remote templates (default: .)",
        ),
    ] = None,
):
    """Add a new hub, or add template(s) to a hub.

    Non-interactive (single command): pass HUB_NAME, TEMPLATE_NAME, --template, and --type.
    Example: tigr81 hub add my-hub my-template -t https://github.com/org/cookiecutter-py --type cookiecutter -c main

    Interactive: run ``tigr81 hub add`` to create a hub, or ``tigr81 hub add HUB_NAME`` to add templates with prompts.
    """
    if (
        hub_name is not None
        and template_name is not None
        and template is not None
        and template_type is not None
    ):
        _add_template_cli(
            hub_name=hub_name,
            template_name=template_name,
            template=template,
            template_type=template_type,
            checkout=checkout,
            directory=directory,
        )
        return

    cli_partial = any(
        x is not None
        for x in (template_name, template, template_type, checkout, directory)
    )
    if hub_name is not None and cli_partial:
        typer.echo(
            "Incomplete non-interactive add: provide HUB_NAME, TEMPLATE_NAME, "
            "--template (-t), and --type together, or omit template options "
            "and use interactive mode (only HUB_NAME)."
        )
        raise typer.Exit(1)

    if hub_name is not None:
        _interactive_add_to_hub(hub_name)
        return

    hub = Hub.prompt()

    if not is_hub_name_valid(hub.name):
        typer.echo(
            f"The hub name {hub.name} is not valid. Already present hub with this name."
        )
        raise typer.Exit(1)
    hub.to_yaml(USER_HUB_LOCATION)


@app.command()
def list(  # noqa: A001
    hub_name: Annotated[
        str, typer.Argument(help="The name of the hub to list")
    ] = "all",
):
    """List all hub templates."""
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
    hub_name: Annotated[
        Optional[str], typer.Argument(help="The name of the hub")
    ] = None,
    template_name: Annotated[
        Optional[str],
        typer.Argument(
            help=(
                "Template to remove from the hub. If omitted, the whole hub is removed "
                "unless you pass --template to pick a template interactively."
            ),
        ),
    ] = None,
    interactive_template: Annotated[
        bool,
        typer.Option(
            "--template",
            "-t",
            help=(
                "Remove one template from the hub via an interactive prompt "
                "(non-script use). To delete a specific template by name, use: "
                "hub remove HUB TEMPLATE"
            ),
        ),
    ] = False,
):
    """Remove a hub, or remove one template from a hub."""
    hubs = load_hubs([USER_HUB_LOCATION])

    if len(hubs) == 0:
        typer.echo("No hubs were found..")
        raise typer.Exit()

    if hub_name is None:
        hub_name = tigr81_utils.create_interactive_prompt(
            values=[*hubs.keys()],
            message="Select a hub",
        )

    if hub_name not in hubs:
        typer.echo(f"The hub name '{hub_name}' does not exist.")
        raise typer.Exit()

    selected_hub = hubs.get(hub_name)

    delete_one_template = template_name is not None or interactive_template

    if delete_one_template:
        if template_name is not None and interactive_template:
            typer.echo(
                "Use either `hub remove HUB TEMPLATE` or `hub remove HUB --template`, "
                "not both."
            )
            raise typer.Exit(code=1)

        if len(selected_hub.hub_templates) == 0:
            typer.echo(f"The hub '{hub_name}' does not contain any hub templates.")
            raise typer.Exit()

        if template_name is not None:
            hub_template_name_to_delete = template_name
        else:
            hub_template_name_to_delete = tigr81_utils.create_interactive_prompt(
                values=[*selected_hub.hub_templates.keys()],
                message=f"Select a template from the hub '{hub_name}' to delete",  # noqa: S608
            )

        if hub_template_name_to_delete not in selected_hub.hub_templates:
            typer.echo(
                f"The hub template '{hub_template_name_to_delete}' does not exist "
                f"in hub '{hub_name}'."
            )
            raise typer.Exit(code=1)

        typer.echo(f"Deleting hub template '{hub_template_name_to_delete}'...")
        selected_hub.hub_templates.pop(hub_template_name_to_delete)

        selected_hub.to_yaml(USER_HUB_LOCATION)
        typer.echo(
            f"Hub template '{hub_template_name_to_delete}' deleted successfully."
        )
    else:
        hub_path = USER_HUB_LOCATION / f"{hub_name}.yml"
        typer.echo(f"Deleting hub '{hub_name}'...")
        hub_path.unlink()
        typer.echo(f"Hub '{hub_name}' deleted successfully.")


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
    default: bool = typer.Option(
        default=False, help="Set to False to enable input during cookiecutter execution"
    ),
):
    """Scaffold a template from an existing hub templates."""
    hubs = load_hubs()

    if not hub_name:
        hub_name = tigr81_utils.create_interactive_prompt(
            values=[*hubs.keys()],
            message="Select the hub from which to scaffold the template",
        )

    selected_hub = hubs.get(hub_name)
    if not selected_hub:
        typer.echo(f"Hub '{hub_name}' not found.")
        raise typer.Exit(code=1)

    if not template_name:
        template_name = tigr81_utils.create_interactive_prompt(
            values=[*selected_hub.hub_templates.keys()],
            message=f"Select a template from the hub '{hub_name}'",  # noqa: S608
        )

    hub_template = selected_hub.hub_templates.get(template_name)
    if not hub_template:
        typer.echo(f"Template '{template_name}' not found in hub '{hub_name}'.")
        raise typer.Exit(code=1)

    hub_template = get_template_from_hubs(
        hub_name=hub_name, template_name=template_name, hubs=hubs
    )
    _template_type = hub_template.template_type
    typer.echo(f"Scaffolding template type: {_template_type}")
    if _template_type == TemplateTypeEnum.COOKIECUTTER:
        cookiecutter(
            template=hub_template.template,
            output_dir=output_dir,
            no_input=default,
            checkout=hub_template.checkout,
            directory=hub_template.directory,
        )
    elif _template_type == TemplateTypeEnum.RAW_GIT:
        gitw.clone_repo_directory(
            repo_url=hub_template.template,
            output_dir=output_dir,
            directory=hub_template.directory,
            checkout=hub_template.checkout,
        )
    elif _template_type == TemplateTypeEnum.COPIER:
        copier.run_copy(
            src_path=hub_template.template,
            dst_path=output_dir,
            vcs_ref=hub_template.checkout,
            defaults=default,
        )
    else:
        raise ValueError("Unknown template type")
