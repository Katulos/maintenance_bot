from dishka import Provider, Scope, provide, AsyncContainer

from app.core.config.main import Config
from app.core.infrastructure.odoo.odoo import Odoo
from app.core.infrastructure.odoo.odoorpc import OdooRPC


class OdooProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_odoo(self,
        container: AsyncContainer,
        config: Config,) -> Odoo:
        return OdooRPC(container, config)

