from __future__ import annotations

from typing import Any

import structlog
from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    CurrentPage,
    FirstPage,
    LastPage,
    NextPage,
    PrevPage,
    Row,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format

from ...config import settings
from ...services.odoo import OdooService

# from ...services.odoo import fetch_employees
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat

_PAGE_SIZE = settings.app.pagination_size


async def _employee_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    aiogram_session_logger: structlog.typing.FilteringBoundLogger,
    **kwargs: Any,
) -> dict[str, Any]:
    employee = await odoo.fetch_employees()
    if employee is None:
        employee = []
    return {
        "employee": employee,
        "show_scroll": len(employee) > _PAGE_SIZE,
        "fast_scroll": len(employee) > _PAGE_SIZE * 2,
    }


window = Window(
    I18NFormat("maintenance-forward-text"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_employee",
            items="employee",
            item_id_getter=lambda x: x.id,
            type_factory=int,
        ),
        width=1,
        height=_PAGE_SIZE,
        hide_pager=True,
        id="scroll_employee",
    ),
    Row(
        FirstPage(
            scroll="scroll_employee",
            text=Format("⏮️ {target_page1}"),
            when=F["data"]["fast_scroll"],
        ),
        PrevPage(scroll="scroll_employee"),
        CurrentPage(
            scroll="scroll_employee",
            text=Format("{current_page1}/{pages}"),
        ),
        NextPage(scroll="scroll_employee"),
        LastPage(
            scroll="scroll_employee",
            text=Format("{target_page1} ⏭️"),
            when=F["data"]["fast_scroll"],
        ),
        when=F["show_scroll"],
    ),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=DialogSG.MAINTENANCE_INFO,
        ),
        MAIN_MENU_BTN,
    ),
    getter=_employee_getter,
    state=DialogSG.MAINTENANCE_FORWARD,
)
