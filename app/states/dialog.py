from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const


class DialogSG(StatesGroup):
    MAIN = State()
    EQUIPMENTS_PAGER = State()
    MAINTENANCE_PAGER = State()


MAIN_MENU_BTN = SwitchTo(Const("Main menu"), id="main", state=DialogSG.MAIN)
