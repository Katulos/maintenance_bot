from typing import Any

from aiogram import F
from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import (
    CurrentPage,
    Group,
    NextPage,
    PrevPage,
    Row,
    Select,
    Start,
    StubScroll,
)
from aiogram_dialog.widgets.text import Format

from app.bot.states.dialog import MainMenuSG, MaintenanceMenuSG
from app.bot.utils.i18n_format import I18NFormat
from app.core.infrastructure.services.odoo import OdooService

_PAGE_SIZE = settings.app.pagination_size


async def _maintenance_requests_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    **kwargs: Any,
) -> dict[str, Any]:
    current_page = await dialog_manager.find(
        "scroll_maintenance_requests",
    ).get_page()

    offset = current_page * _PAGE_SIZE

    request_count = await odoo.fetch_user_maintenances_count(
        event_from_user.id,
    )

    if not request_count:
        request_count = 0

    requests = await odoo.fetch_user_maintenances(
        event_from_user.id,
        limit=_PAGE_SIZE,
        offset=offset,
    )

    if not requests:
        requests = []

    pages = request_count // _PAGE_SIZE + bool(request_count % _PAGE_SIZE)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "maintenance_requests": requests,
    }


window = Window(
    I18NFormat(
        "maintenance-requests-title",
        when=F["maintenance_requests"].len() > 0,
    ),
    I18NFormat("no-entries-title", when=~F["maintenance_requests"].len() > 0),
    Group(
        Select(
            Format("{item[0].name}"),
            id="s_maintenance_requests",
            items="maintenance_requests",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=maintenance_info_switch,
        ),
        width=1,
        when=F["maintenance_requests"].len() > 0,
    ),
    StubScroll(id="scroll_maintenance_requests", pages="pages"),
    Row(
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
        when=F["maintenance_requests"].len() > _PAGE_SIZE,
    ),
    Row(
        Start(
            text=I18NFormat("back-button"),
            id="main_menu",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    getter=_maintenance_requests_getter,
    state=MaintenanceMenuSG.MAINTENANCE_PAGER,
)
