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
    Validator(
        "core.debug",
        is_type_of=bool,
        default=False,
    ),
    # db
    Validator(
        "db.database_url",
        is_type_of=str,
        default="postgresql+asyncpg://devel:devel@db:5432/devel",
    ),
    Validator("db.echo", is_type_of=bool, default=False),
    # API
    Validator("api.bind", is_type_of=str, default="127.0.0.1"),
    Validator("api.port", is_type_of=int, default=8000),
    Validator("api.enable_access_log", is_type_of=bool, default=False),
    # bot
    Validator("bot.token", is_type_of=str),
    Validator("bot.page_size", is_type_of=int, default=5),
    Validator(
        "bot.api_type",
        is_type_of=str,
        is_in=["local", "official"],
        default="official",
    ),
    Validator(
        "bot.api_server_base",
        is_type_of=str,
        default="http://local-bot-api:8081",
    ),
    Validator(
        "bot.is_local",
        is_type_of=bool,
        default=False,
    ),
    Validator(
        "bot.fsm_type",
        is_type_of=str,
        is_in=["memory", "redis"],
        default="memory",
    ),
    Validator("bot.use_webhook", is_type_of=bool, default=False),
    Validator("bot.use_local_server", is_type_of=bool, default=False),
    Validator(
        "bot.webhook_path",
        is_type_of=str,
        default="/tg/webhooks/bot/{bot_id}",
    ),
    Validator("bot.webhook_listening_host", is_type_of=str, default="bot"),
    Validator("odoo.bot.webhook_listening_port", is_type_of=int, default=88),
    Validator(
        "bot.webhook_max_updates_in_queue", is_type_of=int, default=100
    ),
    Validator(
        "bot.webhook_secret_token", is_type_of=str | None, default=None
    ),
    # Odoo
    Validator("odoo.host", is_type_of=str),
    Validator("odoo.database", is_type_of=str),
    Validator("odoo.username", is_type_of=str),
    Validator("odoo.password", is_type_of=str),
    Validator("odoo.port", is_type_of=int, default=8069),
    Validator(
        "odoo.protocol",
        is_type_of=str,
        is_in=["jsonrpc", "jsonrpc+ssl"],
        default="jsonrpc+ssl",
    ),
    # Redis
    Validator("redis.host", is_type_of=str, default="redis"),
    Validator("redis.port", is_type_of=int, default=6379),
    Validator("redis.db", is_type_of=int, default=0),
    Validator("redis.username", is_type_of=str | None, default=None),
    Validator("redis.password", is_type_of=str | None, default=None),
)

try:
    settings.validators.validate_all()
except ValidationError as e:
    logging.error(e.message)
    sys.exit(1)
