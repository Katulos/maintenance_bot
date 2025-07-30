from dishka import Provider, Scope, provide

from app.core.config.odoo import OdooConfig
from app.core.infrastructure.odoo.odoo import Odoo
from app.core.infrastructure.odoo.odoorpc import OdooRPC


class OdooProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_odoo(
        self,
        config: OdooConfig,
    ) -> Odoo:
        return OdooRPC(config)
