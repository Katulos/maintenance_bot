import logging

from dishka import Provider, Scope, provide
from odoorpc import ODOO

from app.core.config.odoo import OdooConfig


class OdooProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_odoo(
        self,
        config: OdooConfig,
    ) -> ODOO:
        try:
            client = ODOO(
                host=config.host,
                port=config.port,
                protocol=config.protocol,
            )
            client.login(
                db=config.database,
                login=config.username,
                password=config.password,
            )
            return client
        except Exception as e:
            logging.error(e)
