from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram_dialog import (
    Dialog,
)

from app.bot.dialogs.equipments.windows import (
    info,
    list,
)


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    equipment_router = router.include_router(
        Router(name=__name__ + ".equipments"),
    )
    equipment_dialog = Dialog(
        list.window,
        info.window,
    )

    equipment_router.include_router(equipment_dialog)
    return router
