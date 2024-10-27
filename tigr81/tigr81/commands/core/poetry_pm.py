import pathlib as pl
import shutil
import subprocess as sp
import sys

import typer


class PoetryPM:
    """A utility class for managing Python dependencies using Poetry.

    This class provides methods to interact with the Poetry package manager.
    It checks for the presence of Poetry, installs components, and removes
    dependencies from a specified working directory.
    """

    def __init__(self):
        self.poetry_executable = shutil.which("poetry")
        if self.poetry_executable:
            result = sp.run(
                [self.poetry_executable, "--version"],
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                check=True,
                text=True,
            )
            poetry_version = result.stdout.strip()
            typer.echo(f"Poetry executable: {self.poetry_executable}")
            typer.echo(f"Poetry version: {poetry_version}")
        else:
            typer.echo("Poetry is not installed or not found on this machine.")
            sys.exit(1)

    def install(self, cwd: pl.Path) -> None:
        try:
            typer.echo(f"Installing component {cwd}...")
            result: sp.CompletedProcess = sp.run(
                [self.poetry_executable, "install"],
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                check=True,
                cwd=cwd,
            )

            typer.echo(result.stdout, color="green")
            typer.echo(result.stderr, color="red")

            if result.returncode != 0:
                typer.echo(
                    "An error occurred while running 'poetry install'.", color="red"
                )
                sys.exit(1)
        except sp.CalledProcessError:
            typer.echo("An error occurred while running 'poetry install'.", color="red")
            sys.exit(1)

    def remove(self, cwd: pl.Path, dependency: str) -> None:
        try:
            typer.echo(f"Removing dependency {dependency} from {cwd}...")
            result: sp.CompletedProcess = sp.run(
                [self.poetry_executable, "remove", dependency],
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                check=True,
                cwd=cwd,
            )

            typer.echo(result.stdout, color="green")
            typer.echo(result.stderr, color="red")

            if result.returncode != 0:
                typer.echo(
                    f"An error occurred while running 'poetry remove {dependency}'.",
                    color="red",
                )
                sys.exit(1)
        except sp.CalledProcessError:
            typer.echo(
                f"An error occurred while running 'poetry remove {dependency}'.",
                color="red",
            )
            sys.exit(1)
