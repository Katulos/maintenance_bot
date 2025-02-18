from __future__ import annotations

import odoorpc
import structlog
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, Row

from ..config import settings
from ..states import MAIN_MENU_BTN, DialogSG
from ..utils.i18n_format import I18NFormat


async def _maintenance_info(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo_logger: structlog.typing.FilteringBoundLogger,
    **kwargs,
) -> None:
    try:
        odoo: odoorpc.ODOO = dialog_manager.middleware_data.get("odoo")
        user_id = event_from_user.id
        maintenance_id = dialog_manager.dialog_data.get("maintenance_id")

        if user_id not in settings.odoo.users:
            odoo_logger.error("User is missing from the configuration file")
            return {"maintenance": []}

        odoo.login(
            db=settings.odoo.database,
            login=settings.odoo.users[user_id].username,
            password=settings.odoo.users[user_id].password,
        )

        maintenance = odoo.env["maintenance.request"].browse(maintenance_id)

        return {"maintenance": maintenance}

    except odoorpc.error.RPCError as e:
        odoo_logger.error(e)
        return {"maintenance": []}


window = Window(
    I18NFormat("maintenance-info-title"),
    Row(
        Back(text=I18NFormat("back-button")),
        MAIN_MENU_BTN,
        Cancel(
            text=I18NFormat("close-button"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
    ),
    getter=_maintenance_info,
    state=DialogSG.MAINTENANCE_INFO,
)
