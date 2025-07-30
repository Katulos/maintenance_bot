from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo

from app.bot.states.dialog import MainMenuSG, MaintenancesMenuSG
from app.bot.utils.i18n_format import I18NFormat

window = Window(
    I18NFormat("maintenances-close-text"),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="maintenance_requests",
            state=MaintenancesMenuSG.MAINTENANCE_PAGER,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    state=MaintenancesMenuSG.MAINTENANCE_CLOSE,
)
