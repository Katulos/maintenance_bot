from dataclasses import dataclass, field

from app.core.config.api import ApiConfig
from app.core.config.bot import BotConfig
from app.core.config.core import CoreConfig
from app.core.config.db import DbConfig
from app.core.config.odoo import OdooConfig
from app.core.config.redis import RedisConfig


@dataclass(kw_only=True, frozen=True, slots=True)
class Config:
    #
    api: ApiConfig = field(default_factory=ApiConfig)

    #
    core: CoreConfig = field(default_factory=CoreConfig)

    #
    bot: BotConfig = field(default_factory=BotConfig)

    #
    db: DbConfig = field(default_factory=DbConfig)

    #
    odoo: OdooConfig = field(default_factory=OdooConfig)

    #
    redis: RedisConfig = field(default_factory=RedisConfig)
