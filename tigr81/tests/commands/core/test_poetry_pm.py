import functools
import subprocess

import pytest
import typer
from pytest_mock import MockerFixture

from tigr81.commands.core.poetry_pm import PoetryPM


@pytest.fixture
def mock_poetry_pm(mocker: MockerFixture):
    """Fixture to create a PoetryPM instance with a mocked poetry executable."""
    result = mocker.Mock()
    result.stdout = "Poetry (version 1.3.2)"
    mocker.patch("subprocess.run", return_value=result)
    mocker.patch("shutil.which", return_value="/usr/local/bin/poetry")
    return PoetryPM()


def test_poetry_initialization_success(mocker: MockerFixture):
    """Test PoetryPM initialization success."""
    result = mocker.Mock()
    result.stdout = "Poetry (version 1.3.2)"
    mocker.patch("subprocess.run", return_value=result)
    mocker.patch("shutil.which", return_value="/usr/local/bin/poetry")
    PoetryPM()


def test_poetry_initialization_failure(mocker: MockerFixture):
    """Test poetry PM initialization failure."""
    mocker.patch("shutil.which", return_value=None)
    with pytest.raises(typer.Exit):
        PoetryPM()


@pytest.mark.parametrize(
    "returncode, side_effect, should_raise_exception",
    [
        (0, None, False),  # Success case, no exception
        (1, None, True),  # Failure with return code 1, should raise exception
        (
            1,
            subprocess.CalledProcessError(returncode=1, cmd=""),
            True,
        ),  # Failure due to exception
    ],
)
def test_poetry_command(
    mocker: MockerFixture,
    mock_poetry_pm: PoetryPM,
    returncode,
    side_effect,
    should_raise_exception,
):
    """Test poetry PM install and remove with different return codes and exceptions."""
    result = mocker.Mock()
    result.returncode = returncode

    mock_run = mocker.patch("subprocess.run", return_value=result)
    if side_effect:
        mock_run.side_effect = side_effect

    # Test both `install` and `remove` commands
    for command in [
        mock_poetry_pm.install,
        functools.partial(mock_poetry_pm.remove, dependency=""),
    ]:
        if should_raise_exception:
            with pytest.raises(typer.Exit):
                command(".")
        else:
            command(".")
