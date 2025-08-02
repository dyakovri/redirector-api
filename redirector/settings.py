import logging
from functools import lru_cache

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.networks import PostgresDsn

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", frozen=True)

    db_dsn: PostgresDsn = PostgresDsn("postgresql://postgres@postgres:5432/postgres")

    oidc_configuration_uri: AnyHttpUrl
    oidc_client_id: str

    secret: str | None = None


@lru_cache()
def get_settings():
    return Settings()  # type: ignore
