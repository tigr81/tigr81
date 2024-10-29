import pathlib as pl
import shutil
import subprocess as sp

import typer


class PoetryPM:
    """A utility class for managing Python dependencies using Poetry.

    This class provides methods to interact with the Poetry package manager.
    It checks for the presence of Poetry, installs components, and removes
    dependencies from a specified working directory.
    """

    def __init__(self):
        """Initializes the PoetryPM class by checking for the Poetry executable.

        If Poetry is installed, it captures the Poetry version information.
        If Poetry is not found, it will print a message and exit the program.
        """
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
            raise typer.Exit()

    def install(self, cwd: pl.Path) -> None:
        """Installs dependencies in the specified working directory using Poetry.

        Args:
            cwd (pl.Path): The path to the working directory where `poetry install`
                           should be executed.

        This method runs `poetry install` in the specified directory and captures
        both standard output and standard error, displaying any error messages in
        red text. If installation fails, it will print an error message and exit.
        """
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
                raise typer.Exit()
        except sp.CalledProcessError:
            typer.echo("An error occurred while running 'poetry install'.", color="red")
            raise typer.Exit()

    def remove(self, cwd: pl.Path, dependency: str) -> None:
        """Removes a specified dependency from the working directory using Poetry.

        Args:
            cwd (pl.Path): The path to the working directory where `poetry remove`
                           should be executed.
            dependency (str): The name of the dependency to remove.

        This method runs `poetry remove <dependency>` in the specified directory
        and captures both standard output and standard error, displaying error
        messages in red text if they occur. If the removal fails, it will print
        an error message and exit.
        """
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
                raise typer.Exit()
        except sp.CalledProcessError:
            typer.echo(
                f"An error occurred while running 'poetry remove {dependency}'.",
                color="red",
            )
            raise typer.Exit()
