import pytest
import yaml

import tigr81.utils as tigr81_utils


def test_read_yaml_valid_file(tmp_path):
    """Create a temporary YAML file with some content."""
    yaml_content = {"key1": "value1", "key2": 2, "key3": [1, 2, 3]}
    file_path = tmp_path / "test_valid.yaml"
    with open(file_path, "w") as f:
        yaml.dump(yaml_content, f)

    # Test that the function reads the YAML file correctly
    result = tigr81_utils.read_yaml(str(file_path))
    assert result == yaml_content, "The function should correctly parse a valid YAML file."


def test_read_yaml_empty_file(tmp_path):
    """Create an empty YAML file."""
    file_path = tmp_path / "test_empty.yaml"
    file_path.touch()  # Create an empty file

    # Test that the function returns an empty dictionary for an empty file
    result = tigr81_utils.read_yaml(str(file_path))
    assert result == {}, "The function should return an empty dictionary for an empty file."


def test_read_yaml_nonexistent_file():
    """Test that the function raises an exception for a non-existent file."""
    with pytest.raises(FileNotFoundError):
        tigr81_utils.read_yaml("nonexistent_file.yaml")
