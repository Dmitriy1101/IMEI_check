"""
Main settings object "settings" is here.
"""

import os
from pathlib import Path
from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Base settings."""

    BASE_DIR: Path = Path(__file__).parent.parent.resolve()

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_DB: str

    TOKEN_SANDBOX: str = os.environ.get("TOKEN_SANDBOX", "")
    TOKEN_LIVE: str = os.environ.get("TOKEN_LIVE", "")
    DB_SCHEMA: str = os.environ.get("DB_SCHEMA", "test_back")

    TEST_TOKEN: str = (
        "cf4gJ5Qovk2W0ZJ4zSth7SjweFsbfv7SNigImdzhVt3uue9bi3_UIyJPNtzNaEyJDHFaD6KYkHO-JMob"
    )


class DockerSettings(Settings):
    """Docker"""

    # PostgreSQL
    DATABASE_USER: str = os.environ.get("DB_USER")
    DATABASE_PASSWORD: str = os.environ.get("DB_PASS")
    DATABASE_HOST: str = os.environ.get("DB_HOST")
    DATABASE_PORT: int = os.environ.get("DB_PORT")
    DATABASE_DB: str = os.environ.get("DB_DB")

    # Redis
    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: int = os.environ.get("REDIS_PORT")
    REDIS_DB: int = os.environ.get("REDIS_DB")


class LocalSettings(Settings):
    """LOcal is local"""

    # PostgreSQL
    DATABASE_USER: str = "dbuser"
    DATABASE_PASSWORD: str = "pass"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = "15432"
    DATABASE_DB: str = "dbname"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 1


def get_settings() -> Union[LocalSettings, DockerSettings]:
    """Get settings obj by 'TYPE_ENV' env variable."""

    config_cls_dict = {
        "docker": DockerSettings,
        "test": LocalSettings,
    }

    env_type = os.environ.get("TYPE_ENV", "test")

    if env_type not in config_cls_dict:
        raise NameError("environment variable 'TYPE_ENV' is invalid ")

    config_cls = config_cls_dict[env_type]

    return config_cls()


settings: Union[DockerSettings, LocalSettings] = get_settings()
