from __future__ import annotations

import asyncio
from collections import deque
from collections.abc import Awaitable
from time import time
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from ..config import settings

# blacklist: set[int] = set(settings.bot.blacklist)
# whitelist = settings.bot.whitelist
#
# _users: dict[int, deque[float]] = {}


class AntiFloodMiddleware(BaseMiddleware):
    _blacklist: set[int] = set(settings.bot.blacklist)

    _whitelist = settings.bot.whitelist

    _users: dict[int, deque[float]] = {}

    def __init__(self, rate_limit: int = 15) -> None:
        self.rate_limit = rate_limit
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.event.from_user.id
        if user_id in self._whitelist:
            return await handler(event, data)

        if user_id in self._blacklist:
            return

        if await self._is_flood(user_id):
            self._blacklist.add(user_id)
            asyncio.create_task(
                self._remove_from_blacklist(user_id, self.rate_limit),
            )
            data["aiogram_logger"].warning("Flood detected", user_id=user_id)
            return

        return await handler(event, data)

    async def _is_flood(
        self,
        user_id: int,
        messages: int = 3,
        seconds: int = 15,
    ) -> bool:
        now = time()
        user_timestamps = self._users.setdefault(user_id, deque())

        while user_timestamps and now - user_timestamps[0] > seconds:
            user_timestamps.popleft()

        user_timestamps.append(now)

        return len(user_timestamps) > messages

    async def _remove_from_blacklist(
        self,
        user_id: int,
        delay: int = 15,
    ) -> None:
        await asyncio.sleep(delay)
        if user_id in self._blacklist:
            self._blacklist.remove(user_id)
            if user_id in self._users:
                del self._users[user_id]
