import logging
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic.networks import PostgresDsn

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = PostgresDsn("postgresql://postgres@postgres:5432/postgres")
    SECRET: str = "secret"


@lru_cache()
def get_settings():
    settings = Settings()
    logging.info(settings)
    return settings
