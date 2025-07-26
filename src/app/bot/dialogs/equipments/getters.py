from typing import Any

from aiogram.types import User
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.config.main import Config
from app.core.infrastructure.odoo import Odoo


@inject
async def equipment_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: FromDishka[Odoo],
    config: FromDishka[Config],
    **kwargs: Any,
) -> dict[str, Any]:
    equipment_id = dialog_manager.dialog_data.get("equipment_id")

    user_credentials = config.odoo.users[event_from_user.id]

    odoo.login(
        login=user_credentials.username,
        password=user_credentials.password,
        db=config.odoo.database,
    )
    equipment = await odoo.fetch_equipment(equipment_id)
    return {"equipment": equipment}


@inject
async def equipments_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: FromDishka[Odoo],
    config: FromDishka[Config],
    **kwargs: Any,
) -> dict[str, Any]:
    page_size = config.bot.page_size

    current_page = await dialog_manager.find("scroll_equipments").get_page()

    offset = current_page * page_size

    user_credentials = config.odoo.users[event_from_user.id]

    odoo.login(
        login=user_credentials.username,
        password=user_credentials.password,
        db=config.odoo.database,
    )

    equipment_count = await odoo.fetch_user_equipments_count(
        event_from_user.id,
    )

    if not equipment_count:
        equipment_count = 0

    equipments = await odoo.fetch_user_equipments(
        event_from_user.id,
        limit=page_size,
        offset=offset,
    )

    if not equipments:
        equipments = []

    pages = equipment_count // page_size + bool(equipment_count % page_size)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "equipments": equipments,
    }
