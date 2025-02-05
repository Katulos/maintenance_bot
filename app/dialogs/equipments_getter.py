from __future__ import annotations

import odoorpc
import structlog
from aiogram.types import User
from aiogram_dialog import DialogManager

from ..config import settings


async def equipments_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo_logger: structlog.typing.FilteringBoundLogger,
    **kwargs,
):
    try:
        odoo: odoorpc.ODOO = dialog_manager.middleware_data.get("odoo")
        user_id = event_from_user.id

        if user_id not in settings.odoo.users:
            odoo_logger.error("User is missing from the configuration file")
            return {"equipments": []}

        odoo.login(
            db=settings.odoo.database,
            login=settings.odoo.users[user_id].username,
            password=settings.odoo.users[user_id].password,
        )

        equipment = odoo.env["maintenance.equipment"]
        equipment_ids = equipment.search(
            [("employee_id.telegram_id", "=", user_id)],
        )
        equipments = equipment.browse(equipment_ids)

        return {
            "equipments": [(eq.name, eq) for eq in equipments],
        }

    except odoorpc.error.RPCError as e:
        odoo_logger.error(e)
        return {"equipments": []}
