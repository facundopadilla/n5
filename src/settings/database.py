from pydantic import PostgresDsn

from src.settings.base_settings import BaseProjectSettings


class _DatabaseSettings(BaseProjectSettings):
    POSTGRES_DSN: PostgresDsn


DatabaseSettings = _DatabaseSettings()
