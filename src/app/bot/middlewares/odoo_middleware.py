import logging
from collections.abc import Awaitable, Callable
from typing import Any

import odoorpc
from aiogram import BaseMiddleware, html
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

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

        odoo: Odoo = data["odoo"]
        config: Config = data["config"]

        if user.id not in config.odoo.users:
            logging.warning(
                f"User {user.id} is missing from the configuration file",
                type="business",
            )
            return

        try:
            user_settings = config.odoo.users[user.id]
            odoo.login(
                db=config.odoo.database,
                login=user_settings.username,
                password=user_settings.password,
            )
        except (odoorpc.error.RPCError, KeyError) as e:
            logging.error(f"Failed to login to Odoo: {e}")
            return

        data["odoo"] = odoo

        odoo_user = await odoo.fetch_user(event.from_user.id)

        if not odoo_user:
            user_id = event.from_user.id
            user_full_name = html.quote(event.from_user.full_name)
            i18n = data[I18N_FORMAT_KEY]

            logging.error(
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
