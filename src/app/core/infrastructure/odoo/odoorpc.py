import logging
from typing import Any

import odoorpc
from dishka import AsyncContainer

from app.core.config.main import Config
from app.core.infrastructure.odoo.odoo import Odoo


class OdooRPC(Odoo):
    def __init__(
        self,
        container: AsyncContainer,
        config: Config,
    ) -> None:
        self.container = container
        self._odoo = odoorpc.ODOO(
            host=config.odoo.host,
            protocol=config.odoo.protocol,
            port=config.odoo.port,
        )

    def login(self, login: str, password: str, db: str) -> None:
        return self._odoo.login(
            db=db,
            login=login,
            password=password,
        )

    async def fetch_user(
        self,
        user_id: int,
    ) -> odoorpc.models.Model | None:
        try:
            model = self._odoo.env["res.users"]
            res_users_id = model.search(
                [
                    ("telegram_id", "=", user_id),
                    ("employee_type", "=", "employee"),
                ],
                limit=1,
            )
            res_users = model.browse(res_users_id)
            return res_users
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_users(
        self,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        try:
            model = self._odoo.env["res.users"]
            res_users = model.search_read(
                [("employee_type", "=", "employee")],
                fields=["id", "telegram_id", "name"],
                limit=limit,
                offset=offset,
            )
            if isinstance(res_users, list) and all(
                isinstance(item, dict) for item in res_users
            ):
                return res_users
            else:
                logging.error("Unexpected return type from search_read")
                return None
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_users_count(
        self,
    ) -> int | None:
        try:
            model = self._odoo.env["res.users"]
            count = model.search_count([("employee_type", "=", "employee")])
            if isinstance(count, int):
                return count
            else:
                logging.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_equipment(
        self,
        equipment_id: int,
    ) -> odoorpc.models.Model | None:
        try:
            equipment = self._odoo.env["maintenance.equipment"].browse(
                equipment_id,
            )
            return equipment
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_equipments(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        try:
            model = self._odoo.env["maintenance.equipment"]
            equipment_ids = model.search(
                [("technician_user_id.telegram_id", "=", user_id)],
                limit=limit,
                offset=offset,
            )
            equipments = model.browse(equipment_ids)
            return equipments
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_equipments_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            model = self._odoo.env["maintenance.equipment"]
            count = model.search_count(
                [("technician_user_id.telegram_id", "=", user_id)],
            )
            if isinstance(count, int):
                return count
            else:
                logging.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_maintenance(
        self,
        maintenance_id: int,
    ) -> odoorpc.models.Model | None:
        try:
            maintenance = self._odoo.env["maintenance.request"].browse(
                maintenance_id,
            )
            return maintenance
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_maintenances(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        try:
            model = self._odoo.env["maintenance.request"]
            request_ids = model.search(
                [("user_id.telegram_id", "=", user_id)],
                limit=limit,
                offset=offset,
            )
            requests = model.browse(request_ids)
            return requests
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_maintenances_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            model = self._odoo.env["maintenance.request"]
            count = model.search_count(
                [("user_id.telegram_id", "=", user_id)],
            )
            if isinstance(count, int):
                return count
            else:
                logging.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return None

    async def forward_maintenance(
        self,
        maintenance_id: int,
        user_id: int,
    ) -> bool:
        try:
            maintenance = self._odoo.env["maintenance.request"].browse(
                maintenance_id,
            )
            maintenance.write({"user_id": user_id})
            return True
        except odoorpc.error.RPCError as e:
            logging.error(e)
            return False
