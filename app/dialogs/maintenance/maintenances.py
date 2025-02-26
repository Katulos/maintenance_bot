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
from ...handlers.user.maintenance import maintenance_info
from ...services.odoo import OdooService

# from ...services.odoo import fetch_maintenances
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat

_PAGE_SIZE = settings.app.pagination_size


async def _maintenance_requests_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    aiogram_session_logger: structlog.typing.FilteringBoundLogger,
    **kwargs: Any,
) -> dict[str, Any]:
    requests = await odoo.fetch_maintenances(event_from_user.id)
    if requests is None:
        requests = []
    return {
        "maintenance_requests": requests,
        "show_scroll": len(requests) > _PAGE_SIZE,
        "fast_scroll": len(requests) > _PAGE_SIZE * 2,
    }


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
        width=1,
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
            text=Format("{current_page1}/{pages}"),
        ),
        NextPage(
            scroll="scroll_maintenance_requests",
            text=Format("▶️"),
        ),
        LastPage(
            scroll="scroll_maintenance_requests",
            text=Format("{target_page1} ⏭️"),
        ),
        when=F["show_scroll"],
    ),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="main_menu",
            state=DialogSG.MAIN,
        ),
        MAIN_MENU_BTN,
    ),
    getter=_maintenance_requests_getter,
    state=DialogSG.MAINTENANCE_PAGER,
)
