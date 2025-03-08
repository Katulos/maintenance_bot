from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start

from ..utils.i18n_format import I18NFormat


class MaintenanceSG(StatesGroup):
    MAINTENANCE_ACCEPT = State()
    MAINTENANCE_CLOSE = State()
    MAINTENANCE_FORWARD = State()
    MAINTENANCE_INFO = State()
    MAINTENANCE_NEW = State()
    MAINTENANCE_PAGER = State()


class EquipmentsSG(StatesGroup):
    EQUIPMENTS_PAGER = State()
    EQUIPMENT_INFO = State()


class MenuSG(StatesGroup):
    MAIN = State()


MAIN_MENU_BTN = Start(
    I18NFormat("menu-button"),
    id="main",
    state=MenuSG.MAIN,
    mode=StartMode.RESET_STACK,
)
