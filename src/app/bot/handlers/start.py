from aiogram import types
from aiogram_dialog import DialogManager, StartMode

from app.bot.states import MainMenuSG


async def start_command(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MainMenuSG.MAIN, mode=StartMode.RESET_STACK)
