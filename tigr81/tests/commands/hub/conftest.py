import pytest


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