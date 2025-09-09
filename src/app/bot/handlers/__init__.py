from aiogram import Dispatcher, F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent

from app.bot import dialogs
from app.bot.handlers import cancel, menu, start
from app.bot.handlers.errors import clear_unknown_intent, errors_handler


def setup(dp: Dispatcher) -> Router:
    router = Router(name=__name__)

    router.message.register(
        start.start_command,
        CommandStart(),
        F.chat.type == ChatType.PRIVATE,
    )

    router.message.register(
        cancel.cancel_command,
        Command(commands=["cancel"]),
        F.chat.type == ChatType.PRIVATE,
    )

    # router.message.register(
    #     equipments.equipments_list_command,
    #     Command(commands=["equipments", "eq"]),
    #     F.chat.type == ChatType.PRIVATE,
    # )
    #
    # router.message.register(
    #     maintenances.maintenances_list_command,
    #     Command(commands=["maintenances", "ma"]),
    #     F.chat.type == ChatType.PRIVATE,
    # )
    #
    # router.message.register(
    #     maintenances.maintenance_new_command,
    #     Command(commands=["new", "manew"]),
    #     F.chat.type == ChatType.PRIVATE,
    # )

    router.message.register(
        menu.menu_command,
        Command(commands=["menu"]),
        F.chat.type == ChatType.PRIVATE,
    )

    # Register error handlers
    dp.errors.register(
        clear_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        errors_handler,
    )
    #
    dp.include_router(router)
    #
    dialogs.setup(dp)
    return router
