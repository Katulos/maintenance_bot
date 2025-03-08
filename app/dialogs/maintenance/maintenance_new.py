from __future__ import annotations

from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Start

from ...states import MAIN_MENU_BTN
from ...states.dialog import MaintenanceSG, MenuSG
from ...utils.i18n_format import I18NFormat

window = Window(
    I18NFormat("maintenance-new-request-title"),
    Row(
        Start(
            text=I18NFormat("back-button"),
            id="new_maintenance",
            state=MenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        MAIN_MENU_BTN,
    ),
    state=MaintenanceSG.MAINTENANCE_NEW,
)
