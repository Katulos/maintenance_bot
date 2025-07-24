from typing import Any

import pytz
from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Select, Start, SwitchTo
from aiogram_dialog.widgets.text import List

from app.bot.states.dialog import MainMenuSG
from app.bot.utils.i18n_format import I18NFormat, Transformer
from app.core.infrastructure.services.odoo import OdooService


async def _maintenance_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    **kwargs: Any,
) -> dict[str, Any]:
    maintenance_id = dialog_manager.dialog_data.get("maintenance_id")
    if not maintenance_id:
        return {"maintenance": None}
    maintenance = await odoo.fetch_maintenance(maintenance_id)
    if maintenance and maintenance.create_date:
        tz = maintenance.env.context.get("tz", "UTC")
        maintenance.create_date = maintenance.create_date.replace(
            tzinfo=pytz.utc,
        ).astimezone(pytz.timezone(tz))
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
        when=F["item"].equipment_id,
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-created"),
            mapping={"created": F["item"].create_uid.name},
        ),
        items="maintenance",
    ),
    List(
        Transformer(
            I18NFormat("maintenance-info-when-request-date"),
            mapping={"request_date": F["item"].create_date},
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
            on_click=maintenance_close_switch,
        ),
        Select(
            text=I18NFormat("forward-button"),
            id="forward_maintenance",
            items="maintenance",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=maintenance_forward_switch,
        ),
    ),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=MaintenanceMenuSG.MAINTENANCE_PAGER,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    getter=_maintenance_getter,
    state=MaintenanceMenuSG.MAINTENANCE_INFO,
)
