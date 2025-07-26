from aiogram import Dispatcher, F, Router
from aiogram.enums import ChatType
from aiogram_dialog import (
    Dialog,
)

from app.bot.dialogs.equipments.windows import info, list


def setup(dp: Dispatcher) -> None:
    dp.include_router(
        Dialog(info.window, list.window),
    )
