from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo

from app.bot.states.dialog import MainMenuSG, MaintenanceMenuSG
from app.bot.utils.i18n_format import I18NFormat

window = Window(
    I18NFormat("maintenance-close-text"),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=MaintenanceMenuSG.MAINTENANCE_INFO,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    state=MaintenanceMenuSG.MAINTENANCE_CLOSE,
)
