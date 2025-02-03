from __future__ import annotations

import logging
import os
import pathlib
import sys
from typing import Dict, List, Tuple, Type

from pydantic import BaseModel, Field, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

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
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


class AppConfig(BaseModel):
    BASE_DIR: pathlib.Path = Field(
        default=BASE_DIR,
    )

    debug: bool = Field(default=False)

    supported_locales: List[str] = ["en", "ru"]

    default_locale: str = Field(default="en")

    @property
    def logging_level(self) -> str:
        return "DEBUG" if self.debug else "INFO"

    fsm_storage_path: pathlib.Path = Field(
        default=os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent,
            "data",
            "fsm_storage.db",
        ),
    )


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

    users: Dict[int, OdooUserCredentials]


class Settings(AbstractSettings):
    try:
        app: AppConfig
        bot: BotConfig
        odoo: OdooConfig
    except ValidationError as e:
        logger.critical(e)
        sys.exit(0)
    except ValueError as e:
        logger.critical("Configuration file validation error: %s", e)
        sys.exit(0)


try:
    settings = Settings()
except ValidationError as e:
    logger.critical(e)
    sys.exit(0)
except ValueError as e:
    logger.critical("Configuration file validation error: %s", e)
    sys.exit(0)
