import logging

from dishka import Provider, Scope, provide
from odoorpc import ODOO

from ...config import settings


class OdooProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_odoo(self) -> ODOO:
        try:
            client = ODOO(
                host=settings.get("odoo.host"),
                port=settings.get("odoo.port"),
                protocol=settings.get("odoo.protocol"),
            )
            client.login(
                db=settings.get("odoo.database"),
                login=settings.get("odoo.username"),
                password=settings.get("odoo.password"),
            )
            return client
        except Exception as e:
            logging.error(e)
