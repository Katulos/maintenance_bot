from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True, slots=True)
class CoreConfig:
    secret_key: str

    debug: bool = field(default=False)
