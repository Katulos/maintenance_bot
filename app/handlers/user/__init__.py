from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.i18n import gettext as _

from ... import states
from ...filters import ChatTypeFilter, TextFilter
from . import start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter("private"))

    user_router.message.register(start.start, CommandStart())
    user_router.message.register(
        start.start,
        TextFilter(_("🏠Home")),
        StateFilter(states.user.UserMainMenu.menu),
    )

    return user_router
