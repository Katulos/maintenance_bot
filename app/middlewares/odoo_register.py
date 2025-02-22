from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware, html
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

from ..services.odoo import fetch_employee
from ..utils.i18n_format import I18N_FORMAT_KEY


class OdooRegisterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [Message | CallbackQuery, dict[str, Any]],
            Awaitable[Any],
        ],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        employee = await fetch_employee(event.from_user)

        if not employee:
            user_id = event.from_user.id
            user_full_name = html.quote(event.from_user.full_name)
            i18n = data[I18N_FORMAT_KEY]

            data["odoo_logger"].error(
                f"User {user_id} is not registered in Odoo",
            )

            await event.answer(
                i18n(
                    "no-register-message",
                    {"user_id": user_id, "user_full_name": user_full_name},
                ),
                parse_mode=ParseMode.HTML,
            )
            return False

        return await handler(event, data)
