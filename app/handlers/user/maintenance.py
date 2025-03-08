from __future__ import annotations

from typing import Any

from aiogram import Bot, types
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode

from ...services.odoo import OdooService
from ...states.dialog import MaintenanceSG


async def maintenance(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        MaintenanceSG.MAINTENANCE_PAGER,
        mode=StartMode.RESET_STACK,
    )


async def maintenance_new(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        MaintenanceSG.MAINTENANCE_NEW,
        mode=StartMode.RESET_STACK,
    )


async def maintenance_info_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenanceSG.MAINTENANCE_INFO)


async def maintenance_accept_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenanceSG.MAINTENANCE_ACCEPT)


async def maintenance_forward_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenanceSG.MAINTENANCE_FORWARD)


async def maintenance_forward_done(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    maintenance_id = dialog_manager.dialog_data["maintenance_id"]
    user_id = selected_item
    odoo: OdooService = dialog_manager.middleware_data["odoo"]
    await odoo.forward_maintenance(maintenance_id, user_id)
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def maintenance_close_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenanceSG.MAINTENANCE_CLOSE)
