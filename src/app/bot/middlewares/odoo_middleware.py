import logging
from collections.abc import Awaitable, Callable
from typing import Any

import odoorpc
from aiogram import BaseMiddleware, html
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from dishka import AsyncContainer

from app.bot.utils.i18n_format import I18N_FORMAT_KEY
from app.core.config.main import Config
from app.core.infrastructure.odoo.odoo import Odoo


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
        if not user:
            logging.error("Received event without from_user")
            return None

        container: AsyncContainer = data["dishka_container"]
        odoo: Odoo = await container.get(Odoo)
        config = await container.get(Config)
        i18n = data[I18N_FORMAT_KEY]

        # Check if user is in config
        if user.id not in config.odoo.users:
            logging.warning(
                f"User {user.id} is missing from the configuration file",
            )
            await self._notify_user(
                event,
                i18n(
                    "no-register-message",
                    {
                        "user_id": user.id,
                        "user_full_name": html.quote(user.full_name),
                    },
                ),
            )
            return None

        try:
            user_settings = config.odoo.users[user.id]
            odoo.login(
                db=config.odoo.database,
                login=user_settings.username,
                password=user_settings.password,
            )
        except (odoorpc.error.RPCError, KeyError) as e:
            logging.error(f"Failed to login to Odoo: {e}")
            await self._notify_user(
                event,
                i18n(
                    "no-register-message",
                    {
                        "user_id": user.id,
                        "user_full_name": html.quote(user.full_name),
                    },
                ),
            )
            return None

        # Check if user exists in Odoo
        odoo_user = await odoo.fetch_user(user.id)
        if not odoo_user or not hasattr(odoo_user, "id"):
            logging.error(
                f"User {user.id} is not registered in Odoo or has no id attribute",
            )
            await self._notify_user(
                event,
                i18n(
                    "no-register-callback-message"
                    if isinstance(event, CallbackQuery)
                    else "no-register-message",
                    {
                        "user_id": user.id,
                        "user_full_name": html.quote(user.full_name),
                    },
                ),
            )
            return None

        return await handler(event, data)

    @staticmethod
    async def _notify_user(
        event: Message | CallbackQuery,
        message: str,
        parse_mode: ParseMode = ParseMode.HTML,
    ) -> None:
        if isinstance(event, Message):
            await event.answer(message, parse_mode=parse_mode)
        elif isinstance(event, CallbackQuery):
            await event.answer(message, show_alert=True)
