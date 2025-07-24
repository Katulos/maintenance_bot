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
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format

from app.bot.states.dialog import MainMenuSG
from app.bot.utils.i18n_format import I18NFormat
from app.core.infrastructure.services.odoo import OdooService

_PAGE_SIZE = settings.app.pagination_size


async def _users_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    **kwargs: Any,
) -> dict[str, Any]:
    current_page = await dialog_manager.find("scroll_users").get_page()

    offset = current_page * _PAGE_SIZE

    users_count = await odoo.fetch_users_count()

    if not users_count:
        users_count = 0

    users = await odoo.fetch_users(
        limit=_PAGE_SIZE,
        offset=offset,
    )

    if not users:
        users = []

    pages = users_count // _PAGE_SIZE + bool(users_count % _PAGE_SIZE)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "users": users,
    }


window = Window(
    I18NFormat("maintenance-forward-text"),
    Group(
        Select(
            Format("{item[name]}"),
            id="s_user",
            items="users",
            item_id_getter=lambda x: x["id"],
            type_factory=int,
            on_click=maintenance_forward_done,
        ),
        width=1,
    ),
    StubScroll(id="scroll_users", pages="pages"),
    Row(
        PrevPage(scroll="scroll_users", text=Format("◀️")),
        CurrentPage(
            scroll="scroll_users",
            text=Format("{current_page1}/{pages}"),
        ),
        NextPage(scroll="scroll_users", text=Format("▶️")),
        when=F["users"].len() > _PAGE_SIZE,
    ),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=MaintenanceMenuSG.MAINTENANCE_INFO,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    getter=_users_getter,
    state=MaintenanceMenuSG.MAINTENANCE_FORWARD,
)
