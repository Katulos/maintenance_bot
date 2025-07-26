from aiogram import F
from aiogram_dialog import StartMode, Window
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

from app.bot.dialogs.equipments.getters import equipments_getter
from app.bot.handlers.equipments import equipment_info
from app.bot.states.dialog import EquipmentsMenuSG, MainMenuSG
from app.bot.utils.i18n_format import I18NFormat

_PAGE_SIZE=5


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
    getter=equipments_getter,
    state=EquipmentsMenuSG.EQUIPMENTS_PAGER,
)
