from __future__ import annotations

import odoorpc
import structlog
from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, Row
from aiogram_dialog.widgets.text import List

from ..config import settings
from ..states import MAIN_MENU_BTN, DialogSG
from ..utils.i18n_format import I18NFormat, Transformer


async def _equipment_info(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo_logger: structlog.typing.FilteringBoundLogger,
    **kwargs,
) -> None:
    try:
        odoo: odoorpc.ODOO = dialog_manager.middleware_data.get("odoo")
        user_id = event_from_user.id
        equipment_id = dialog_manager.dialog_data.get("equipment_id")

        if user_id not in settings.odoo.users:
            odoo_logger.error("User is missing from the configuration file")
            return {"equipment": []}

        odoo.login(
            db=settings.odoo.database,
            login=settings.odoo.users[user_id].username,
            password=settings.odoo.users[user_id].password,
        )

        equipment = odoo.env["maintenance.equipment"].browse(equipment_id)

        return {"equipment": equipment}

    except odoorpc.error.RPCError as e:
        odoo_logger.error(e)
        return {"equipment": []}


window = Window(
    I18NFormat("equipment-info-title"),
    List(
        # Category: { $category }\nName: { $name}\nSerial: { $serial_no }\nEmployee: { $employee }
        Transformer(
            I18NFormat("equipment-info"),
            {
                "category": F["item"].category_id.name,
                "name": F["item"].name,
                "serial_no": F["item"].serial_no,
                "employee": F["item"].employee_id.name,
            },
        ),
        items="equipment",
    ),
    Row(
        Back(text=I18NFormat("back-button")),
        MAIN_MENU_BTN,
        Cancel(
            text=I18NFormat("close-button"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
    ),
    getter=_equipment_info,
    state=DialogSG.EQUIPMENT_INFO,
)
