from __future__ import annotations

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Row, SwitchTo

from ...states import MAIN_MENU_BTN
from ...states.dialog import MaintenanceSG
from ...utils.i18n_format import I18NFormat

window = Window(
    I18NFormat("maintenance-close-text"),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=MaintenanceSG.MAINTENANCE_INFO,
        ),
        MAIN_MENU_BTN,
    ),
    state=MaintenanceSG.MAINTENANCE_CLOSE,
)
