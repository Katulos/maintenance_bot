from dataclasses import dataclass, field
from typing import Literal


@dataclass(kw_only=True, frozen=True, slots=True)
class OdooConfig:
    host: str

    database: str

    username: str

    password: str

    port: int = field(default=8069)

    protocol: Literal["jsonrpc", "jsonrpc+ssl"] = field(default="jsonrpc+ssl")
