from __future__ import annotations

from typing import Any

import structlog
from aiogram import html, types
from aiogram.filters import BaseFilter

from ..services.odoo import fetch_employee


class OdooRegisterFilter(BaseFilter):
    async def __call__(
        self,
        message: types.Message,
        odoo_logger: structlog.typing.FilteringBoundLogger,
        **kwargs: Any,
    ) -> bool:
        employee = await fetch_employee(message.from_user)

        if not employee:
            odoo_logger.error("User is not registered in Odoo")
            await self._send_welcome_message(
                message,
            )
            return False
        return True

    async def _send_welcome_message(
        self,
        message: types.Message,
    ) -> None:
        user = message.from_user
        user_id = user.id
        user_full_name = html.quote(user.full_name)

        m = [
            f"Hello, <a href='tg://user?id={user_id}'>{user_full_name}</a>!",
            "We haven't met.",
            "Please contact your system administrator.",
        ]
        await message.answer(
            "\n".join(m),
        )
