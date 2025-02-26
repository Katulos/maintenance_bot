from __future__ import annotations

from aiogram_dialog import ShowMode, Window
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo

from ..states import DialogSG
from ..utils.i18n_format import I18NFormat

window = Window(
    # Menu title
    I18NFormat("select-an-option-title"),
    # Menu buttons
    SwitchTo(
        I18NFormat("equipments-title"),
        id="equipments",
        state=DialogSG.EQUIPMENTS_PAGER,
    ),
    SwitchTo(
        I18NFormat("maintenance-requests-title"),
        id="maintenance_requests",
        state=DialogSG.MAINTENANCE_PAGER,
    ),
    SwitchTo(
        I18NFormat("maintenance-new-request-title"),
        id="maintenance_new_request",
        state=DialogSG.MAINTENANCE_NEW,
    ),
    Cancel(
        text=I18NFormat("cancel-button"),
        show_mode=ShowMode.DELETE_AND_SEND,
    ),
    state=DialogSG.MAIN,
)
