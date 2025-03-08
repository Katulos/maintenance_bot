from __future__ import annotations

from aiogram import types
from aiogram_dialog import DialogManager, StartMode

from ...states.dialog import MenuSG


async def start(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MenuSG.MAIN, mode=StartMode.RESET_STACK)
