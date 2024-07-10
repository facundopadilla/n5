from src.settings.base_settings import BaseProjectSettings


class _ProjectSettings(BaseProjectSettings):
    DEBUG: bool = False
    TESTING: bool = False
    VERSION: str = "0.1.0"


ProjectSettings = _ProjectSettings()
