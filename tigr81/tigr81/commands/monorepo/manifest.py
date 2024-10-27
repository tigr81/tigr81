import pathlib as pl
import shutil
from typing import List, Optional

import typer
import yaml
from graphviz import Digraph
from pydantic import BaseModel

import tigr81.utils as tigr81_utils
from tigr81.commands.core.poetry_pm import PoetryPM
from tigr81.commands.monorepo.constants import (
    MANIFEST_DEFAULT_DESCRIPTION,
    MANIFEST_DEFAULT_NAME,
    MANIFEST_DEFAULT_RELATIVE_PATH,
    MANIFEST_FILE_NAME,
)
from tigr81.commands.scaffold.project_template import ProjectTemplate, ProjectTypeEnum


class Manifest(BaseModel):
    name: Optional[str] = MANIFEST_DEFAULT_NAME
    relative_path: Optional[pl.Path] = MANIFEST_DEFAULT_RELATIVE_PATH
    description: Optional[str] = MANIFEST_DEFAULT_DESCRIPTION
    components: Optional[List[ProjectTemplate]] = []

    def remove(self, component_name: str) -> ProjectTemplate:
        component_to_remove = None
        # find the component to delete
        for component in self.components:
            if component.project_options.name == component_name:
                component_to_remove = component
                break

        if not component_to_remove:
            raise ValueError(
                f"Component with name '{component_name}' not found in the manifest."
            )

        # find the component in which the component_name is installed
        components_to_update = []
        for component in self.components:
            for dependency in component.dependencies:
                if dependency.name == component_name:
                    components_to_update.append(component.project_options.name)

        if len(components_to_update) == 0:
            continue_flg = True
        else:
            continue_flg = typer.confirm(
                f"""By removing the component {component_name} you will remove it also from the components: {tigr81_utils.pretty_list(components_to_update)}\nDo you want to continue?"""
            )
        if continue_flg:
            if components_to_update:
                pc = PoetryPM()
                for component in self.components:
                    for dependency in component.dependencies:
                        if dependency.name == component_name:
                            cwd = (
                                self.relative_path
                                / component.relative_path
                                / component.project_options.name
                            )
                            pc.remove(cwd, component_name)

            typer.echo(
                f"Removing component {component_name} from manifest components.."
            )
            self.components.remove(component_to_remove)

            typer.echo("Deleting component folder file..")
            shutil.rmtree(
                self.relative_path
                / component_to_remove.relative_path
                / component_to_remove.project_options.name
            )
            typer.echo(f"Component {component_name} removed successfully")
            return component_to_remove

    @classmethod
    def prompt(cls) -> "Manifest":
        name = typer.prompt(
            "Enter a name for the monorepo project", default=MANIFEST_DEFAULT_NAME
        )
        relative_path = typer.prompt(
            "Enter the relative path for the monorepo project, the folder in which the monorepo source code will be located:",
            default=MANIFEST_DEFAULT_RELATIVE_PATH,
        )
        description = typer.prompt(
            "Enter a description for the monorepo project",
            default=MANIFEST_DEFAULT_DESCRIPTION,
        )

        components = []
        while typer.confirm("Do you want to add a component? (y/n)", default=True):
            components.append(ProjectTemplate.prompt(available_dependencies=components))

        return Manifest(
            name=name,
            relative_path=relative_path,
            description=description,
            components=components,
        )

    def to_graphviz_digraph(self) -> Digraph:
        dg = Digraph(name=self.name, filename=self.name, format="png")

        for component in self.components:
            fillcolor = "white"
            if component.project_type == ProjectTypeEnum.FAST_API:
                fillcolor = "slateblue1"

            name = component.project_options.name
            label = f"{component.project_options.name}\n\n{component.project_options.description}"

            dg.node(
                name=name, label=label, shape="box", style="filled", fillcolor=fillcolor
            )

            for dependency in component.dependencies:
                dg.edge(tail_name=dependency.name, head_name=name)

        return dg

    def to_yaml(self, file_name: str = MANIFEST_FILE_NAME) -> None:
        with open(file_name, "w") as f:
            yaml.dump(
                data=self.model_dump(mode="json"),
                stream=f,
                default_flow_style=False,
                sort_keys=False,
            )
