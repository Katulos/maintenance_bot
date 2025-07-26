from __future__ import annotations

from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Start

from app.bot.handlers.cancel import close_button_handler
from app.bot.states.dialog import (
    EquipmentsMenuSG,
    MainMenuSG,
    MaintenancesMenuSG,
)
from app.bot.utils.i18n_format import I18NFormat

window = Window(
    # Menu title
    I18NFormat("select-an-option-title"),
    # Menu buttons
    Start(
        I18NFormat("equipments-title"),
        id="equipments",
        state=EquipmentsMenuSG.EQUIPMENTS_PAGER,
        mode=StartMode.RESET_STACK,
    ),
    Start(
        I18NFormat("maintenances-requests-title"),
        id="maintenance_requests",
        state=MaintenancesMenuSG.MAINTENANCE_PAGER,
        mode=StartMode.RESET_STACK,
    ),
    Start(
        I18NFormat("maintenances-new-request-title"),
        id="maintenance_new_request",
        state=MaintenancesMenuSG.MAINTENANCE_NEW,
        mode=StartMode.RESET_STACK,
    ),
    Button(
        id="cancel",
        text=I18NFormat("cancel-button"),
        on_click=close_button_handler,
    ),
    # Cancel(
    #     text=I18NFormat("cancel-button"),
    #     show_mode=ShowMode.DELETE_AND_SEND,
    # ),
    state=MainMenuSG.MAIN,
)
