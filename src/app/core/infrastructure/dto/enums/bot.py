from enum import Enum


class BotApiType(Enum):
    OFFICIAL = "official"
    LOCAL = "local"


class BotFsmType(Enum):
    MEMORY = "memory"
    REDIS = "redis"
