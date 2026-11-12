import asyncio
import logging
from typing import Any

from dishka import Provider, Scope, provide
from odoorpc import ODOO
from odoorpc.error import RPCError

from ...config import settings


class OdooProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_odoo(self) -> ODOO:
        try:
            odoo_config: dict[str, Any] = {
                "host": settings.get("odoo.host"),
                "port": settings.get("odoo.port"),
                "protocol": settings.get("odoo.protocol"),
                "db": settings.get("odoo.database"),
                "login": settings.get("odoo.username"),
                "password": settings.get("odoo.password"),
            }

            client = await asyncio.to_thread(
                self._initialize_and_login_odoo,
                odoo_config,
            )

            await asyncio.to_thread(
                self._verify_module_installed,
                client,
                "user_telegram_contact",
            )

            return client

        except RPCError as e:
            logging.error(
                "Odoo RPC Error during dependency resolution: %s",
                e,
            )
            raise
        except Exception as e:
            logging.error(
                "Unexpected error during Odoo client initialization: %s",
                e,
            )
            raise

    @staticmethod
    def _initialize_and_login_odoo(config: dict[str, Any]) -> ODOO:
        client = ODOO(
            host=config["host"],
            port=config["port"],
            protocol=config["protocol"],
        )
        client.login(
            db=config["db"],
            login=config["login"],
            password=config["password"],
        )
        return client

    @staticmethod
    def _verify_module_installed(client: ODOO, module_name: str) -> None:
        module_model = client.env["ir.module.module"]

        module_ids = module_model.search([("name", "=", module_name)])

        if not module_ids:
            raise RPCError(
                f"Odoo module '{module_name}' not found in database registry.",
            )

        module_record = module_model.browse(module_ids[0])
        current_state = module_record.state

        if current_state != "installed":
            raise RPCError(
                f"Odoo module '{module_name}' is not installed. Current state: '{current_state}'",
            )
