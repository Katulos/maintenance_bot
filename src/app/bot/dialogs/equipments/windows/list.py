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

from app.bot.states.dialog import EquipmentsMenuSG, MainMenuSG
from app.bot.utils.i18n_format import I18NFormat
from app.core.infrastructure.services.odoo import OdooService

_PAGE_SIZE = settings.app.pagination_size


async def _equipments_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: OdooService,
    **kwargs: Any,
) -> dict[str, Any]:
    current_page = await dialog_manager.find("scroll_equipments").get_page()

    offset = current_page * _PAGE_SIZE

    equipment_count = await odoo.fetch_user_equipments_count(
        event_from_user.id,
    )

    if not equipment_count:
        equipment_count = 0

    equipments = await odoo.fetch_user_equipments(
        event_from_user.id,
        limit=_PAGE_SIZE,
        offset=offset,
    )

    if not equipments:
        equipments = []

    pages = equipment_count // _PAGE_SIZE + bool(equipment_count % _PAGE_SIZE)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "equipments": equipments,
    }


window = Window(
    I18NFormat("equipments-title", when=F["equipments"].len() > 0),
    I18NFormat("no-entries-title", when=~F["equipments"].len() > 0),
    Group(
        Select(
            Format("{item[0].name}"),
            id="s_equipments",
            items="equipments",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=equipment_info,
        ),
        width=1,
        when=F["equipments"].len() > 0,
    ),
    StubScroll(id="scroll_equipments", pages="pages"),
    Row(
        PrevPage(
            scroll="scroll_equipments",
            text=Format("◀️"),
        ),
        CurrentPage(
            scroll="scroll_equipments",
            text=Format("{current_page1}/{pages}"),
        ),
        NextPage(
            scroll="scroll_equipments",
            text=Format("▶️"),
        ),
        when=F["equipments"].len() > _PAGE_SIZE,
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
    getter=_equipments_getter,
    state=EquipmentsMenuSG.EQUIPMENTS_PAGER,
)
