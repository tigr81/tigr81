from pytest_mock import MockerFixture

from tigr81.utils.interactive_prompt import create_interactive_prompt


def test_create_interactive_prompt(mocker: MockerFixture):
    """Test create_interactive_prompt function with mock prompt response."""
    values = ["apple", "banana", "cherry"]
    icon_mapping = {"apple": "🍎", "banana": "🍌"}
    message = "Pick a fruit"
    display_transform = str.upper

    mocker.patch(
        "tigr81.utils.interactive_prompt.prompt",
        return_value={"selection": "banana"},
    )

    result = create_interactive_prompt(
        values=values,
        icon_mapping=icon_mapping,
        message=message,
        display_transform=display_transform,
    )

    assert result == "banana"
