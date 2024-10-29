import pathlib as pl
import shutil
import subprocess
from typing import Tuple

import typer


def get_latest_tag(repo_url: str) -> str:
    """Fetches the latest tag from a remote Git repository.

    Args:
        repo_url (str): The URL of the remote Git repository.

    Returns:
        str: The latest tag in semantic version order, or "0.0.0" if no tags are found.

    This function uses `git ls-remote --tags` to list all tags in the specified remote
    repository, then extracts and sorts them according to semantic versioning.
    Annotated tags (those ending with '^{}') are ignored.
    """
    try:
        # Fetch tags from the remote repository
        result = subprocess.run(
            ["git", "ls-remote", "--tags", repo_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Extract and filter tag names, ignoring annotated tags (those with '^{}' suffix)
        tags = [
            line.split("refs/tags/")[-1]
            for line in result.stdout.splitlines()
            if "refs/tags/" in line and not line.endswith("^{}")
        ]

        # Sort tags by semantic version order
        tags.sort(key=lambda s: list(map(int, s.split("."))))

        # Return the latest tag or "0.0.0" if no tags are found
        latest_tag = tags[-1] if tags else "0.0.0"
        typer.echo(f"Latest Tag: {latest_tag}")
        return latest_tag

    except subprocess.CalledProcessError as e:
        typer.echo(f"Error fetching tags: {e.stderr}", err=True)
        return "0.0.0"


def get_author_info() -> Tuple[str, str]:
    """Retrieves the author's name and email from the Git configuration.

    Returns:
        Tuple[str, str]: A tuple containing the author's name and email.
    """
    # Get the author's email from Git config
    author_email = subprocess.run(
        ["git", "config", "user.email"], capture_output=True, text=True, check=True
    ).stdout.strip()

    # Extract the author's name from the email
    author_name = author_email.split("@")[0]

    return author_name, author_email


def clone_repo_directory(
    repo_url: str, checkout: str, directory: pl.Path, output_dir: pl.Path
) -> None:
    """Clones a specific directory from the repository using sparse checkout. If the directory is ".", it clones the entire repository."""
    output_dir_str = str(output_dir)
    checkout = checkout or "main"
    if output_dir_str == ".":
        output_dir = pl.Path(pl.Path(repo_url).name.replace(".git", ""))
        output_dir_str = str(output_dir)

    # Clone the repository without checking out files
    subprocess.run(
        ["git", "clone", "--no-checkout", repo_url, output_dir_str], check=True
    )

    # If directory is not ".", use sparse checkout
    if str(directory) != ".":
        sparse_checkout_path = output_dir / ".git" / "info" / "sparse-checkout"
        sparse_checkout_path.write_text(f"{directory}\n")

        subprocess.run(
            ["git", "-C", output_dir_str, "config", "core.sparseCheckout", "true"],
            check=True,
        )

    # Checkout the specified branch
    subprocess.run(["git", "-C", output_dir_str, "checkout", checkout], check=True)

    git_dir = output_dir / ".git"
    assert git_dir.exists() or git_dir.is_dir()
    shutil.rmtree(git_dir)
