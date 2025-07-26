from dataclasses import dataclass, field


@dataclass
class BotConfig:
    token: str

    page_size: int = field(default=5)
