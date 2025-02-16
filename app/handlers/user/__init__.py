from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart

from ...filters import ChatTypeFilter, OdooRegisterFilter
from . import equipments, maintenance, menu, start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter("private"))
    user_router.message.filter(OdooRegisterFilter())

    user_router.message.register(start.start, CommandStart())
    user_router.message.register(
        equipments.equipments,
        Command(commands={"equipments", "eq"}),
    )
    user_router.message.register(
        maintenance.maintenance,
        Command(commands={"maintenance", "ma"}),
    )
    user_router.message.register(menu.menu, Command(commands={"menu"}))
    return user_router
