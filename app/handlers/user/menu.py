from __future__ import annotations

from aiogram import types
from aiogram_dialog import DialogManager, StartMode

from ...states import DialogSG


async def menu(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(DialogSG.MAIN, mode=StartMode.RESET_STACK)
