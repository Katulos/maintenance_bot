from __future__ import annotations

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const

from ..states import DialogSG
from ..utils.i18n_format import I18NFormat

window = Window(
    # Menu title
    Const("Please, select an option:"),
    # Menu buttons
    SwitchTo(
        Const(text=I18NFormat("Equipments")),
        id="equipments",
        state=DialogSG.EQUIPMENTS_PAGER,
    ),
    SwitchTo(
        Const(text=I18NFormat("Maintenance Requests")),
        id="maintenance_requests",
        state=DialogSG.MAINTENANCE_PAGER,
    ),
    Cancel(text=I18NFormat("Cancel")),
    state=DialogSG.MAIN,
)
