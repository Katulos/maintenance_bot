import os
import pathlib

from aiogram import Dispatcher
from fluent.runtime import FluentLocalization, FluentResourceLoader

from app.bot.middlewares.antiflood_middleware import AntiFloodMiddleware
from app.bot.middlewares.i18n_middleware import I18nMiddleware
from app.bot.middlewares.odoo_middleware import OdooMiddleware


def _make_i18n_middleware() -> I18nMiddleware:
    default_locale = "en"
    supported_locales = ["en", "ru"]
    loader = FluentResourceLoader(
        os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent.parent,
            "locales",
            "{locale}",
        ),
    )
    l10ns = {
        locale: FluentLocalization(
            [locale, default_locale],
            ["main.ftl"],
            loader,
        )
        for locale in supported_locales
    }
    return I18nMiddleware(l10ns, default_locale)


def setup(dp: Dispatcher) -> None:
    # Antiflood middleware
    dp.update.outer_middleware(AntiFloodMiddleware())

    # i18n middleware
    dp.message.middleware(_make_i18n_middleware())
    dp.callback_query.middleware(_make_i18n_middleware())

    # Check odoo registration middleware
    # dp.update.outer_middleware(OdooMiddleware())
    # dp.message.middleware(OdooMiddleware())
    # dp.callback_query.middleware(OdooMiddleware())
