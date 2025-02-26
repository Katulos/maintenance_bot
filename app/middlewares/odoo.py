from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable

import odoorpc
import structlog
from aiogram import BaseMiddleware, html
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

from ..config import settings
from ..services.odoo import OdooService
from ..utils.i18n_format import I18N_FORMAT_KEY


class OdooMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [Message | CallbackQuery, dict[str, Any]],
            Awaitable[Any],
        ],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user

        odoo: OdooService = data["odoo"]
        logger: structlog.typing.FilteringBoundLogger = data["odoo_logger"]

        if user.id not in settings.odoo.users:
            logger.warning(
                f"User {user.id} is missing from the configuration file",
                type="business",
            )
            return

        try:
            user_settings = settings.odoo.users[user.id]
            odoo.login(
                db=settings.odoo.database,
                login=user_settings.username,
                password=user_settings.password,
            )
        except (odoorpc.error.RPCError, KeyError) as e:
            logger.error(f"Failed to login to Odoo: {e}")
            return

        data["odoo"] = odoo

        employee = await odoo.fetch_employee(event.from_user.id)

        if not employee:
            user_id = event.from_user.id
            user_full_name = html.quote(event.from_user.full_name)
            i18n = data[I18N_FORMAT_KEY]

            logger.error(
                f"User {user_id} is not registered in Odoo",
            )

            if isinstance(event, Message):
                await event.answer(
                    i18n(
                        "no-register-message",
                        {
                            "user_id": user_id,
                            "user_full_name": user_full_name,
                        },
                    ),
                    parse_mode=ParseMode.HTML,
                )

            if isinstance(event, CallbackQuery):
                await event.answer(
                    i18n(
                        "no-register-callback-message",
                        {
                            "user_id": user_id,
                            "user_full_name": user_full_name,
                        },
                    ),
                    show_alert=True,
                )

            return

        return await handler(event, data)
