from typing import Any

import pytz
from aiogram.types import User
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.config.main import Config
from app.core.infrastructure.odoo import Odoo

@inject
async def users_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: FromDishka[Odoo],
    config: FromDishka[Config],
    **kwargs: Any,
) -> dict[str, Any]:
    page_size = config.bot.page_size

    current_page = await dialog_manager.find("scroll_users").get_page()

    offset = current_page * page_size

    user_credentials = config.odoo.users[event_from_user.id]

    odoo.login(
        login=user_credentials.username,
        password=user_credentials.password,
        db=config.odoo.database,
    )

    users_count = await odoo.fetch_users_count()

    if not users_count:
        users_count = 0

    users = await odoo.fetch_users(
        limit=page_size,
        offset=offset,
    )

    if not users:
        users = []

    pages = users_count // page_size + bool(users_count % page_size)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "users": users,
    }


@inject
async def maintenance_requests_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: FromDishka[Odoo],
    config: FromDishka[Config],
    **kwargs: Any,
) -> dict[str, Any]:
    page_size = config.bot.page_size

    current_page = await dialog_manager.find(
        "scroll_maintenance_requests",
    ).get_page()

    offset = current_page * page_size

    user_credentials = config.odoo.users[event_from_user.id]

    odoo.login(
        login=user_credentials.username,
        password=user_credentials.password,
        db=config.odoo.database,
    )

    request_count = await odoo.fetch_user_maintenances_count(
        event_from_user.id,
    )

    if not request_count:
        request_count = 0

    requests = await odoo.fetch_user_maintenances(
        event_from_user.id,
        limit=page_size,
        offset=offset,
    )

    if not requests:
        requests = []

    pages = request_count // page_size + bool(request_count % page_size)

    return {
        "pages": pages,
        "current_page": current_page + 1,
        "maintenance_requests": requests,
    }


@inject
async def maintenance_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo: FromDishka[Odoo],
    config: FromDishka[Config],
    **kwargs: Any,
) -> dict[str, Any]:
    maintenance_id = dialog_manager.dialog_data.get("maintenance_id")
    if not maintenance_id:
        return {"maintenances": None}

    user_credentials = config.odoo.users[event_from_user.id]

    odoo.login(
        login=user_credentials.username,
        password=user_credentials.password,
        db=config.odoo.database,
    )

    maintenance = await odoo.fetch_maintenance(maintenance_id)
    if maintenance and maintenance.create_date:
        tz = maintenance.env.context.get("tz", "UTC")
        maintenance.create_date = maintenance.create_date.replace(
            tzinfo=pytz.utc,
        ).astimezone(pytz.timezone(tz))
    return {"maintenances": maintenance}
