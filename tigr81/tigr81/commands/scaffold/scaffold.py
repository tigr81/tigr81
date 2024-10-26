from typing import Optional
from tigr81.commands.core import gitw
from typing_extensions import Annotated
from cookiecutter.main import cookiecutter
import typer
import pathlib as pl

from tigr81 import LOCAL_REPO_LOCATION, REPO_LOCATION
from tigr81.cli_settings import CLI_SETTINGS
import tigr81.commands.core.scaffold as scaffold_core
from tigr81.commands.scaffold.project_template import (
    Dependency,
    ProjectTemplate,
    ProjectTemplateOptions,
    ProjectTypeEnum,
)
from tigr81.commands.scaffold.select_project_type_interactive import (
    select_project_type_interactive,
)


def scaffold(
    project_type: Annotated[
        ProjectTypeEnum, typer.Argument(help="The project type to scaffold")
    ] = None,
    default: bool = typer.Option(
        False, help="Set to False to enable input during cookiecutter execution"
    ),
    output_dir: pl.Path = typer.Option(
        pl.Path("."),
        help="Set if you want to scaffold the project template in a specific directory",
    ),
    dev: bool = typer.Option(
        False,
        help="Set this flag to use the default local directory based on project type",
    ),
    local_dir: Optional[pl.Path] = typer.Option(
        None, help="Specify a local folder for the template"
    ),
    checkout: str = typer.Option(
        None, help="Specify the branch for non-local scaffolding (default: latest tag)"
    ),
    cookiecutter_url: str = typer.Option(
        None,
        "--cookiecutter-url",
        "--ck-url",
        help="Specify the url or path (for local scaffolding) of a cookiecutter project template",
    ),
    git_url: str = typer.Option(
        None,
        "--git-url",
        help="Specify the url of a git repo you want to scaffold",
    ),
    directory: Optional[pl.Path] = typer.Option(
        None, help="Specify a relative path to a directory (for git_url and cookiecutter_url scaffolding templates)"
    ),
):
    """Scaffold a project template"""

    if cookiecutter_url is not None:
        typer.echo(f"Scaffolding custom cookiecutter: {cookiecutter_url}")
        cookiecutter(
            template=cookiecutter_url,
            output_dir=output_dir,
            directory=directory or ".",
            no_input=default,
            checkout=checkout or "main" ,
        )
        return
    
    if git_url is not None:
        typer.echo(f"Scaffolding clone repo: {cookiecutter_url}")
        gitw.clone_repo_directory(
            repo_url=git_url,
            checkout=checkout or "main",
            directory=directory or pl.Path("."),
            output_dir=output_dir,
        )
        return

    # Prompt the user for project type if not provided
    if not project_type:
        project_type = select_project_type_interactive()

    if dev and local_dir is None:
        local_dir = str(project_type)

    if local_dir is not None:
        typer.echo(f"Scaffolding local: {cookiecutter_url}")
        cookiecutter(
            template=str(local_dir),
            output_dir=output_dir / "scaffolded"
            if str(output_dir) == "."
            else output_dir,
            no_input=default,
        )
        return

    if checkout is None:
        checkout = gitw.get_latest_tag(repo_url=project_type.project_location)

    typer.echo("scaffolding checkout")
    typer.echo(f"Tag: {checkout}")

    if project_type == ProjectTypeEnum.PRIME_REACT:
        scaffold_core.scaffold_cookiecutter(
            project_type=project_type,
            default=default,
            output_dir=output_dir,
            checkout=checkout,
        )
    else:
        scaffold_core.scaffold_project_type(
            project_type=project_type,
            default=default,
            output_dir=output_dir,
            checkout=checkout,
        )


if __name__ == "__main__":
    project_type = "fastapi"
    PROJECT_TEMPLATE_LOCATION = REPO_LOCATION
    checkout = "develop"

    if CLI_SETTINGS.tigr81_environment == "local":
        PROJECT_TEMPLATE_LOCATION = LOCAL_REPO_LOCATION.as_posix()
        checkout = None

    typer.echo(
        f"Scaffolding a {project_type} project template from {PROJECT_TEMPLATE_LOCATION}"
    )

    project_template = ProjectTemplate(
        project_type=project_type,
        project_options=ProjectTemplateOptions(
            name=project_type,
            package_name=project_type,
            description=project_type,
        ),
        dependencies=[
            Dependency(name="dagprep", relative_path="../../dagprep"),
            Dependency(name="fresko", relative_path="../../fresko"),
        ],
    )

    print(project_template.extra_content)

    cookiecutter(
        template=PROJECT_TEMPLATE_LOCATION,
        output_dir=".",
        no_input=True,
        # extra_context=project_template.project_options.model_dump(),
        extra_context=project_template.extra_content,
        checkout=checkout,
        directory=f"project_templates/{project_template.project_type}",
    )
