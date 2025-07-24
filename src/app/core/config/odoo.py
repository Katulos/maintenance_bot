from dataclasses import dataclass, field
from typing import Literal


@dataclass
class OdooUserCredentials:
    username: str

    password: str

@dataclass
class OdooConfig:
    host: str

    database: str

    users: dict[int, OdooUserCredentials]

    port: int = field(default=8069)

    protocol: Literal["jsonrpc", "jsonrpc+ssl"] = field(default="jsonrpc+ssl")
