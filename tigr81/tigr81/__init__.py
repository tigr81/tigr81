import pathlib as pl

PACKAGE_LOCATION = pl.Path(__file__).parent.resolve()
ROOT_LOCATION = PACKAGE_LOCATION.parent
LOCAL_REPO_LOCATION = ROOT_LOCATION.parent

LOCAL_PROJECT_TEMPLATES_FOLDER_LOCATION = LOCAL_REPO_LOCATION / "project_templates"
RESOURCE_LOCATION = PACKAGE_LOCATION / "resources"
HUBS_LOCATION = RESOURCE_LOCATION / "hubs"
DEFAULT_HUB_LOCATION = HUBS_LOCATION / "tigr81_hub_templates.yml"

USER_CONFIG_LOCATION = pl.Path.home() / ".tigr81rc"
USER_CONFIG_LOCATION.mkdir(exist_ok=True)
USER_HUB_LOCATION = USER_CONFIG_LOCATION / "hubs"
USER_HUB_LOCATION.mkdir(exist_ok=True)

AVAILABLE_HUBS = [HUBS_LOCATION, USER_HUB_LOCATION]

PYPY_URL = "https://pypi.org/project/tigr81/"
REPO_LOCATION = "https://github.com/tigr81/tigr81.git"
ORGANIZATION_LOCATION = "https://github.com/tigr81"
