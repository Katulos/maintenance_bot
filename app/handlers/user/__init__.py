from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart

from . import start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.register(start.start, CommandStart())
    return user_router
