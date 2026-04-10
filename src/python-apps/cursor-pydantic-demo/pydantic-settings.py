from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: SecretStr
    database_url: str
    debug: bool = False
    max_connections: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

print(f"API_KEY: {settings.api_key}")
print(f"DATABASE_URL: {settings.database_url}")
print(f"DEBUG: {settings.debug}")
print(f"MAX_CONNECTIONS: {settings.max_connections}")
