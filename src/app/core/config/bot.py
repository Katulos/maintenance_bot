from dataclasses import dataclass, field
from enum import Enum


@dataclass
class BotApiType(Enum):
    OFFICIAL = "official"
    LOCAL = "local"


@dataclass
class BotFsmType(Enum):
    MEMORY = "memory"
    REDIS = "redis"


@dataclass
class BotConfig:
    token: str

    page_size: int = field(default=5)

    drop_previous_updates: bool = field(default=False)

    api_type: BotApiType = field(default=BotApiType.OFFICIAL)

    api_server_base: str = field(default="http://local-bot-api:8081")

    @property
    def is_local(self) -> bool:
        match self.api_type:
            case BotApiType.OFFICIAL:
                return False
            case BotApiType.LOCAL:
                return True
            case _:
                raise ValueError(f"Invalid bot api type: {self.api_type}")

    @property
    def bot_id(self) -> int:
        return int(self.token.split(":")[0])

    fsm_type: BotFsmType = field(default=BotFsmType.REDIS)

    use_webhook: bool = field(default=False)

    use_local_server: bool = field(default=False)

    webhook_path: str = field(
        default="/tg/webhooks/bot/{bot_id} ",
    )

    @property
    def webhook_address(self) -> str:
        return (
            "http://"
            + self.webhook_listening_host
            + ":"
            + str(self.webhook_listening_port)
            + self.webhook_path
        )

    webhook_listening_host: str = field(default="bot")

    webhook_listening_port: int = field(default=88)

    webhook_max_updates_in_queue: int = field(default=100)

    webhook_secret_token: str | None = None
