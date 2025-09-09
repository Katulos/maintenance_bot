from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from app.bot.dialogs import start


def setup(dp: Dispatcher) -> None:
    start.setup(dp)
    # equipments.setup(dp)
    # maintenances.setup(dp)
    setup_dialogs(dp)
