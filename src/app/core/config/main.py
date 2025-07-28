from dataclasses import dataclass, field

from app.core.config.bot import BotConfig
from app.core.config.core import CoreConfig
from app.core.config.odoo import OdooConfig
from app.core.config.redis import RedisConfig


@dataclass
class Config:
    core: CoreConfig = field(default_factory=CoreConfig)

    #
    bot: BotConfig = field(default_factory=BotConfig)

    #
    odoo: OdooConfig = field(default_factory=OdooConfig)

    #
    redis: RedisConfig = field(default_factory=RedisConfig)
