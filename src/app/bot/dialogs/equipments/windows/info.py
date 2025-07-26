from aiogram import F
from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo
from aiogram_dialog.widgets.text import List

from app.bot.dialogs.equipments.getters import equipment_getter
from app.bot.states.dialog import (
    EquipmentsMenuSG,
    MainMenuSG,
    MaintenancesMenuSG,
)
from app.bot.utils.i18n_format import I18NFormat, Transformer

window = Window(
    I18NFormat("equipment-info-title"),
    List(
        Transformer(
            I18NFormat("equipment-info"),
            {
                "category": F["item"].category_id.name,
                "name": F["item"].name,
                "serial_no": F["item"].serial_no,
                "user": F["item"].technician_user_id.name,
            },
        ),
        items="equipment",
    ),
    Row(
        SwitchTo(
            text=I18NFormat("maintenances-show-button"),
            id="info_maintenance",
            state=MaintenancesMenuSG.MAINTENANCE_PAGER,
        ),
    ),
    Row(
        Row(
            SwitchTo(
                text=I18NFormat("back-button"),
                id="equipments",
                state=EquipmentsMenuSG.EQUIPMENTS_PAGER,
            ),
            Start(
                I18NFormat("menu-button"),
                id="main",
                state=MainMenuSG.MAIN,
                mode=StartMode.RESET_STACK,
            ),
        ),
    ),
    getter=equipment_getter,
    state=EquipmentsMenuSG.EQUIPMENT_INFO,
)
