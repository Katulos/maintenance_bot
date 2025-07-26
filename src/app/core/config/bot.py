from dataclasses import dataclass, field


@dataclass
class BotApiType:
    official = "official"
    local = "local"


@dataclass
class BotConfig:
    token: str

    page_size: int = field(default=5)

    drop_previous_updates: bool = field(default=False)

    type: BotApiType = field(default=BotApiType.official)

    api_server_base: str = field(default="http://local-bot-api:8081")

    @property
    def is_local(self) -> bool:
        match self.type:
            case BotApiType.official:
                return False
            case BotApiType.local:
                return True
            case _:
                raise ValueError(f"Invalid bot api type: {self.type}")

    @property
    def bot_id(self) -> int:
        return int(self.token.split(":")[0])

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
