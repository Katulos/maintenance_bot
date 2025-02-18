from __future__ import annotations

import odoorpc
import structlog
from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Row, Select
from aiogram_dialog.widgets.text import List

from ...config import settings
from ...handlers.user.maintenance import (
    accept_maintenance,
    close_maintenance,
    forward_maintenance,
)
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat, Transformer


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
    List(
        Transformer(
            I18NFormat("maintenance-info-when-category"),
            mapping={"category": F["item"].category_id.name},
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-name"),
            mapping={"name": F["item"].name},
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-equipment"),
            mapping={"equipment": F["item"].equipment_id.name},
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-created"),
            mapping={"created": F["item"].employee_id.name},
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-request-date"),
            mapping={"request_date": F["item"].request_date},
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-user"),
            mapping={"user": F["item"].user_id.name},
        ),
        items="maintenance",
    ),
    Row(
        Select(
            text=I18NFormat("accept-button"),
            id="accept_maintenance",
            items="maintenance",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=accept_maintenance,
        ),
        Select(
            text=I18NFormat("forward-button"),
            id="forward_maintenance",
            items="maintenance",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=forward_maintenance,
        ),
        Select(
            text=I18NFormat("close-button"),
            id="close_maintenance",
            items="maintenance",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=close_maintenance,
        ),
    ),
    Row(
        Back(text=I18NFormat("back-button")),
        MAIN_MENU_BTN,
    ),
    getter=_maintenance_info,
    state=DialogSG.MAINTENANCE_INFO,
)
