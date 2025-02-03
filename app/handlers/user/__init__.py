from __future__ import annotations

from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart, StateFilter

from ... import states
from ...filters import ChatTypeFilter, OdooRegisterFilter, TextFilter
from . import equipments, help, start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter("private"))
    user_router.message.filter(OdooRegisterFilter())

    user_router.message.register(start.start, CommandStart())
    user_router.message.register(
        start.start,
        TextFilter("🏠Home"),
        StateFilter(states.user.UserMainMenu.main_menu),
    )

    user_router.message.register(equipments.equipments)
    user_router.message.register(
        equipments.equipments,
        TextFilter("⚙️ My Equipments"),
    )
    user_router.message.register(help.help)

    return user_router
