from __future__ import annotations

import odoorpc
from aiogram import html, types
from aiogram.filters import BaseFilter

from ..config import settings


class OdooRegisterFilter(BaseFilter):
    async def __call__(
        self,
        message: types.Message,
        odoo: odoorpc.ODOO,
    ) -> bool:
        user = message.from_user
        user_id = user.id
        user_full_name = html.quote(user.full_name)

        if user_id not in settings.odoo.users:
            await self._send_welcome_message(message, user_id, user_full_name)
            return False

        try:
            odoo.login(
                db=settings.odoo.database,
                login=settings.odoo.users[user_id].username,
                password=settings.odoo.users[user_id].password,
            )
        except odoorpc.error.RPCError:
            await self._send_welcome_message(message, user_id, user_full_name)
            return False

        hr = odoo.env["hr.employee"]
        employee_id = hr.search([("telegram_id", "=", user_id)], limit=1)
        if not employee_id:
            await self._send_welcome_message(message, user_id, user_full_name)
            return False

        return True

    async def _send_welcome_message(
        self,
        message: types.Message,
        user_id: int,
        user_full_name: str,
    ) -> None:
        m = [
            "Hello, <a href='tg://user?id={user_id}'>{user_full_name}</a>!".format(
                user_id=user_id,
                user_full_name=user_full_name,
            ),
            "We haven't met.",
            "Please contact your system administrator.",
        ]
        await message.answer(
            "\n".join(m),
        )
