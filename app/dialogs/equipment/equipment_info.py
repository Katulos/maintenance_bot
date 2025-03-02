from __future__ import annotations

from typing import Any

import structlog
from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Row, SwitchTo
from aiogram_dialog.widgets.text import List

from ...services.odoo import OdooService

# from ...services.odoo import fetch_equipment
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat, Transformer


async def _equipment_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    aiogram_session_logger: structlog.typing.FilteringBoundLogger,
    **kwargs: Any,
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
            state=DialogSG.MAINTENANCE_PAGER,
        ),
    ),
    Row(
        Row(
            SwitchTo(
                text=I18NFormat("back-button"),
                id="equipments",
                state=DialogSG.EQUIPMENTS_PAGER,
            ),
            MAIN_MENU_BTN,
        ),
    ),
    getter=_equipment_getter,
    state=DialogSG.EQUIPMENT_INFO,
)
