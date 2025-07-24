from dataclasses import dataclass

from aiogram.types import BotCommand


@dataclass
class CommandsGroup:
    name: str
    commands: list[BotCommand]

    def __str__(self) -> str:
        return f"{self.name}\n" + "\n".join(
            f"/{x.command} - {x.description}" for x in self.commands
        )
