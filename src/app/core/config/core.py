from dataclasses import dataclass, field


@dataclass
class CoreConfig:
    debug: bool = field(default=False)
