import logging
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

# Путь к конфигу:
# C:\Users\Alexey\Desktop\Python\Stepic_Suren\
# fastapi-url-shortener\url-shortener\core\config.py

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisDbConfig(BaseModel):
    default: int = 0
    redis_db_tokens: int = 1
    redis_db_users: int = 2
    redis_db_short_urls: int = 3

    @model_validator(mode="after")
    def check_db(self) -> Self:
        db_values = list(self.model_dump().values())
        if len(set(db_values)) != len(db_values):
            error_msg = "Database numbers should be unique!"
            raise ValueError(error_msg)
        return self


class RedisNamesConfig(BaseModel):
    tokens_set: str = "tokens"
    short_urls_hash_name: str = "short_urls_hash_name"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    database: RedisDbConfig = RedisDbConfig()
    names: RedisNamesConfig = RedisNamesConfig()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        env_nested_delimiter="__",
        env_prefix="URL_SHORTENER__",
        yaml_file=(
            BASE_DIR / "config.default.yaml",
            BASE_DIR / "config.local.yaml",
        ),
        yaml_config_section="url-shortener",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for
            loading the settings values.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()
