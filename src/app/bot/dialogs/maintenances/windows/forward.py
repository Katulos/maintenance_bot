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
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format

from app.bot.dialogs.maintenances.getters import users_getter
from app.bot.handlers.maintenances import maintenance_forward_done
from app.bot.states.dialog import MainMenuSG, MaintenancesMenuSG
from app.bot.utils.i18n_format import I18NFormat

_PAGE_SIZE=5

window = Window(
    I18NFormat("maintenances-forward-text"),
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
            state=MaintenancesMenuSG.MAINTENANCE_INFO,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    getter=users_getter,
    state=MaintenancesMenuSG.MAINTENANCE_FORWARD,
)
