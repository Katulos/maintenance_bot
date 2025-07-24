from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory

from app.bot.middlewares.data_middleware import LrmMiddlewareData
from app.core.config.bot import BotConfig
from app.core.infrastructure.odoo import Odoo


class InitMiddleware(BaseMiddleware):
    def __init__(
        self,
        bg_manager_factory: BgManagerFactory,
    ) -> None:
        self.bg_manager_factory = bg_manager_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: LrmMiddlewareData,
    ) -> Any:
        container = data["dishka_container"]
        data["config"] = await container.get(BotConfig)
        data["odoo"] = await container.get(Odoo)

        data["bg_manager_factory"] = self.bg_manager_factory

        # data["dao"] = await container.get(DAO)

        result = await handler(event, data)
        return result
