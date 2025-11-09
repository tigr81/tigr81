import tigr81.utils as tigr81_utils
from tigr81.commands.scaffold.project_template import (
    ICON_MAPPING,
    ProjectTypeEnum,
)


def select_project_type_interactive() -> ProjectTypeEnum:
    """Prompt user to select a project type interactively using the utility function."""
    return tigr81_utils.create_interactive_prompt(
        values=list(ProjectTypeEnum),
        icon_mapping=ICON_MAPPING,
        message="Select the project type to scaffold",
    )
