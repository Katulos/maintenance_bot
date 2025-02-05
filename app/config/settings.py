from __future__ import annotations

import pathlib
import sys

from pydantic import BaseModel, Field, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from .. import utils

logger = utils.logging.setup_logger().bind(type="business")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

config = BASE_DIR / "config.yaml"

if config.is_file():
    logger.info("Using config file: %s", config)
else:
    logger.critical("Can't find config file: %s", config)
    logger.critical("The application is shutting down")
    sys.exit(1)


class AbstractSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
        env_nested_delimiter=".",
        yaml_file=config,
        yaml_file_encoding="utf-8",
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
        return (YamlConfigSettingsSource(settings_cls),)


class AppConfig(BaseModel):
    BASE_DIR: pathlib.Path = Field(
        default=BASE_DIR,
    )

    debug: bool = Field(default=False)

    supported_locales: list[str] = ["en", "ru"]

    default_locale: str = Field(default="en")

    @property
    def logging_level(self) -> str:
        return "DEBUG" if self.debug else "INFO"


class BotConfig(BaseModel):
    token: str


class OdooUserCredentials(BaseModel):
    username: str

    password: str


class OdooConfig(BaseModel):
    host: str

    port: int = Field(default=8069)

    database: str

    protocol: str = Field(default="jsonrpc+ssl")

    users: dict[int, OdooUserCredentials]


class Settings(AbstractSettings):
    app: AppConfig
    bot: BotConfig
    odoo: OdooConfig


try:
    settings = Settings()
    logger.info("Configuration loaded")
except (ValueError, ValidationError) as e:
    logger.critical("Configuration file validation error: %s", e)
    sys.exit(0)
