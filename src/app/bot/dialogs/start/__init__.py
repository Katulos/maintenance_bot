from aiogram import Dispatcher, F, Router
from aiogram.enums import ChatType
from aiogram_dialog import (
    Dialog,
)

from app.bot.dialogs.start.windows import list


def setup(dp: Dispatcher) -> None:
    dp.include_router(
        Dialog(list.window),
    )
