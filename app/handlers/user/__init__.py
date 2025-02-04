from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart

from ...filters import ChatTypeFilter, OdooRegisterFilter
from . import start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter("private"))
    user_router.message.filter(OdooRegisterFilter())

    user_router.message.register(start.start, CommandStart())
    return user_router
