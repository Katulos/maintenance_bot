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

from app.bot.dialogs.maintenances.getters import (
    maintenance_requests_getter,
)
from app.bot.handlers.maintenances import maintenance_info_switch
from app.bot.states.dialog import MainMenuSG, MaintenancesMenuSG
from app.bot.utils.i18n_format import I18NFormat

_PAGE_SIZE = 5

window = Window(
    I18NFormat(
        "maintenances-requests-title",
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
    getter=maintenance_requests_getter,
    state=MaintenancesMenuSG.MAINTENANCE_PAGER,
)
