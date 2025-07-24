from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram_dialog import (
    Dialog,
)

from app.bot.dialogs.maintenance.windows import (
    accept,
    close,
    forward,
    info,
    list,
    new,
)


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    equipment_router = router.include_router(
        Router(name=__name__ + ".maintenance"),
    )
    equipment_dialog = Dialog(
        accept.window,
        close.window,
        forward.window,
        info.window,
        list.window,
        new.window,
    )

    equipment_router.include_router(equipment_dialog)
    return router
