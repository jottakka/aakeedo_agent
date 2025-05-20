from pydantic import HttpUrl, Field
from pydantic_settings  import BaseSettings, SettingsConfigDict

class AakeedoConfig(BaseSettings):
    """
    Configuration settings for the Kanji API client.

    This model loads settings from environment variables. It can also load
    from a .env file if present in the application's root directory.
    """
    kanji_api_base_url: HttpUrl = Field(
        default="https://kanjiapi.dev/v1",
        description=(
            "The base URL for the Kanji API. "
            "This value can be overridden by setting the KANJI_API_BASE_URL environment variable."
        )
    )
    wanikani_api_base_url: HttpUrl = Field(
        default="https://api.wanikani.com/v2/",
        description="The base URL for the WaniKani API v2."
    )
    wanikani_api_revision: str = Field(
        default="20170710",
        description="The WaniKani API revision date required in headers."
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

_cached_config: AakeedoConfig | None = None

def get_env_configs() -> AakeedoConfig:
    """
    Retrieves a cached instance of the KanjiApiConfig.

    This function ensures that the configuration is loaded only once and reused,
    which is efficient and prevents repeated disk I/O if using .env files.

    Returns:
        The application's Kanji API configuration settings.
    """
    global _cached_config

    if _cached_config is None:
        _cached_config = AakeedoConfig()
    return _cached_config
