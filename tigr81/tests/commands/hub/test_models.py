from pytest_mock import MockerFixture

from tigr81.commands.hub.models import Hub, HubTemplate, TemplateTypeEnum

"""
Unit tests for HubTemplate.prompt
"""


def test_hub_template_prompt(mocker: MockerFixture):
    """Test hub template prompt."""
    mocker.patch(
        "tigr81.utils.create_interactive_prompt",
        return_value=TemplateTypeEnum.COOKIECUTTER,
    )
    mock_prompt = mocker.patch("typer.prompt")
    template = "http://example.com/example-template.git"
    template_name = "example-template"
    checkout = "main"
    directory = "subfolder"
    mock_prompt.side_effect = [
        template,
        template_name,
        checkout,
        directory,
    ]
    mocker.patch("tigr81.utils.extract_template_name", return_value="example-template")

    hub_template = HubTemplate.prompt()

    assert hub_template.template_type == TemplateTypeEnum.COOKIECUTTER
    assert hub_template.template == template
    assert hub_template.name == template_name
    assert hub_template.checkout == checkout
    assert hub_template.directory == directory


def test_hub_template_str(mock_hub_template: HubTemplate):
    """Test HubTemplate __str__ method."""
    expected_output = (
        "\tTemplate type: cookiecutter\n"
        "\tTemplate name: example-template\n"
        "\tTemplate location: http://example.com/template-repo.git\n"
        "\tCheckout: main\n"
        "\tDirectory: subfolder\n"
    )
    assert str(mock_hub_template) == expected_output


"""
Unit tests for Hub.prompt
"""

def test_hub_prompt(mocker: MockerFixture, mock_hub_template: HubTemplate):
    """Test Hub.prompt method."""
    mocker.patch("typer.prompt", return_value="hub1")
    mock_confirm = mocker.patch("typer.confirm")
    mock_confirm.side_effect = [
        True,
        False,
    ]
    mocker.patch("tigr81.commands.hub.models.HubTemplate.prompt", return_value=mock_hub_template)

    hub = Hub.prompt()

    assert hub.name == "hub1"
    assert hub.hub_templates[mock_hub_template.name] == mock_hub_template
