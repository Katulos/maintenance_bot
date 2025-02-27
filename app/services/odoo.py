from __future__ import annotations

from typing import Any

import odoorpc

from ..utils import logging

_logger = logging.setup_logger().bind(type="odoo")


class OdooService(odoorpc.ODOO):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def fetch_employee(
        self,
        user_id: int,
    ) -> odoorpc.models.Model | None:
        try:
            hr = self.env["hr.employee"]
            employee_id = hr.search([("telegram_id", "=", user_id)], limit=1)
            employee = hr.browse(employee_id)
            return employee
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_employees(
        self,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        try:
            hr = self.env["hr.employee"]
            employee_ids = hr.search([], limit=limit, offset=offset)
            employees = hr.browse(employee_ids)
            return employees
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_employees_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            hr = self.env["hr.employee"]
            count = hr.search_count([("telegram_id", "=", user_id)])
            if isinstance(count, int):
                return count
            else:
                _logger.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_equipment(
        self,
        equipment_id: int,
    ) -> odoorpc.models.Model | None:
        try:
            equipment = self.env["maintenance.equipment"].browse(equipment_id)
            return equipment
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_equipments(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        try:
            equipment = self.env["maintenance.equipment"]
            equipment_ids = equipment.search(
                [("employee_id.telegram_id", "=", user_id)],
                limit=limit,
                offset=offset,
            )
            equipments = equipment.browse(equipment_ids)
            return equipments
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_equipments_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            equipment = self.env["maintenance.equipment"]
            count = equipment.search_count(
                [("employee_id.telegram_id", "=", user_id)],
            )
            if isinstance(count, int):
                return count
            else:
                _logger.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_maintenance(
        self,
        maintenance_id: int,
    ) -> odoorpc.models.Model | None:
        try:
            maintenance = self.env["maintenance.request"].browse(
                maintenance_id,
            )
            return maintenance
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_maintenances(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        try:
            request = self.env["maintenance.request"]
            request_ids = request.search(
                [("equipment_id.employee_id.telegram_id", "=", user_id)],
                limit=limit,
                offset=offset,
            )
            requests = request.browse(request_ids)
            return requests
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None

    async def fetch_maintenances_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            request = self.env["maintenance.request"]
            count = request.search_count(
                [("equipment_id.employee_id.telegram_id", "=", user_id)],
            )
            if isinstance(count, int):
                return count
            else:
                _logger.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except odoorpc.error.RPCError as e:
            _logger.error(e)
            return None
