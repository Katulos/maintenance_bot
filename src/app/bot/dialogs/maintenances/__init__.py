from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram_dialog import (
    Dialog,
)

from app.bot.dialogs.maintenances.windows import (
    accept,
    close,
    forward,
    info,
    list,
    new,
)


def setup(router: Router) -> None:
    router.include_router(
        Dialog(
            accept.window,
            close.window,
            forward.window,
            info.window,
            list.window,
            new.window,
        ),
    )
