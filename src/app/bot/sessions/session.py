import asyncio
import logging
import time
from typing import Any

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import (
    RestartingTelegram,
    TelegramRetryAfter,
    TelegramServerError,
)
from aiogram.methods.base import TelegramMethod, TelegramType


class Session(AiohttpSession):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        st = time.monotonic()
        logging.debug("Making request to API")
        try:
            res = await super().make_request(bot, method, timeout)
        except Exception as e:
            logging.exception(
                f"API error {e} time_spent_ms={(time.monotonic() - st) * 1000}",
            )
            raise
        response = (
            res.model_dump(exclude_none=True, exclude_unset=True)
            if hasattr(res, "model_dump")
            else res
        )
        logging.debug(
            f"API response:{response} time_spent_ms={(time.monotonic() - st) * 1000}",
        )
        return res


class SmartSession(Session):
    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        attempt = 0
        while True:
            attempt += 1
            try:
                res = await super().make_request(bot, method, timeout)
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except (RestartingTelegram, TelegramServerError):
                if attempt > 6:
                    sleepy_time = 64
                else:
                    sleepy_time = 2**attempt
                await asyncio.sleep(sleepy_time)
            except Exception:
                raise
            else:
                return res
