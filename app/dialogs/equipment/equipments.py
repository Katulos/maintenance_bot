from __future__ import annotations

from typing import Any

import structlog
from aiogram import F
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

from ...config import settings
from ...handlers.user.equipments import equipment_info
from ...services.odoo import fetch_equipments
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat

_PAGE_SIZE = settings.app.pagination_size


async def _equipments_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    aiogram_session_logger: structlog.typing.FilteringBoundLogger,
    **kwargs: Any,
) -> dict[str, Any]:
    equipments = await fetch_equipments(event_from_user)
    if equipments is None:
        equipments = []
    return {
        "equipments": equipments,
        "show_scroll": len(equipments) > _PAGE_SIZE,
        "fast_scroll": len(equipments) > _PAGE_SIZE * 2,
    }


window = Window(
    I18NFormat("equipments-title"),
    ScrollingGroup(
        Select(
            Format("{item[0].name}"),
            id="s_equipments",
            items="equipments",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=equipment_info,
        ),
        width=1,
        height=_PAGE_SIZE,
        hide_pager=True,
        id="scroll_equipments",
    ),
    Row(
        FirstPage(
            scroll="scroll_equipments",
            text=Format("⏮️ {target_page1}"),
        ),
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
        LastPage(
            scroll="scroll_equipments",
            text=Format("{target_page1} ⏭️"),
        ),
        when=F["show_scroll"],
    ),
    Row(
        MAIN_MENU_BTN,
        Cancel(
            text=I18NFormat("close-button"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
    ),
    getter=_equipments_getter,
    state=DialogSG.EQUIPMENTS_PAGER,
)
