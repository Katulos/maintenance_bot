from __future__ import annotations

from collections.abc import Sequence

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | Sequence[str]) -> None:
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type  # type: ignore[no-any-return]
        return message.chat.type in self.chat_type
