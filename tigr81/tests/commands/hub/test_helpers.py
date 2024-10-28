import pytest
import typer

from tigr81.commands.hub.helpers import (
    get_template_from_hubs,
    is_hub_name_valid,
    load_hubs,
)

"""
Unit tests for load_hubs
"""


def test_load_hubs_no_hubs(mock_hub_folders):
    """Test load hubs with no hubs to load."""
    hubs = load_hubs(mock_hub_folders)
    assert len(hubs) == 0


def test_load_hubs_fake_hubs(mocker, mock_hub_folders):
    """Test load hubs with fake hubs."""
    hub_file = mock_hub_folders[0] / "empty.yml"
    hub_file.touch()

    mock_hub = mocker.Mock()
    mock_hub.name = "Hub1"

    mocker.patch("tigr81.commands.hub.models.Hub.from_yaml", return_value=mock_hub)

    hubs = load_hubs(mock_hub_folders)
    assert isinstance(hubs, dict)
    assert "Hub1" in hubs
    assert len(hubs) == 1


"""
Unit tests for is_hub_name_valid
"""


def mock_load_hubs(mocker, mock_hub_data):
    """Mock load hubs."""
    return mocker.patch(
        "tigr81.commands.hub.helpers.load_hubs", return_value=mock_hub_data
    )


def test_is_hub_name_valid_with_valid_hub_name(mocker, mock_hub_folders, mock_hub_data):
    """Test with a hub name that exists in the loaded hubs."""
    mock_load_hubs(mocker, mock_hub_data)
    hub_name = "valid_hub_1"
    assert not is_hub_name_valid(hub_name, mock_hub_folders)


def test_is_hub_name_valid_with_invalid_hub_name(
    mocker, mock_hub_folders, mock_hub_data
):
    """Test with a hub name that does not exist in the loaded hubs."""
    mock_load_hubs(mocker, mock_hub_data)
    hub_name = "invalid_hub"
    assert is_hub_name_valid(hub_name, mock_hub_folders)


def test_is_hub_name_valid_with_empty_hubs(mocker, mock_hub_folders):
    """Test with an empty hubs dictionary from load_hubs."""
    mock_load_hubs(mocker, {})
    hub_name = "any_hub_name"
    assert is_hub_name_valid(hub_name, mock_hub_folders)


"""
Unit tests for get_template_from_hubs
"""

def test_get_template_from_hubs_no_hubs():
    """Test get template from hubs with no hubs available."""
    with pytest.raises(typer.Exit):
        get_template_from_hubs(
            hub_name="pippo",
            template_name="pluto",
            hubs={}
        )