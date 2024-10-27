from typing import Optional

from pydantic_settings import BaseSettings


class CliSettings(BaseSettings):
    tigr81_environment: Optional[str] = None


CLI_SETTINGS = CliSettings()
