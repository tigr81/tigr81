from tigr81.commands.scaffold.project_template import ProjectTypeEnum

def test_enum_str():
    assert str(ProjectTypeEnum.FAST_API) == "fastapi"

def test_enum_repr():
    assert repr(ProjectTypeEnum.FAST_API) == "fastapi"

def test_enum_members():
    assert ProjectTypeEnum.FAST_API in ProjectTypeEnum
