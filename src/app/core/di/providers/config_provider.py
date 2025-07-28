import pathlib

from dishka import Provider, Scope, provide

from app.core.config.bot import BotConfig
from app.core.config.loader import ConfigLoader
from app.core.config.main import Config
from app.core.config.odoo import OdooConfig
from app.core.config.redis import RedisConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    def __init__(self, config_path: pathlib.Path) -> None:
        self.config_path = config_path
        super().__init__()

    @provide
    def provide_config(self) -> Config:
        return ConfigLoader.load_config(self.config_path)

    @provide
    def provide_bot_config(self, config: Config) -> BotConfig:
        return config.bot

    @provide
    def provide_odoo_config(self, config: Config) -> OdooConfig:
        return config.odoo

    @provide
    def provide_redis_config(self, config: Config) -> RedisConfig:
        return config.redis
