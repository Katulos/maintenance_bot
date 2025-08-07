import logging
from typing import Any

from odoorpc import ODOO
from odoorpc.error import RPCError
from odoorpc.models import Model

from app.core.config.odoo import OdooConfig
from app.core.infrastructure.odoo.odoo import Odoo


class OdooRPC(Odoo):
    def __init__(
        self,
        config: OdooConfig,
    ) -> None:
        self._odoo = ODOO(
            host=config.host,
            protocol=config.protocol,
            port=config.port,
        )

    def login(self, login: str, password: str, db: str) -> None:
        return self._odoo.login(
            db=db,
            login=login,
            password=password,
        )

    async def accept_maintenance(self, maintenance_id: int) -> bool:
        try:
            record: Model = self._odoo.env["maintenance.request"].browse(
                maintenance_id,
            )
            next_stage = self._odoo.env["maintenance.stage"].search(
                [("sequence", ">", record.stage_id.sequence)],
                order="sequence asc",
                limit=1,
            )
            if next_stage:
                record.with_context().write(
                    {"stage_id": next_stage.id, "kanban_state": "done"},
                )
            return True
        except RPCError as e:
            logging.error(e)
            return False

    async def close_maintenance(self, maintenance_id: int) -> bool:
        try:
            record: Model = self._odoo.env["maintenance.request"].browse(
                maintenance_id,
            )
            next_stage = self._odoo.env["maintenance.stage"].search(
                [("sequence", ">", record.stage_id.sequence)],
                order="sequence asc",
                limit=1,
            )
            if next_stage:
                record.with_context().write(
                    {"stage_id": next_stage[0], "kanban_state": "done"},
                )
            return True
        except RPCError as e:
            logging.error(e)
            return False

    async def fetch_user(
        self,
        user_id: int,
    ) -> Model | None:
        try:
            model: Model = self._odoo.env["res.users"]
            res_users_id = model.search(
                [
                    ("telegram_id", "=", user_id),
                    ("employee_type", "=", "employee"),
                ],
                limit=1,
            )
            res_users = model.browse(res_users_id)
            return res_users
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_users(
        self,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        try:
            model: Model = self._odoo.env["res.users"]
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
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_users_count(
        self,
    ) -> int | None:
        try:
            model: Model = self._odoo.env["res.users"]
            count = model.search_count([("employee_type", "=", "employee")])
            if isinstance(count, int):
                return count
            else:
                logging.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_equipment(
        self,
        equipment_id: int,
    ) -> Model | None:
        try:
            equipment: Model = self._odoo.env["maintenance.equipment"].browse(
                equipment_id,
            )
            return equipment
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_equipments(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> Model | None:
        try:
            model: Model = self._odoo.env["maintenance.equipment"]
            equipment_ids = model.search(
                [("technician_user_id.telegram_id", "=", user_id)],
                limit=limit,
                offset=offset,
            )
            equipments = model.browse(equipment_ids)
            return equipments
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_equipments_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            model: Model = self._odoo.env["maintenance.equipment"]
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
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_maintenance(
        self,
        maintenance_id: int,
    ) -> Model | None:
        try:
            record: Model = self._odoo.env["maintenance.request"].browse(
                maintenance_id,
            )
            return record
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_maintenances(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> Model | None:
        try:
            model: Model = self._odoo.env["maintenance.request"]
            request_ids = model.search(
                [
                    ("user_id.telegram_id", "=", user_id),
                    ("archive", "=", False),
                ],
                limit=limit,
                offset=offset,
            )
            requests = model.browse(request_ids)
            return requests
        except RPCError as e:
            logging.error(e)
            return None

    async def fetch_user_maintenances_count(
        self,
        user_id: int,
    ) -> int | None:
        try:
            model: Model = self._odoo.env["maintenance.request"]
            count = model.search_count(
                [
                    ("user_id.telegram_id", "=", user_id),
                    ("archive", "=", False),
                ],
            )
            if isinstance(count, int):
                return count
            else:
                logging.error(
                    f"Unexpected type returned by search_count: {type(count)}",
                )
                return None
        except RPCError as e:
            logging.error(e)
            return None

    async def forward_maintenance(
        self,
        maintenance_id: int,
        user_id: int,
    ) -> bool:
        try:
            maintenance: Model = self._odoo.env["maintenance.request"].browse(
                maintenance_id,
            )
            maintenance.write({"user_id": user_id})
            return True
        except RPCError as e:
            logging.error(e)
            return False
