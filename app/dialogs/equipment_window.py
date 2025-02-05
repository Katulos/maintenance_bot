from __future__ import annotations

from operator import itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    CurrentPage,
    FirstPage,
    LastPage,
    Multiselect,
    NextPage,
    PrevPage,
    Row,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Format

from ..states import MAIN_MENU_BTN, DialogSG
from ..utils.i18n_format import I18NFormat
from .equipments_getter import equipments_getter

window = Window(
    I18NFormat("equipments-title"),
    ScrollingGroup(
        Multiselect(
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id="ms_equipments",
            items="equipments",
            item_id_getter=itemgetter(1),
        ),
        width=2,
        height=5,
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
            text=Format("{current_page1}"),
        ),
        NextPage(
            scroll="scroll_equipments",
            text=Format("▶️"),
        ),
        LastPage(
            scroll="scroll_equipments",
            text=Format("{target_page1} ⏭️"),
        ),
    ),
    Row(
        PrevPage(scroll="scroll_equipments"),
        NextPage(scroll="scroll_equipments"),
        MAIN_MENU_BTN,
        Cancel(text=I18NFormat("close-button")),
    ),
    getter=equipments_getter,
    state=DialogSG.EQUIPMENTS_PAGER,
)
