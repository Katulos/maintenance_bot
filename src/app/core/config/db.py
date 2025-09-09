from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True, slots=True)
class DbConfig:
    host: str = field(default="db")

    port: int = field(default=5432)

    username: str | None = None

    password: str | None = None

    database: str | None = None

    echo: bool = False

    @property
    def dsn(self) -> str:
        required_fields = [
            "username",
            "password",
            "host",
            "port",
            "database",
        ]
        missing = [
            field for field in required_fields if not getattr(self, field)
        ]
        if missing:
            raise ValueError(
                f"Missing required parameters for connection: {', '.join(missing)}",
            )

        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
