from __future__ import annotations

from typing import Any

import structlog
from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Row, Select, SwitchTo
from aiogram_dialog.widgets.text import List

from ...handlers.user.maintenance import (
    close_maintenance,
    forward_maintenance,
)
from ...services.odoo import OdooService

# from ...services.odoo import fetch_maintenance
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat, Transformer


async def _maintenance_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    aiogram_session_logger: structlog.typing.FilteringBoundLogger,
    **kwargs: Any,
) -> dict[str, Any]:
    maintenance_id = dialog_manager.dialog_data.get("maintenance_id")
    maintenance = await odoo.fetch_maintenance(maintenance_id)
    return {"maintenance": maintenance}


window = Window(
    List(
        Transformer(
            I18NFormat("maintenance-info-when-category"),
            mapping={"category": F["item"].category_id.name},
            when=F["item"].category_id,
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
            when=F["item"].employee_id,
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-request-date"),
            mapping={
                "request_date": F["item"].create_date,
            },  # TODO: use timezone F["item"].env.context.tz
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-user"),
            mapping={"user": F["item"].user_id.name},
            when=F["item"].user_id,
        ),
        items="maintenance",
    ),
    Row(
        Select(
            text=I18NFormat("complete-button"),
            id="close_maintenance",
            items="maintenance",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=close_maintenance,
        ),
        Select(
            text=I18NFormat("forward-button"),
            id="forward_maintenance",
            items="maintenance",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=forward_maintenance,
        ),
    ),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=DialogSG.MAINTENANCE_PAGER,
        ),
        MAIN_MENU_BTN,
    ),
    getter=_maintenance_getter,
    state=DialogSG.MAINTENANCE_INFO,
)
