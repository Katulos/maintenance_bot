import odoorpc
from dishka import AsyncContainer

from app.core.config.main import Config
from app.core.infrastructure.odoo.odoo import Odoo


class OdooRPC(Odoo):

    def __init__(self,
                 container: AsyncContainer, config: Config) -> None:
        self.container = container
        self._odoo = odoorpc.ODOO(
            host=config.odoo.host,
            protocol=config.odoo.protocol,
            port=config.odoo.port,
        )
