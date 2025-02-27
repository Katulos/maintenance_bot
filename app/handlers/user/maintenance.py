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


async def maintenance_new(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        DialogSG.MAINTENANCE_NEW,
        mode=StartMode.RESET_STACK,
    )


async def maintenance_info(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(DialogSG.MAINTENANCE_INFO)


async def maintenance_accept(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(DialogSG.MAINTENANCE_ACCEPT)


async def maintenance_forward(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(DialogSG.MAINTENANCE_FORWARD)


async def maintenance_close(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(DialogSG.MAINTENANCE_CLOSE)
