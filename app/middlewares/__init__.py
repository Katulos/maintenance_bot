from __future__ import annotations

from .i18n import I18nMiddleware
from .logging import StructLoggingMiddleware
from .odoo_register import OdooRegisterMiddleware

__all__ = [
    "OdooRegisterMiddleware",
    "StructLoggingMiddleware",
    "I18nMiddleware",
]
