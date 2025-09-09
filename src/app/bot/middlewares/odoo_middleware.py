import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, html
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message, TelegramObject, User
from dishka import AsyncContainer

from app.bot.utils.i18n_format import I18N_FORMAT_KEY
from app.core.config.main import Config


class OdooMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any | None:
        user: User | None = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        try:
            container: AsyncContainer = data["dishka_container"]
            dao: OdooDao = await container.get(OdooDao)
            config = await container.get(Config)
            i18n = data[I18N_FORMAT_KEY]

            if user.id not in config.odoo.users:
                logging.warning(
                    f"User {user.id} is missing from the configuration file",
                )
                await self._send_not_registered_response(event, user, i18n)
                return None

            if not await dao.res_users.get_by_tg_id(user.id):
                logging.error(f"User {user.id} not found in Odoo")
                await self._send_not_registered_response(event, user, i18n)
                return None

        except (TelegramBadRequest, AttributeError) as e:
            logging.exception(e)
            return None

        return await handler(event, data)

    @staticmethod
    async def _send_not_registered_response(
        event: Message | CallbackQuery,
        user: User,
        i18n: Callable,
    ) -> None:
        context = {"user_full_name": html.quote(user.full_name)}

        if isinstance(event, Message):
            context["user_id"] = user.id
            await event.reply(
                i18n("no-register-message", context),
                parse_mode=ParseMode.HTML,
            )
        elif isinstance(event, CallbackQuery):
            await event.answer(
                i18n("no-register-callback-message", context),
                show_alert=True,
            )
