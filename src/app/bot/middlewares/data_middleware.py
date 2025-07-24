from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.data import MiddlewareData
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory, DialogManager
from aiogram_dialog.api.entities import Context, Stack
from dishka import AsyncContainer

from app.core.config.bot import BotConfig
from app.core.infrastructure.odoo import Odoo


class DialogMiddlewareData(MiddlewareData, total=False):
    dialog_manager: DialogManager
    aiogd_stack: Stack
    aiogd_context: Context


class LrmMiddlewareData(DialogMiddlewareData, total=False):
    config: BotConfig
    dishka_container: AsyncContainer
    odoo: Odoo
    # scheduler: Scheduler
    bg_manager_factory: BgManagerFactory


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: LrmMiddlewareData,
    ) -> Any:
        container = data["dishka_container"]
        result = await handler(event, data)
        return result
