from __future__ import annotations

from aiogram_dialog import ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Cancel, Start

from ..states.dialog import EquipmentsSG, MaintenanceSG, MenuSG
from ..utils.i18n_format import I18NFormat

window = Window(
    # Menu title
    I18NFormat("select-an-option-title"),
    # Menu buttons
    Start(
        I18NFormat("equipments-title"),
        id="equipments",
        state=EquipmentsSG.EQUIPMENTS_PAGER,
        mode=StartMode.RESET_STACK,
    ),
    Start(
        I18NFormat("maintenance-requests-title"),
        id="maintenance_requests",
        state=MaintenanceSG.MAINTENANCE_PAGER,
        mode=StartMode.RESET_STACK,
    ),
    Start(
        I18NFormat("maintenance-new-request-title"),
        id="maintenance_new_request",
        state=MaintenanceSG.MAINTENANCE_NEW,
        mode=StartMode.RESET_STACK,
    ),
    Cancel(
        text=I18NFormat("cancel-button"),
        show_mode=ShowMode.DELETE_AND_SEND,
    ),
    state=MenuSG.MAIN,
)
