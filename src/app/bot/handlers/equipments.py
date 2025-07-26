from typing import Any

from aiogram import Bot, types
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from app.bot.states.dialog import EquipmentsMenuSG


async def equipments_list_command(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        EquipmentsMenuSG.EQUIPMENTS_PAGER,
        mode=StartMode.RESET_STACK,
    )


async def equipment_info(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["equipment_id"] = selected_item
    await dialog_manager.switch_to(EquipmentsMenuSG.EQUIPMENT_INFO)
