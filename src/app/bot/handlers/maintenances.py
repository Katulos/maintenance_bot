from typing import Any

from aiogram import Bot, types
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.bot.states.dialog import MaintenancesMenuSG
from app.core.infrastructure.odoo import Odoo


async def maintenances_list_command(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        MaintenancesMenuSG.MAINTENANCE_PAGER,
        mode=StartMode.RESET_STACK,
    )


async def maintenance_new_command(
    message: types.Message,
    dialog_manager: DialogManager,
    bot: Bot,
) -> None:
    await dialog_manager.start(
        MaintenancesMenuSG.MAINTENANCE_NEW,
        mode=StartMode.RESET_STACK,
    )


async def maintenance_info_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenancesMenuSG.MAINTENANCE_INFO)


async def maintenance_accept_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenancesMenuSG.MAINTENANCE_ACCEPT)


async def maintenance_forward_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await dialog_manager.switch_to(MaintenancesMenuSG.MAINTENANCE_FORWARD)


@inject
async def maintenance_forward_done(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
    odoo: FromDishka[Odoo],
) -> None:
    maintenance_id = dialog_manager.dialog_data["maintenance_id"]
    user_id = selected_item
    await odoo.forward_maintenance(maintenance_id, user_id)
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def maintenance_close_switch(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    selected_item: int,
    odoo: FromDishka[Odoo]
) -> None:
    dialog_manager.dialog_data["maintenance_id"] = selected_item
    await odoo.close_maintenance(selected_item)
    await dialog_manager.switch_to(MaintenancesMenuSG.MAINTENANCE_CLOSE)
