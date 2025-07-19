import logging
import pathlib

import yaml
from adaptix import Retort

from app.core.config.main import Config


class ConfigLoader:
    @classmethod
    def load_config(cls, config_path: pathlib.Path) -> Config:
        retort = Retort()
        if not config_path.exists():
            logging.critical("Config file not found: %s", config_path)
            exit(1)

        with open(config_path, encoding="utf-8") as f:
            raw_config = yaml.safe_load(f) or {}

        return retort.load(raw_config, Config)
