import logging
from functools import lru_cache

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.networks import PostgresDsn

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", frozen=True)

    db_dsn: PostgresDsn = PostgresDsn("postgresql://postgres@postgres:5432/postgres")

    # Настройки проверки токенов
    oidc_configuration_uri: AnyHttpUrl
    oidc_client_id: str

    # Настройки разрешения прав
    oidc_admin_claim: str = "groups"
    oidc_admin_claim_value: str = "redirector_admin"

    secret: str | None = None


@lru_cache()
def get_settings():
    return Settings()  # type: ignore
