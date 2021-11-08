import logging
from functools import lru_cache

from pydantic import BaseSettings
from pydantic.networks import PostgresDsn

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = "postgresql://postgres@localhost:5432/postgres"
    SECRET: str = "secret"


@lru_cache()
def get_settings():
    settings = Settings()
    logging.info(settings)
    return settings
