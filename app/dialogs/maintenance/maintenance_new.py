from __future__ import annotations

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Row, SwitchTo

from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat

window = Window(
    I18NFormat("maintenance-new-request-title"),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="new_maintenance",
            state=DialogSG.MAIN,
        ),
        MAIN_MENU_BTN,
    ),
    state=DialogSG.MAINTENANCE_NEW,
)
