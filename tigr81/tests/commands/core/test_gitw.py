import subprocess

from pytest_mock import MockerFixture

from tigr81.commands.core.gitw import get_latest_tag, get_author_info

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