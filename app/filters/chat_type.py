from __future__ import annotations

import typing

from aiogram import types


class ChatTypeFilter:
    def __init__(self, chat_type: str | typing.Sequence[str]):
        self.chat_type = chat_type

    async def __call__(self, message: types.Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type  # type: ignore[no-any-return]
        return message.chat.type in self.chat_type
