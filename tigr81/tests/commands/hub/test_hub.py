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


def test_hub_remove_deletes_existing_hub(tmp_path: pl.Path, mocker: MockerFixture):
    """Removing a hub by name deletes its YAML file."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    hub = Hub(
        name="hub1",
        hub_templates={
            "t1": HubTemplate(
                name="t1",
                template="https://example.com/t1",
                template_type=TemplateTypeEnum.COOKIECUTTER,
            )
        },
    )
    hub.to_yaml(tmp_path)

    result = runner.invoke(app, ["hub", "remove", "hub1"])

    assert result.exit_code == 0
    assert not (tmp_path / "hub1.yml").exists()
    assert "Hub 'hub1' deleted successfully." in result.stdout


def test_hub_remove_template_deletes_existing_template(
    tmp_path: pl.Path, mocker: MockerFixture, mock_hub_template: HubTemplate
):
    """Second positional argument removes that template and keeps the hub file."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    keep = HubTemplate(
        name="keep",
        template="https://example.com/keep",
        template_type=TemplateTypeEnum.COPIER,
    )
    hub = Hub(
        name="hub1",
        hub_templates={
            mock_hub_template.name: mock_hub_template,
            keep.name: keep,
        },
    )
    hub.to_yaml(tmp_path)

    result = runner.invoke(
        app, ["hub", "remove", "hub1", mock_hub_template.name]
    )

    assert result.exit_code == 0
    saved = Hub.from_yaml(tmp_path / "hub1.yml")
    assert mock_hub_template.name not in saved.hub_templates
    assert keep.name in saved.hub_templates
    assert (
        f"Hub template '{mock_hub_template.name}' deleted successfully."
        in result.stdout
    )


def test_hub_remove_template_interactive(
    tmp_path: pl.Path, mocker: MockerFixture, mock_hub_template: HubTemplate
):
    """--template / -t opens the interactive template picker (no second argument)."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    keep = HubTemplate(
        name="keep",
        template="https://example.com/keep",
        template_type=TemplateTypeEnum.COPIER,
    )
    hub = Hub(
        name="hub1",
        hub_templates={
            mock_hub_template.name: mock_hub_template,
            keep.name: keep,
        },
    )
    hub.to_yaml(tmp_path)
    mocker.patch(
        "tigr81.commands.hub.hub.tigr81_utils.create_interactive_prompt",
        return_value=mock_hub_template.name,
    )

    result = runner.invoke(app, ["hub", "remove", "hub1", "--template"])

    assert result.exit_code == 0
    saved = Hub.from_yaml(tmp_path / "hub1.yml")
    assert mock_hub_template.name not in saved.hub_templates
    assert keep.name in saved.hub_templates


def test_hub_remove_template_nonexistent_name(
    tmp_path: pl.Path, mocker: MockerFixture, mock_hub_template: HubTemplate
):
    """Unknown template name as second argument fails; hub YAML is unchanged."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    hub = Hub(
        name="hub1",
        hub_templates={mock_hub_template.name: mock_hub_template},
    )
    hub.to_yaml(tmp_path)

    result = runner.invoke(app, ["hub", "remove", "hub1", "no_such_template"])

    assert result.exit_code == 1
    assert "does not exist" in result.stdout
    saved = Hub.from_yaml(tmp_path / "hub1.yml")
    assert mock_hub_template.name in saved.hub_templates


def test_hub_remove_template_positional_and_flag_mutually_exclusive(
    tmp_path: pl.Path, mocker: MockerFixture, mock_hub_template: HubTemplate
):
    """Passing both a template name and --template is rejected."""
    mocker.patch("tigr81.commands.hub.hub.USER_HUB_LOCATION", tmp_path)
    hub = Hub(
        name="hub1",
        hub_templates={mock_hub_template.name: mock_hub_template},
    )
    hub.to_yaml(tmp_path)

    result = runner.invoke(
        app, ["hub", "remove", "hub1", mock_hub_template.name, "--template"]
    )

    assert result.exit_code == 1
    assert "not both" in result.stdout


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