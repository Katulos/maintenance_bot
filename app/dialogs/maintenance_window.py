from __future__ import annotations

from operator import itemgetter

from aiogram_dialog import ShowMode, Window
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

from ..handlers.user.maintenance import maintenance_info
from ..states import MAIN_MENU_BTN, DialogSG
from ..utils.i18n_format import I18NFormat
from .maintenance_requests_getter import maintenance_requests_getter

window = Window(
    I18NFormat("maintenance-requests-title"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_maintenance_requests",
            items="maintenance_requests",
            item_id_getter=itemgetter(1),
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
    getter=maintenance_requests_getter,
    state=DialogSG.MAINTENANCE_PAGER,
)
