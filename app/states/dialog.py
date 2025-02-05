from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.widgets.kbd import SwitchTo

from ..utils.i18n_format import I18NFormat


class DialogSG(StatesGroup):
    MAIN = State()
    EQUIPMENTS_PAGER = State()
    MAINTENANCE_PAGER = State()


MAIN_MENU_BTN = SwitchTo(
    I18NFormat("menu-button"),
    id="main",
    state=DialogSG.MAIN,
)
