from __future__ import annotations

import os

from aiogram import Bot, Dispatcher
from fluent.runtime import FluentLocalization, FluentResourceLoader

from .config import settings
from .middlewares import I18nMiddleware


def make_i18n_middleware():
    default_locale = settings.app.default_locale
    supported_locales = settings.app.supported_locales
    loader = FluentResourceLoader(
        os.path.join(
            os.path.dirname(__file__),
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


def setup_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware(make_i18n_middleware())
    dp.callback_query.middleware(make_i18n_middleware())


async def main():
    dp = Dispatcher()
    setup_middlewares(dp)
    bot = Bot(token=settings.bot.token)
    await dp.start_polling(bot)
