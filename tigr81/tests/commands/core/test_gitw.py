import pathlib as pl
import subprocess

from pytest_mock import MockerFixture

from tigr81.commands.core.gitw import (
    clone_repo_directory,
    get_author_info,
    get_latest_tag,
)

"""
Unit tests for get_latest_tag
"""

def test_get_latest_tag_with_tagged_repo(mocker: MockerFixture):
    """Test get_latest_tag function with a tagged repo."""
    result = mocker.Mock()
    result.stdout.splitlines = lambda: [
        "d62d84456a68d6359c5c8e5504a1611724cfa4fd        refs/tags/0.0.1",
        "8976f04faad06c0b437cae48669af82990365e55        refs/tags/0.0.2",
    ]
    mocker.patch("subprocess.run", return_value=result)
    latest_tag = get_latest_tag("https://some-repo.gitw")
    assert latest_tag == "0.0.2"


def test_get_latest_tag_with_error(mocker: MockerFixture):
    """Test get_latest_tag function when subprocess.run raises CalledProcessError."""
    # Simulate a CalledProcessError with return code and stderr message
    mocker.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd="git ls-remote --tags",
            stderr="Remote repository not found",
        ),
    )
    latest_tag = get_latest_tag("https://invalid-repo.gitw")
    assert latest_tag == "0.0.0"


"""
Unit tests for get_author_info
"""

def test_get_author_info(mocker: MockerFixture):
    """Test get_author_info."""
    result = mocker.Mock()
    result.stdout = "giuambro@gmail.com"
    mocker.patch("subprocess.run", return_value=result)
    author_name, author_email = get_author_info()
    assert (author_name, author_email) == ("giuambro", "giuambro@gmail.com")


"""
Unit tests for clone_repo_directory
"""

def test_clone_directory_entire_repo(mocker: MockerFixture, mock_repo_url, mock_folders):
    """Test clone_directory for an entire repo."""
    checkout = ""
    directory = pl.Path(".")
    output_dir = mock_folders[0]

    git_dir = output_dir / ".git"
    git_dir.mkdir()

    mock_spr = mocker.patch("subprocess.run")
    clone_repo_directory(
        repo_url=mock_repo_url,
        checkout=checkout,
        directory=directory,
        output_dir=output_dir
    )
    mock_spr.assert_any_call(
        ["git", "clone", "--no-checkout", mock_repo_url, str(output_dir)], check=True
    )
    mock_spr.assert_any_call(
        ["git", "-C", str(output_dir), "checkout", "main"], check=True
    )



def test_clone_directory_sub_repo(mocker: MockerFixture, mock_repo_url, mock_folders):
    """Test clone_directory for a folder of a repo."""
    checkout = ""
    directory = mock_folders[0]
    output_dir = mock_folders[1]

    git_dir = output_dir / ".git"
    git_dir.mkdir()

    sparse_checkout_file = git_dir / "info" / "sparse-checkout"
    sparse_checkout_file.parent.mkdir(parents=True, exist_ok=True)
    sparse_checkout_file.touch()
    
    mock_spr = mocker.patch("subprocess.run")
    clone_repo_directory(
        repo_url=mock_repo_url,
        checkout=checkout,
        directory=directory,
        output_dir=output_dir
    )
    mock_spr.assert_any_call(
        ["git", "clone", "--no-checkout", mock_repo_url, str(output_dir)], check=True
    )
    mock_spr.assert_any_call(
        ["git", "-C", str(output_dir), "config", "core.sparseCheckout", "true"], check=True
    )
    mock_spr.assert_any_call(
        ["git", "-C", str(output_dir), "checkout", "main"], check=True
    )