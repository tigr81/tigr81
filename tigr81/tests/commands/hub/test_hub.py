from pytest_mock import MockerFixture
from typer.testing import CliRunner

from tigr81.main import app

runner = CliRunner()


def test_hub_add(mocker: MockerFixture):
    """Test hub add command."""
    mock_hub = mocker.Mock()
    mock_hub.name = "hub1"
    mocker.patch("tigr81.commands.hub.models.Hub.prompt", return_value=mock_hub)
    mocker.patch("tigr81.commands.hub.hub.is_hub_name_valid", return_value=False)

    result = runner.invoke(app, ["hub", "add"])

    assert result.exit_code == 1


def test_hub_list_all(mocker: MockerFixture):
    """Test hub list command without hub name."""
    mock_hub = mocker.Mock()
    mock_hub.name = "hub1"
    mock_hubs = {
        "hub1": mock_hub
    }
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value=mock_hubs)

    result = runner.invoke(app, ["hub", "list"])

    assert result.exit_code == 0


def test_hub_wrong_hub(mocker: MockerFixture):
    """Test hub list command."""
    mock_hub = mocker.Mock()
    mock_hub.name = "hub1"
    mock_hubs = {
        "hub1": mock_hub
    }
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value=mock_hubs)
    result = runner.invoke(app, ["hub", "list", "hub2"])
    assert result.exit_code == 0


def test_hub_good_hub(mocker: MockerFixture):
    """Test hub list command."""
    mock_hub = mocker.Mock()
    mock_hub.name = "hub1"
    mock_hubs = {
        "hub1": mock_hub
    }
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value=mock_hubs)
    result = runner.invoke(app, ["hub", "list", "hub1"])
    assert result.exit_code == 0


def test_hub_remove_no_hubs(mocker: MockerFixture):
    """Test hub remove command with no hubs."""
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value={})

    result = runner.invoke(app, ["hub", "remove"])

    assert result.exit_code == 0


def test_hub_remove_wrong_hub_name(mocker: MockerFixture):
    """Test hub remove command."""
    mock_hub = mocker.Mock()
    mock_hub.name = "hub1"
    mock_hubs = {
        "hub1": mock_hub
    }
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value=mock_hubs)

    result = runner.invoke(app, ["hub", "remove", "hub2"])

    assert result.exit_code == 0   