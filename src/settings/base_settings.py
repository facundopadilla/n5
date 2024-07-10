from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env.local"), case_sensitive=True, extra="ignore"
    )
