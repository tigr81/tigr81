import pytest

from tigr81.commands.hub.models import HubTemplate, TemplateTypeEnum


@pytest.fixture
def mock_hub_folders(tmp_path):
    """Mock for hub folders."""
    _num_dirs = 3

    _tmp_dirs = [tmp_path / f"tmp_dir_{i}" for i in range(_num_dirs)]

    for _directory in _tmp_dirs:
        _directory.mkdir()

    return _tmp_dirs

@pytest.fixture
def mock_hub_data():
    """Mock data returned by load_hubs."""
    return {
        "valid_hub_1": "Hub1 Details",
        "valid_hub_2": "Hub2 Details",
    }

@pytest.fixture
def mock_hub_template():
    """Mock HubTemplate."""
    return HubTemplate(
        name="example-template",
        template="http://example.com/template-repo.git",
        checkout="main",
        directory="subfolder",
        template_type=TemplateTypeEnum.COOKIECUTTER,
    )