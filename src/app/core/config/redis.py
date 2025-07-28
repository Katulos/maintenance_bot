from dataclasses import dataclass, field


@dataclass
class RedisConfig:
    host: str = field(default="redis")

    port: int = field(default=6379)

    db: int = field(default=1)

    username: str = field(default="")

    password: str = field(default="")
