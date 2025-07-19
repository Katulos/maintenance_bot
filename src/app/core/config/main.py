from dataclasses import dataclass, field

from app.core.config.bot import BotConfig
from app.core.config.core import CoreConfig


@dataclass
class Config:
    core: CoreConfig = field(default_factory=CoreConfig)

    #
    bot: BotConfig = field(default_factory=BotConfig)
