from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True, slots=True)
class ApiConfig:
    bind: str = field(default="0.0.0.0")

    port: int = field(default=8000)

    enable_access_log: bool = field(default=False)
