from __future__ import annotations

from typing import Any

import structlog
from aiogram.types import User
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    CurrentPage,
    Group,
    NextPage,
    PrevPage,
    Row,
    Select,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format

from ...config import settings
from ...handlers.user.maintenance import maintenance_forward_done
from ...services.odoo import OdooService
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
    current_page = await dialog_manager.find("scroll_employee").get_page()

    offset = current_page * _PAGE_SIZE

    employee_count = await odoo.fetch_employees_count(event_from_user.id)

    if not employee_count:
        employee_count = 0

    employees = await odoo.fetch_employees(
        limit=_PAGE_SIZE,
        offset=offset,
    )

    if not employees:
        employees = []

    pages = employee_count // _PAGE_SIZE + bool(employee_count % _PAGE_SIZE)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "employees": employees,
    }


window = Window(
    I18NFormat("maintenance-forward-text"),
    Group(
        Select(
            Format("{item[0].name}"),
            id="s_employee",
            items="employees",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=maintenance_forward_done,
        ),
        width=1,
    ),
    StubScroll(id="scroll_employee", pages="pages"),
    Row(
        PrevPage(scroll="scroll_employee", text=Format("◀️")),
        CurrentPage(
            scroll="scroll_employee",
            text=Format("{current_page1}/{pages}"),
        ),
        NextPage(scroll="scroll_employee", text=Format("▶️")),
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
