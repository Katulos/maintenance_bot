import os
import pathlib

from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory
from fluent.runtime import FluentLocalization, FluentResourceLoader

from app.bot.middlewares.antiflood_middleware import AntiFloodMiddleware
from app.bot.middlewares.data_middleware import LoadDataMiddleware

# from app.bot.middlewares.add_user_middleware import AddUserMiddleware
# from app.bot.middlewares.antiflood_middleware import AntiFloodMiddleware
# from app.bot.middlewares.data_middleware import LoadDataMiddleware
from app.bot.middlewares.i18n_middleware import I18nMiddleware
from app.bot.middlewares.init_middleware import InitMiddleware
from app.bot.middlewares.odoo_middleware import OdooMiddleware

# from app.bot.middlewares.init_middleware import InitMiddleware


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


def setup(
    dp: Dispatcher,
    bg_manager_factory: BgManagerFactory,
) -> None:
    dp.update.middleware(
        InitMiddleware(bg_manager_factory=bg_manager_factory),
    )

    dp.update.middleware(LoadDataMiddleware())

    dp.update.outer_middleware(AntiFloodMiddleware())

    dp.message.middleware(_make_i18n_middleware())
    dp.callback_query.middleware(_make_i18n_middleware())

    dp.message.middleware(OdooMiddleware())
    dp.callback_query.middleware(OdooMiddleware())

    # dp.update.middleware(AddUserMiddleware())
