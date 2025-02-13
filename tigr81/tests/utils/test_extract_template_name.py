import pytest

import tigr81.utils as tigr81_utils


@pytest.mark.parametrize(
    "template, expected",
    [
        # URLs with various structures
        ("https://github.com/user/my-repo.git", "my-repo"),
        ("https://github.com/user/my-repo/", "my-repo"),
        ("https://bitbucket.org/user/my-repo.git/", "my-repo"),
        ("https://example.com/user/project_repo", "project_repo"),
        # Edge case: URL with unusual structure
        ("https://github.com/user/repo.name.git", "reponame"),
        ("https://github.com/user/.hidden-repo.git", "hidden-repo"),
    ],
)
def test_extract_template_name_given_url(template, expected):
    """Test that extract_template_name returns the correct name for various types of URLs."""
    assert tigr81_utils.extract_template_name(template) == expected


def test_extract_template_name_path(tmp_path):
    """Test that extract_template_name returns the correct name for an existing directory."""
    tmp_dir = tmp_path / "test"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    assert tigr81_utils.extract_template_name(str(tmp_dir)) == "test"


@pytest.mark.parametrize(
    "invalid_template",
    [
        pytest.lazy_fixture("temp_local_path"),
        "/non/existent/path",  # Non-existent local path
        "invalid_url_format",  # Invalid URL format
        "ftp://github.com/user/repo",  # Unsupported URL protocol
        "my-repo.tar.gz",  # only a filename with extension (no directory)
    ],
)
def test_extract_template_name_invalid_path(invalid_template):
    """Test that extract_template_name raises a ValueError for non-existent paths or invalid URLs."""
    with pytest.raises(ValueError):
        tigr81_utils.extract_template_name(invalid_template)
