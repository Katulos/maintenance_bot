from __future__ import annotations

from typing import Any

from aiogram import Bot, types
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from ...states import DialogSG


async def maintenance(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        DialogSG.MAINTENANCE_PAGER,
        mode=StartMode.RESET_STACK,
    )


async def maintenance_info(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(DialogSG.EQUIPMENT_INFO)
