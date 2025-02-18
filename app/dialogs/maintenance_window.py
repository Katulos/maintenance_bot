from __future__ import annotations

import odoorpc
import structlog
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    CurrentPage,
    FirstPage,
    LastPage,
    NextPage,
    PrevPage,
    Row,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Format

from ..config import settings
from ..handlers.user.maintenance import maintenance_info
from ..states import MAIN_MENU_BTN, DialogSG
from ..utils.i18n_format import I18NFormat


async def _maintenance_requests_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo_logger: structlog.typing.FilteringBoundLogger,
    **kwargs,
):
    try:
        odoo: odoorpc.ODOO = dialog_manager.middleware_data.get("odoo")
        user_id = event_from_user.id

        if user_id not in settings.odoo.users:
            odoo_logger.error("User is missing from the configuration file")
            return {"equipments": []}

        odoo.login(
            db=settings.odoo.database,
            login=settings.odoo.users[user_id].username,
            password=settings.odoo.users[user_id].password,
        )

        request = odoo.env["maintenance.request"]
        request_ids = request.search(
            [("equipment_id.employee_id.telegram_id", "=", user_id)],
        )
        requests = request.browse(request_ids)

        return {"maintenance_requests": requests}

    except odoorpc.error.RPCError as e:
        odoo_logger.error(e)
        return {"maintenance_requests": []}


window = Window(
    I18NFormat("maintenance-requests-title"),
    ScrollingGroup(
        Select(
            Format("{item[0].name}"),
            id="s_maintenance_requests",
            items="maintenance_requests",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=maintenance_info,
        ),
        width=2,
        height=5,
        hide_pager=True,
        id="scroll_maintenance_requests",
    ),
    Row(
        FirstPage(
            scroll="scroll_maintenance_requests",
            text=Format("⏮️ {target_page1}"),
        ),
        PrevPage(
            scroll="scroll_maintenance_requests",
            text=Format("◀️"),
        ),
        CurrentPage(
            scroll="scroll_maintenance_requests",
            text=Format("{current_page1}"),
        ),
        NextPage(
            scroll="scroll_maintenance_requests",
            text=Format("▶️"),
        ),
        LastPage(
            scroll="scroll_maintenance_requests",
            text=Format("{target_page1} ⏭️"),
        ),
    ),
    Row(
        PrevPage(scroll="scroll_maintenance_requests"),
        NextPage(scroll="scroll_maintenance_requests"),
        MAIN_MENU_BTN,
        Cancel(
            text=I18NFormat("close-button"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
    ),
    getter=_maintenance_requests_getter,
    state=DialogSG.MAINTENANCE_PAGER,
)
