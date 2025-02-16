from __future__ import annotations

from aiogram_dialog import ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, Row

from ..states import MAIN_MENU_BTN, DialogSG
from ..utils.i18n_format import I18NFormat

window = Window(
    I18NFormat("equipment-info-title"),
    Row(
        Back(text=I18NFormat("back-button")),
        MAIN_MENU_BTN,
        Cancel(
            text=I18NFormat("close-button"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
    ),
    state=DialogSG.EQUIPMENT_INFO,
)
