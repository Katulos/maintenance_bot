from __future__ import annotations

import asyncio
from collections import deque
from time import time
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from ..config import settings

blacklist: set[int] = set(settings.bot.blacklist)
whitelist = settings.bot.whitelist

_users: dict[int, deque[float]] = {}


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 15) -> None:
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.rate_limit = rate_limit

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Any],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if user_id in self.whitelist:
            return await handler(event, data)

        if user_id in self.blacklist:
            return

        if await self._is_flood(user_id):
            self.blacklist.add(user_id)
            asyncio.create_task(
                self._remove_from_blacklist(user_id, self.rate_limit),
            )
            data["business_logger"].error(f"User {user_id} Flood detected")
            return

        return await handler(event, data)

    @staticmethod
    async def _is_flood(
        user_id: int,
        messages: int = 3,
        seconds: int = 15,
    ) -> bool:
        now = time()
        user_timestamps = _users.setdefault(user_id, deque())
        user_timestamps.append(now)

        count = 0
        for timestamp in reversed(user_timestamps):
            if now - timestamp < seconds:
                count += 1
            else:
                break

        return count > messages

    async def _remove_from_blacklist(
        self,
        user_id: int,
        delay: int = 15,
    ) -> None:
        await asyncio.sleep(delay)
        if user_id in self.blacklist:
            self.blacklist.remove(user_id)
            if user_id in _users:
                del _users[user_id]
