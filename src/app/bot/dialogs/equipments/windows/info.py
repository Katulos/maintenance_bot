from typing import Any

from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo
from aiogram_dialog.widgets.text import List

from app.bot.states.dialog import (
    EquipmentsMenuSG,
    MainMenuSG,
    MaintenanceMenuSG,
)
from app.bot.utils.i18n_format import I18NFormat, Transformer
from app.core.infrastructure.services.odoo import OdooService


async def _equipment_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
) -> dict[str, Any]:
    equipment_id = dialog_manager.dialog_data.get("equipment_id")
    equipment = await odoo.fetch_equipment(equipment_id)
    return {"equipment": equipment}


window = Window(
    I18NFormat("equipment-info-title"),
    List(
        Transformer(
            I18NFormat("equipment-info"),
            {
                "category": F["item"].category_id.name,
                "name": F["item"].name,
                "serial_no": F["item"].serial_no,
                "user": F["item"].technician_user_id.name,
            },
        ),
        items="equipment",
    ),
    Row(
        SwitchTo(
            text=I18NFormat("maintenance-show-button"),
            id="info_maintenance",
            state=MaintenanceMenuSG.MAINTENANCE_PAGER,
        ),
    ),
    Row(
        Row(
            SwitchTo(
                text=I18NFormat("back-button"),
                id="equipments",
                state=EquipmentsMenuSG.EQUIPMENTS_PAGER,
            ),
            Start(
                I18NFormat("menu-button"),
                id="main",
                state=MainMenuSG.MAIN,
                mode=StartMode.RESET_STACK,
            ),
        ),
    ),
    getter=_equipment_getter,
    state=EquipmentsMenuSG.EQUIPMENT_INFO,
)
