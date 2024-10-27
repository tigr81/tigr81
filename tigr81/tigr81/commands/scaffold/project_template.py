import pathlib as pl
from typing import Dict, List, Optional

import click
import typer
from pydantic import BaseModel, ConfigDict, EmailStr

import tigr81.utils as tigr81_utils
from tigr81 import ORGANIZATION_LOCATION

PROJECT_TEMPLATE_DEFAULT_RELATIVE_PATH = pl.Path(".")


class ProjectTypeEnum(tigr81_utils.StrEnum):
    FAST_API = "fastapi"
    POETRY_PKG = "poetry_pkg"
    PRIME_REACT = "prime-react"

    @property
    def project_location(self):
        return f"{ORGANIZATION_LOCATION}/{self}"

    @staticmethod
    def get_monorepo_types() -> List["ProjectTypeEnum"]:
        return [ProjectTypeEnum.FAST_API, ProjectTypeEnum.POETRY_PKG]


ICON_MAPPING = {
    ProjectTypeEnum.FAST_API: "🌐",
    ProjectTypeEnum.POETRY_PKG: "📦",
    ProjectTypeEnum.PRIME_REACT: "⚛️ ",
}


class ProjectTemplateOptions(BaseModel):
    name: Optional[str] = None
    package_name: Optional[str] = None
    description: Optional[str] = None
    author_name: Optional[str] = "name surname"
    author_email: Optional[EmailStr] = "email@gmail.com"

    @classmethod
    def prompt(cls) -> "ProjectTemplateOptions":
        name = typer.prompt("Enter the project name", default="myproject")
        package_name = typer.prompt(
            "Enter the package name for the project", default="myproject"
        )
        description = typer.prompt(
            "Enter a description for the project",
            default="A description for the project",
        )
        author_name = typer.prompt(
            "Enter the author name for the project", default="name surname"
        )
        author_email = typer.prompt(
            "Enter the author email for the project", default="email@gmail.com"
        )

        return ProjectTemplateOptions(
            name=name,
            package_name=package_name,
            description=description,
            author_name=author_name,
            author_email=author_email,
        )


class Dependency(BaseModel):
    name: str
    relative_path: Optional[pl.Path] = pl.Path(".")

    @classmethod
    def prompt(cls, available_dependencies: List["ProjectTemplate"]):
        names = [pt.project_options.name for pt in available_dependencies]
        name = typer.prompt("Enter the dependency name", type=click.Choice(names))

        selected_project_template = None
        for pt in available_dependencies:
            if pt.project_options.name == name:
                selected_project_template = pt

        if selected_project_template is None:
            raise ValueError("Invalid selected dependency..")

        # relative_path = typer.prompt("Enter the relative path of the dependency", default=pl.Path("."))

        relative_path = (
            pl.Path("../")
            / selected_project_template.relative_path
            / selected_project_template.project_options.name
        )

        return Dependency(
            name=name,
            relative_path=relative_path,
        )


class ProjectTemplate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    project_type: ProjectTypeEnum
    relative_path: Optional[pl.Path] = PROJECT_TEMPLATE_DEFAULT_RELATIVE_PATH
    project_options: ProjectTemplateOptions
    dependencies: Optional[List[Dependency]] = []

    @property
    def project_type_as_enum(self) -> ProjectTypeEnum:
        return ProjectTypeEnum(self.project_type)

    @property
    def extra_content(self) -> Dict:
        extra_content = self.project_options.model_dump(mode="json", exclude_none=True)

        extra_content["dependencies"] = {
            dependency.name: dependency.model_dump(mode="json")
            for dependency in self.dependencies
        }

        return extra_content

    @classmethod
    def prompt(
        cls, available_dependencies: List["ProjectTemplate"] = None
    ) -> "ProjectTemplate":
        project_type = typer.prompt(
            "Enter the project template type for the component you want to add",
            type=click.Choice(ProjectTypeEnum.get_monorepo_types()),
        )

        relative_path = typer.prompt(
            "Enter the relative path of the component you want to add",
            default=PROJECT_TEMPLATE_DEFAULT_RELATIVE_PATH,
        )

        project_options = ProjectTemplateOptions.prompt()

        dependencies = []
        if available_dependencies:
            while typer.confirm(
                "Do you want to add a dependency for this component? (y/n)",
                default=True,
            ):
                dependencies.append(
                    Dependency.prompt(available_dependencies=available_dependencies)
                )

        return ProjectTemplate(
            project_type=project_type,
            relative_path=relative_path,
            project_options=project_options,
            dependencies=dependencies,
        )


if __name__ == "__main__":
    pt = ProjectTemplate.prompt()
