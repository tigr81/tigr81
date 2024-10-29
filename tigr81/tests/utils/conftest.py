import pathlib as pl
import tempfile

import pytest


@pytest.fixture
def temp_local_path():
    """Creates a temporary directory as a mock local path."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_path = pl.Path(tmpdirname)
        temp_file = tmp_path / "my-template"
        temp_file.touch()
        yield str(temp_file)
