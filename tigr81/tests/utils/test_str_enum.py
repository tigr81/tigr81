from tigr81.commands.scaffold.project_template import ProjectTypeEnum


def test_enum_str():
    """Test that enum string representation returns the expected value."""
    assert str(ProjectTypeEnum.FAST_API) == "fastapi"


def test_enum_repr():
    """Test that enum repr returns the expected value."""
    assert repr(ProjectTypeEnum.FAST_API) == "fastapi"


def test_enum_members():
    """Test that enum members are properly contained in the enum."""
    assert ProjectTypeEnum.FAST_API in ProjectTypeEnum
