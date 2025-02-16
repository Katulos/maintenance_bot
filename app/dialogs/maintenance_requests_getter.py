from __future__ import annotations

import odoorpc
import structlog
from aiogram.types import User
from aiogram_dialog import DialogManager

from ..config import settings


async def maintenance_requests_getter(
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

        request = odoo.env["maintenance.request"]
        request_ids = request.search(
            [("equipment_id.employee_id.telegram_id", "=", user_id)],
        )
        requests = request.browse(request_ids)

        return {
            "maintenance_requests": [(eq.name, eq) for eq in requests],
        }

    except odoorpc.error.RPCError as e:
        odoo_logger.error(e)
        return {"maintenance_requests": []}


# async def maintenance_requests_getter(**_kwargs):
#     return {
#         "maintenance_requests": [
#             (f"Maintenance Requests {i}", i) for i in range(1, 300)
#         ],
#     }
