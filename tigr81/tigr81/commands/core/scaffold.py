import pathlib as pl
from typing import List

import typer
from cookiecutter.main import cookiecutter

import tigr81.commands.core.gitw as gitw
from tigr81.commands.scaffold.project_template import (
    ProjectTemplate,
    ProjectTemplateOptions,
    ProjectTypeEnum,
)


def scaffold_project_type(
    project_type: ProjectTypeEnum,
    default: bool = False,
    output_dir: pl.Path = pl.Path("."),
    checkout: str = "main",
):
    author_name, author_email = gitw.get_author_info()

    project_template = ProjectTemplate(
        project_type=project_type,
        project_options=ProjectTemplateOptions(
            author_name=author_name,
            author_email=author_email,
        ),
    )

    scaffold_project_template(
        project_template, default=default, output_dir=output_dir, checkout=checkout
    )


def scaffold_project_template(
    project_template: ProjectTemplate,
    default: bool = False,
    output_dir: pl.Path = pl.Path("."),
    checkout: str = "main",
):
    template = project_template.project_type_as_enum.project_location
    typer.echo(
        f"Scaffolding a {project_template.project_type} project template from {template}"
    )

    author_name, author_email = gitw.get_author_info()

    project_template.project_options.author_name = author_name
    project_template.project_options.author_email = author_email

    cookiecutter(
        template=template,
        output_dir=output_dir,
        no_input=default,
        extra_context=project_template.extra_content,
        checkout=checkout,
        directory=str(project_template.project_type),
    )


def scaffold_cookiecutter(
    project_type: ProjectTypeEnum,
    default: bool = False,
    output_dir: pl.Path = pl.Path("."),
    checkout: str = "main",
):
    template = project_type.project_location
    typer.echo(f"Scaffolding a {project_type} project template from {template}")
    cookiecutter(
        template=template,
        output_dir=output_dir,
        no_input=default,
        checkout=checkout,
        directory=str(project_type),
    )


def scaffold_monorepo(components: List[ProjectTemplate]):
    pass
