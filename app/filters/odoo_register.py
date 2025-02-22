from __future__ import annotations

from typing import Any

import structlog
from aiogram import html
from aiogram.filters import BaseFilter
from aiogram.types import Message

from ..services.odoo import fetch_employee


class OdooRegisterFilter(BaseFilter):
    async def __call__(
        self,
        obj: Message,
        odoo_logger: structlog.typing.FilteringBoundLogger,
        **kwargs: Any,
    ) -> bool:
        employee = await fetch_employee(obj.from_user)

        if not employee:
            odoo_logger.error(f"User {obj.from_user.id} is not registered in Odoo")
            await self._send_welcome_message(
                obj,
            )
            return False
        return True

    async def _send_welcome_message(
        self,
        obj: Message,
    ) -> None:
        user = obj.from_user
        user_id = user.id
        user_full_name = html.quote(user.full_name)

        m = [
            f"Hello, <a href='tg://user?id={user_id}'>{user_full_name}</a>!",
            "We haven't met.",
            "Please contact your system administrator.",
        ]
        await obj.answer(
            "\n".join(m),
        )
