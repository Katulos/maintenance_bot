from __future__ import annotations

import odoorpc
from aiogram.types import User

from .. import utils
from ..config import settings

logger = utils.logging.setup_logger().bind(type="odoo")


async def fetch_employee(user: User) -> odoorpc.models.Model | None:
    odoo: odoorpc.ODOO = await _login(user)
    if not odoo:
        return None
    try:
        hr = odoo.env["hr.employee"]
        employee_id = hr.search([("telegram_id", "=", user.id)], limit=1)
        employee = hr.browse(employee_id)
        return employee
    except odoorpc.error.RPCError as e:
        logger.error(e)
        return None


async def fetch_equipment(
    user: User,
    equipment_id: int,
) -> odoorpc.models.Model | None:
    odoo: odoorpc.ODOO = await _login(user)
    try:
        equipment = odoo.env["maintenance.equipment"].browse(equipment_id)
        return equipment
    except odoorpc.error.RPCError as e:
        logger.error(e)
        return None


async def fetch_equipments(user: User) -> odoorpc.models.Model | None:
    odoo: odoorpc.ODOO = await _login(user)
    try:
        equipment = odoo.env["maintenance.equipment"]
        equipment_ids = equipment.search(
            [("employee_id.telegram_id", "=", user.id)],
        )
        equipments = equipment.browse(equipment_ids)
        return equipments
    except odoorpc.error.RPCError as e:
        logger.error(e)
        return None


async def fetch_maintenance(
    user: User,
    maintenance_id: int,
) -> odoorpc.models.Model | None:
    odoo: odoorpc.ODOO = await _login(user)
    try:
        maintenance = odoo.env["maintenance.request"].browse(maintenance_id)
        return maintenance
    except odoorpc.error.RPCError as e:
        logger.error(e)
        return None


async def fetch_maintenances(user: User) -> odoorpc.models.Model | None:
    odoo: odoorpc.ODOO = await _login(user)
    try:
        request = odoo.env["maintenance.request"]
        request_ids = request.search(
            [("equipment_id.employee_id.telegram_id", "=", user.id)],
        )
        requests = request.browse(request_ids)
        return requests
    except odoorpc.error.RPCError as e:
        logger.error(e)
        return None


async def _login(user: User) -> odoorpc.ODOO | bool:
    odoo = odoorpc.ODOO(
        host=settings.odoo.host,
        port=settings.odoo.port,
        protocol=settings.odoo.protocol,
    )

    if user.id not in settings.odoo.users:
        logger.error(
            f"User {user.id} is missing from the configuration file",
            type="business",
        )
        return False

    try:
        user_settings = settings.odoo.users[user.id]
        odoo.login(
            db=settings.odoo.database,
            login=user_settings.username,
            password=user_settings.password,
        )

    except (odoorpc.error.RPCError, KeyError) as e:
        logger.error(f"Failed to login to Odoo: {e}")
        return False
    return odoo
