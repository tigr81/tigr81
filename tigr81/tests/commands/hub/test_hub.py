import pathlib as pl

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from tigr81.commands.hub.models import Hub, HubTemplate, TemplateTypeEnum
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


def test_hub_add_cli_creates_hub(tmp_path: pl.Path, mocker: MockerFixture):
    """Non-interactive add creates a new hub YAML when the hub name is unknown."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value={})

    result = runner.invoke(
        app,
        [
            "hub",
            "add",
            "newhub",
            "mytpl",
            "--template",
            "https://github.com/foo/bar",
            "--type",
            "cookiecutter",
            "--checkout",
            "develop",
        ],
    )

    assert result.exit_code == 0
    saved = Hub.from_yaml(tmp_path / "newhub.yml")
    assert saved.name == "newhub"
    assert "mytpl" in saved.hub_templates
    tpl = saved.hub_templates["mytpl"]
    assert tpl.template == "https://github.com/foo/bar"
    assert tpl.template_type == TemplateTypeEnum.COOKIECUTTER
    assert tpl.checkout == "develop"
    assert tpl.directory == "."


def test_hub_add_cli_appends_to_existing_hub(
    tmp_path: pl.Path, mocker: MockerFixture
):
    """Non-interactive add merges into an existing hub definition."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    existing = Hub(
        name="hub1",
        hub_templates={
            "old": HubTemplate(
                name="old",
                template="https://example.com/old",
                template_type=TemplateTypeEnum.COOKIECUTTER,
                checkout="main",
                directory=".",
            )
        },
    )
    mocker.patch(
        "tigr81.commands.hub.hub.load_hubs", return_value={"hub1": existing}
    )

    result = runner.invoke(
        app,
        [
            "hub",
            "add",
            "hub1",
            "newtpl",
            "-t",
            "https://github.com/org/copier-tpl",
            "--type",
            "copier",
        ],
    )

    assert result.exit_code == 0
    saved = Hub.from_yaml(tmp_path / "hub1.yml")
    assert set(saved.hub_templates) == {"old", "newtpl"}
    assert saved.hub_templates["newtpl"].template_type == TemplateTypeEnum.COPIER


def test_hub_add_cli_incomplete(mocker: MockerFixture):
    """Mixing hub + template name without --type is rejected."""
    mocker.patch("tigr81.commands.hub.hub.load_hubs", return_value={})

    result = runner.invoke(
        app,
        [
            "hub",
            "add",
            "hub1",
            "tpl",
            "--template",
            "https://github.com/x/y",
        ],
    )

    assert result.exit_code == 1


def test_hub_add_cli_duplicate_template_name(
    tmp_path: pl.Path, mocker: MockerFixture
):
    """Adding a template name that already exists in the hub fails."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    existing = Hub(
        name="hub1",
        hub_templates={
            "dup": HubTemplate(
                name="dup",
                template="https://a",
                template_type=TemplateTypeEnum.RAW_GIT,
            )
        },
    )
    mocker.patch(
        "tigr81.commands.hub.hub.load_hubs", return_value={"hub1": existing}
    )

    result = runner.invoke(
        app,
        [
            "hub",
            "add",
            "hub1",
            "dup",
            "--template",
            "https://github.com/b/other",
            "--type",
            "raw_git",
        ],
    )

    assert result.exit_code == 1