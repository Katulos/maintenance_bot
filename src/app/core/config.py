import logging
import os
import sys

from dynaconf import Dynaconf, ValidationError, Validator

_BASE_DIR = os.getcwd()


settings = Dynaconf(
    settings_files=[
        "?/etc/mtr/settings.ini",
        "?/etc/mtr/.secrets.ini",
        "?/etc/mtr/settings.toml",
        "?/etc/mtr/.secrets.toml",
        "?/etc/mtr/settings.yaml",
        "?/etc/mtr/.secrets.yaml",
        "?/etc/mtr/settings.yml",
        "?/etc/mtr/.secrets.yml",
        "?~/.config/mtr/settings.ini",
        "?~/.config/mtr/.secrets.ini",
        "?~/.config/mtr/settings.toml",
        "?~/.config/mtr/.secrets.toml",
        "?~/.config/mtr/settings.yaml",
        "?~/.config/mtr/.secrets.yaml",
        "?~/.config/mtr/settings.yml",
        "?~/.config/mtr/.secrets.yml",
        os.path.join(_BASE_DIR, "settings.ini"),
        os.path.join(_BASE_DIR, ".secrets.ini"),
        os.path.join(_BASE_DIR, "settings.toml"),
        os.path.join(_BASE_DIR, ".secrets.toml"),
        os.path.join(_BASE_DIR, "settings.yaml"),
        os.path.join(_BASE_DIR, ".secrets.yaml"),
        os.path.join(_BASE_DIR, "settings.yml"),
        os.path.join(_BASE_DIR, ".secrets.yml"),
    ],
)
settings.validators.register(
    # core
    Validator("core.debug", default=False, is_type_of=bool),
    # API
    Validator("api.bind", is_type_of=str, default="127.0.0.1"),
    Validator("api.port", is_type_of=int, default=8000),
    Validator("api.enable_access_log", is_type_of=bool, default=False),
)

try:
    settings.validators.validate_all()
except ValidationError as e:
    logging.error(e.message)
    sys.exit(1)
